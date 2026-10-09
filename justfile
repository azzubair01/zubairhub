# zubairhub justfile

set shell := ["bash", "-uc"]

# List available recipes
default:
    @just --list

# Set up ARM64 virtual environment and install dependencies
setup:
    @if [ ! -d ".venv" ]; then \
        echo "Creating ARM64 virtual environment (.venv)..."; \
        arch -arm64 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv; \
    fi
    @echo "Installing dependencies via pip..."
    arch -arm64 .venv/bin/pip install --upgrade pip
    arch -arm64 .venv/bin/pip install -r requirements.txt

# Fast setup using uv
setup-uv:
    @if [ ! -d ".venv" ]; then \
        echo "Creating ARM64 virtual environment (.venv)..."; \
        arch -arm64 /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv; \
    fi
    @echo "Installing dependencies via uv..."
    arch -arm64 uv pip install -r requirements.txt --python .venv/bin/python

# Run the Streamlit application
run *args:
    @if [ ! -d ".venv" ]; then \
        echo "Error: Virtual environment (.venv) not found. Please run 'just setup' first."; \
        exit 1; \
    fi
    arch -arm64 .venv/bin/streamlit run app.py {{args}}
