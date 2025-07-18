#!/bin/env bash

# Build and upload to PyPI script using pipenv
# Usage: ./release.sh [test|prod]

set -e

TARGET=${1:-test}

echo "Installing/updating dependencies with pipenv..."
pipenv install --dev

echo "Building package..."
pipenv run python -m build --clean

if [ "$TARGET" = "test" ]; then
    echo "Uploading to Test PyPI..."
    pipenv run twine upload --repository testpypi dist/*
elif [ "$TARGET" = "prod" ]; then
    echo "Uploading to PyPI..."
    pipenv run twine upload dist/*
else
    echo "Usage: ./release.sh [test|prod]"
    exit 1
fi

echo "Upload complete!"
