#!/bin/bash
# WAN Core Role Tutorial — Environment Setup

set -e

echo "🌐 WAN Core Role Tutorial — Setting up your environment..."
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Install with: brew install python"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 available"
else
    echo "❌ pip3 not found"
    exit 1
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r automation/python/requirements.txt

# Check Ansible
if command -v ansible &> /dev/null; then
    ANSIBLE_VERSION=$(ansible --version | head -1)
    echo "✅ Ansible: $ANSIBLE_VERSION"
else
    echo "📦 Installing Ansible..."
    pip3 install ansible ansible-pylibssh
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker available"
else
    echo "⚠️  Docker not found (optional — needed for Containerlab)"
fi

# Check Containerlab (optional)
if command -v containerlab &> /dev/null; then
    echo "✅ Containerlab available"
else
    echo "⚠️  Containerlab not found (optional — install from containerlab.dev)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Read ROADMAP.md for the learning path"
echo "  2. Start with Module 00: 00-fiserv-context/"
echo "  3. Track progress in PROGRESS.md"
echo "  4. Check automation/ai-prompts/ for AI-assisted workflows"
