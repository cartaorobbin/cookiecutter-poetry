#!/bin/bash

echo "🚀 Setting up cookiecutter-poetry development environment..."

# Update package lists
sudo apt-get update

# Install Poetry
echo "📦 Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vscode/.local/bin:$PATH"
echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> ~/.bashrc

# Configure Poetry
echo "⚙️ Configuring Poetry..."
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

# Install development dependencies (cookiecutter + testing tools)
echo "📚 Installing development dependencies..."
poetry install

# Install pre-commit hooks
echo "🔗 Setting up pre-commit hooks..."
poetry run pre-commit install

# Create directories for testing cookiecutter template generation
echo "📁 Creating test directories..."
mkdir -p /tmp/test-projects

# Make sure the shell sources poetry
echo "🔄 Setting up shell environment..."
echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> ~/.zshrc || true

# Display setup completion
echo "✅ Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  poetry install                    - Install dependencies"
echo "  poetry run pytest                 - Run tests"
echo "  poetry run pre-commit run --all-files - Run code quality checks"
echo "  poetry run cookiecutter .         - Test cookiecutter template generation"
echo "  cd /tmp/test-projects && poetry run cookiecutter /workspaces/cookiecutter-poetry - Generate test project"
echo "  make install                      - Install project (if Makefile available)"
echo "  make test                         - Run tests (if Makefile available)"
echo ""
echo "🧪 To test the Cursor feature:"
echo "  1. Generate a project with cursor_support='y'"
echo "  2. Check if .cursor/rules/development.mdc is created correctly"
echo ""
echo "🎉 Happy cookiecutter template development!" 