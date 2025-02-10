#!/bin/bash
set -e

echo "🧪 Running tests with pytest and coverage..."
poetry run pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

echo "✅ All checks passed!" 