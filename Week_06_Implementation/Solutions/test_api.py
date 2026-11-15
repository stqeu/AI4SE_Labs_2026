from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

r = OpenAI().embeddings.create(model="text-embedding-3-small", input="test")
print("OK, dlzka vektora:", len(r.data[0].embedding))