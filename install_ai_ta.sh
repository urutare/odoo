#!/bin/bash

# Quick AI TA Module Installation for v15_test database

echo "🤖 Installing AI Teaching Assistant Module..."

# Make sure we're in the right directory
cd /home/claude/git/odoo/15.0

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source ~/envs/15.0/bin/activate
echo "✅ Virtual environment activated"

# Install Groq dependency
echo "📦 Installing Groq dependency..."
pip install groq>=0.9.0

# Update .env with the actual API key
echo "🔑 Setting up API key..."
if [ ! -f ".env" ]; then
    echo "# AI Teaching Assistant Configuration" > .env
fi

# Remove any existing GROQ_API_KEY line and add the new one
grep -v "GROQ_API_KEY" .env > .env.tmp && mv .env.tmp .env
echo "GROQ_API_KEY=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" >> .env

echo "✅ Configuration complete!"
echo ""
echo "🚀 To install the module, you have two options:"
echo ""
echo "Option 1 - Update existing running instance:"
echo "  source ~/envs/15.0/bin/activate"
echo "  ./odoo-bin -d v15_test -u website_slides_ai_tutor"
echo ""
echo "Option 2 - Install and restart (safer):"
echo "  1. Stop your current Odoo instance (Ctrl+C in the terminal where it's running)"
echo "  2. Run: source ~/envs/15.0/bin/activate"
echo "  3. Run: ./odoo-bin -d v15_test -i website_slides_ai_tutor --stop-after-init"
echo "  4. Restart Odoo normally with: ./odoo-bin -d v15_test --db-filter ^v15_test$ --workers 3"
echo ""
echo "📚 After installation, the AI TA will appear on course and lesson pages!"
echo "💡 Configure global settings in: Website > Configuration > Settings > eLearning"
