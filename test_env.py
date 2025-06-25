#!/usr/bin/env python3
"""Test script to verify python-dotenv integration"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, '.')

# Import dotenv
from dotenv import load_dotenv

print("Testing python-dotenv integration...")

# Get the Odoo root directory
odoo_root = Path(__file__).parent
env_file = odoo_root / '.env'

print(f"Odoo root: {odoo_root}")
print(f"Env file: {env_file}")
print(f"Env file exists: {env_file.exists()}")

# Load environment variables
if env_file.exists():
    load_dotenv(env_file)
    print("✓ .env file loaded successfully")
else:
    print("✗ .env file not found")

# Check if GROQ_API_KEY is available
groq_key = os.getenv('GROQ_API_KEY')
if groq_key:
    print(f"✓ GROQ_API_KEY loaded: {groq_key[:20]}...")
else:
    print("✗ GROQ_API_KEY not found in environment")

# Test Groq import
try:
    from groq import Groq
    print("✓ Groq library available")
    
    if groq_key:
        try:
            client = Groq(api_key=groq_key)
            print("✓ Groq client initialized successfully")
        except Exception as e:
            print(f"✗ Failed to initialize Groq client: {e}")
    else:
        print("✗ Cannot test Groq client without API key")
        
except ImportError as e:
    print(f"✗ Groq library not available: {e}")

print("\nTest completed!")
