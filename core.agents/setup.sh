#!/bin/bash

echo "🚀 Setting up Interview Agent Environment"
echo "========================================"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install basic dependencies first
echo ""
echo "📦 Installing basic dependencies..."
pip3 install pydantic typing-extensions

# Install strands-agents (this might not be available in public PyPI)
echo ""
echo "📦 Installing Strands Agents..."
echo "⚠️  Note: strands-agents might need to be installed from source or private repository"
echo "   For now, we'll install the available dependencies"

# Install other dependencies
echo ""
echo "📦 Installing other dependencies..."
pip3 install boto3 PyPDF2 python-docx

echo ""
echo "✅ Basic dependencies installed!"
echo ""
echo "📝 Next steps:"
echo "1. Install strands-agents from the official source"
echo "2. Configure AWS credentials: aws configure"
echo "3. Enable Bedrock model access in AWS console"
echo "4. Run the test: python3 test_interview_agent.py"
echo ""
echo "🔗 Strands Agents documentation: https://strandsagents.com"
