#!/bin/bash

echo "🚀 Comprehensive Siril MCP Testing Suite"
echo "========================================"

# Check dependencies
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command -v python &> /dev/null; then
    echo "❌ Python is required but not installed"
    exit 1
fi

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pipenv install --dev

echo "🧪 Running test suites..."

# Run basic functionality tests
echo ""
echo "1️⃣ Basic functionality tests..."
node test-natural-language-scenarios.js

echo ""
echo "2️⃣ User workflow tests..."
node test-user-workflows.js

echo ""
echo "✅ All MCP tests completed!"
