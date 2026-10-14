import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict, deque
from pathlib import Path

TASK_2_DATA = Path(__file__).resolve().parent.parent / "Task_2" / "data"
PROMPTS = ["RTF", "CO-STAR", "CoT"]


def load_database():
    """Build the restaurant database in memory (same as the Task 2 checker)."""
    tables = {}
    with (TASK_2_DATA / "restaurants-schema.csv").open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        for table, field, _pk, _fk, column_type in reader:
            if table.strip() != "-":
                tables.setdefault(table.strip(), []).append((field.strip(), column_type.strip().lower()))

    conn = sqlite3.connect(":memory:")
    for table, columns in tables.items():
        conn.execute(f'CREATE TABLE "{table}" ({", ".join(f"{name}" for name, _ in columns)})')

    with (TASK_2_DATA / "restaurants-db.txt").open(encoding="utf-8") as f:
        for line in f:
            table, values_text = re.fullmatch(r"([A-Z_]+)\((.*)\)", line.rstrip("\r\n")).groups()
            values = next(csv.reader([values_text], skipinitialspace=True))
            converted = [
                int(v) if t.startswith("int") else float(v) if t.startswith("decimal") else v
                for v, (_, t) in zip(values, tables[table])
            ]
            conn.execute(f'INSERT INTO "{table}" VALUES ({", ".join("?" * len(values))})', converted)
    return conn


def row_f1(predicted, expected):
    predicted, expected = Counter(map(tuple, predicted)), Counter(map(tuple, expected))
    if not predicted and not expected:
        return 1.0
    overlap = sum((predicted & expected).values())
    if overlap == 0:
        return 0.0
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    return 2 * precision * recall / (precision + recall)


def main():
    csv.field_size_limit(1_000_000_000)
    conn = load_database()
    results = []

    for prompt in PROMPTS:
        labels = defaultdict(deque)
        with (TASK_2_DATA / "restaurants_dataset.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                labels[row["question"]].append(json.loads(row["result"]))

        scores = []
        with (TASK_2_DATA / prompt / "restaurants_dataset_predictions.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                expected = labels[row["question"]].popleft()
                try:
                    predicted = conn.execute(row["predicted_sql"]).fetchall()
                    scores.append(row_f1(predicted, expected))
                except Exception:
                    scores.append(0.0)

        mean_f1 = sum(scores) / len(scores)
        results.append({"prompt": prompt, "row_overlap_f1": round(mean_f1, 4)})
        print(f"{prompt:8} Row Overlap F1 = {mean_f1:.4f}")

    with (Path(__file__).resolve().parent / "results.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["prompt", "row_overlap_f1"])
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
