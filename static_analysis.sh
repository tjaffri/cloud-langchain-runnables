#!/bin/bash
set -e

echo "🔍 Running type checking with mypy..."
poetry run mypy cloud_langchain_runnables/ tests/

echo "🎨 Running code formatting check with black..."
poetry run black --check cloud_langchain_runnables/ tests/

echo "📝 Running import sorting check with isort..."
poetry run isort --check-only cloud_langchain_runnables/ tests/

echo "🔬 Running code quality checks with flake8..."
poetry run flake8 cloud_langchain_runnables/ tests/

echo "✅ All checks passed!" 