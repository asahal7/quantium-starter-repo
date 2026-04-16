#!/bin/bash

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

source "$REPO_DIR/venv/bin/activate"

python -m pytest "$REPO_DIR/task5/test_app.py" -v

if [ $? -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Tests failed."
    exit 1
fi
