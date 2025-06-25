#!/bin/bash

# AI Teaching Assistant Module Setup Script

echo "🤖 Setting up AI Teaching Assistant Module..."

# Check if we're in the right directory
if [ ! -f "addons/website_slides_ai_tutor/__manifest__.py" ]; then
    echo "❌ Please run this script from the Odoo root directory"
    exit 1
fi

# Check for virtual environment and activate if available
if [ -f "~/envs/15.0/bin/activate" ]; then
    echo "🐍 Activating Python virtual environment..."
    source ~/envs/15.0/bin/activate
    echo "✅ Virtual environment activated"
elif [ -f "../envs/15.0/bin/activate" ]; then
    echo "🐍 Activating Python virtual environment..."
    source ../envs/15.0/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at ~/envs/15.0/"
    echo "   Please activate manually: source ~/envs/15.0/bin/activate"
    echo "   Then re-run this script"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install groq>=0.9.0

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating one..."
    echo "# AI Teaching Assistant Configuration" > .env
    echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
    echo "📝 Please edit .env file and add your Groq API key"
else
    echo "✅ .env file already exists"
fi

# Check if API key is set
if grep -q "your_groq_api_key_here" .env 2>/dev/null; then
    echo "⚠️  Please update your Groq API key in the .env file"
elif grep -q "GROQ_API_KEY=" .env 2>/dev/null; then
    echo "✅ Groq API key appears to be configured"
else
    echo "⚠️  Please add GROQ_API_KEY to your .env file"
fi

# Detect current running database
CURRENT_DB=""
if command -v pgrep >/dev/null 2>&1; then
    ODOO_PROC=$(ps aux | grep "[o]doo-bin.*-d" | head -1)
    if [ -n "$ODOO_PROC" ]; then
        CURRENT_DB=$(echo "$ODOO_PROC" | grep -o "\-d [^ ]*" | cut -d' ' -f2)
        echo "� Detected running Odoo database: $CURRENT_DB"
    fi
fi

echo ""
echo "�🚀 Setup complete! Next steps:"

if [ -n "$CURRENT_DB" ]; then
    echo "1. Make sure your Groq API key is set in .env file"
    echo "2. Update your Odoo database:"
    echo "   For running instance:"
    echo "     source ~/envs/15.0/bin/activate"
    echo "     ./odoo-bin -d $CURRENT_DB -u website_slides_ai_tutor"
    echo "   Or stop Odoo and run:"
    echo "     source ~/envs/15.0/bin/activate"
    echo "     ./odoo-bin -d $CURRENT_DB -i website_slides_ai_tutor --stop-after-init"
else
    echo "1. Make sure your Groq API key is set in .env file"
    echo "2. Activate virtual environment: source ~/envs/15.0/bin/activate"
    echo "3. Update your Odoo database: ./odoo-bin -d YOUR_DATABASE_NAME -u website_slides_ai_tutor"
    echo "   (Replace YOUR_DATABASE_NAME with your actual database name)"
fi

echo "3. Go to Website Settings to configure the AI Teaching Assistant"
echo ""
echo "📚 The AI TA will appear on course and lesson pages once enabled!"
