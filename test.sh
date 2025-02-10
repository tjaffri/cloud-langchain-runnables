#!/bin/bash
set -e

echo "🧪 Running tests with pytest..."
poetry run pytest tests/

echo "✅ All checks passed!" 