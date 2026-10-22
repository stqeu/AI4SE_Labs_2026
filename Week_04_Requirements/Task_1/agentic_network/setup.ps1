# Creates an isolated virtual environment in .\.venv and installs dependencies.
# Usage (from this folder, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

# Pick a Python interpreter (py launcher first, then python on PATH)
$py = $null
if (Get-Command py -ErrorAction SilentlyContinue) { $py = "py -3" }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
else { Write-Error "Python 3.10+ not found on PATH."; exit 1 }

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment in .venv ..."
    Invoke-Expression "$py -m venv .venv"
}

$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $venvPy -m pip install --upgrade pip
& $venvPy -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example - put your OPENAI_API_KEY in it."
}

Write-Host ""
Write-Host "Setup done. Next:"
Write-Host "  1) Edit .env and set OPENAI_API_KEY"
Write-Host "  2) .\.venv\Scripts\python.exe check_setup.py"
