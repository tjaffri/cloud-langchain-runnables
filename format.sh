#!/bin/bash
set -e

echo "🎨 Running code formatters..."

echo "Running black..."
poetry run black cloud_langchain_runnables/ tests/

echo "Running isort..."
poetry run isort cloud_langchain_runnables/ tests/

echo "Running autopep8..."
poetry run autopep8 --in-place --recursive --max-line-length 88 cloud_langchain_runnables/ tests/

echo "✨ All formatting complete!" 