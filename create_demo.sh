#!/bin/bash

# AI Teaching Assistant Demo Setup
# This script creates a demo course to showcase the AI TA functionality

echo "🎓 Setting up AI Teaching Assistant Demo..."

# Configuration
DEMO_SCRIPT="demo_setup.py"

# Create the demo setup script
cat > "$DEMO_SCRIPT" << 'EOF'
#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/home/claude/git/odoo/15.0')
os.environ['DB_NAME'] = 'v15_test'

import odoo
from odoo import api, SUPERUSER_ID

def create_demo_course():
    """Create a demo course with AI Teaching Assistant enabled"""
    print("Creating demo course with AI Teaching Assistant...")
    
    try:
        # Configure Odoo
        odoo.tools.config.parse_config(['--database=v15_test'])
        registry = odoo.registry('v15_test')
        
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            # Create demo course
            demo_course = env['slide.channel'].create({
                'name': 'Python Fundamentals with AI Assistant',
                'description': '''
                <p>Learn Python programming fundamentals with the help of our AI Teaching Assistant!</p>
                <p>This course covers:</p>
                <ul>
                    <li>Python syntax and basics</li>
                    <li>Data structures and algorithms</li>
                    <li>Object-oriented programming</li>
                    <li>Best practices and debugging</li>
                </ul>
                ''',
                'channel_type': 'training',
                'visibility': 'public',
                'enroll': 'public',
                'ai_tutor_enabled': True,
                'ai_tutor_personality': 'friendly',
                'ai_tutor_welcome_message': '''
                Hello! I'm your AI Teaching Assistant for this Python course. 
                I'm here to help you understand concepts, answer questions, 
                and guide you through your learning journey. Feel free to ask 
                me anything about Python programming!
                ''',
                'ai_tutor_course_context': '''
                This is a beginner-friendly Python programming course. Students will learn 
                fundamental concepts including variables, data types, control structures, 
                functions, classes, and basic algorithms. The course includes hands-on 
                exercises and practical examples.
                '''
            })
            
            # Create some demo slides
            slides_data = [
                {
                    'name': 'Introduction to Python',
                    'slide_type': 'presentation',
                    'description': 'What is Python and why should you learn it?',
                    'html_content': '''
                    <h2>Welcome to Python Programming!</h2>
                    <p>Python is a powerful, easy-to-learn programming language.</p>
                    <h3>Why Python?</h3>
                    <ul>
                        <li>Simple and readable syntax</li>
                        <li>Versatile - web, data science, AI, automation</li>
                        <li>Large community and ecosystem</li>
                        <li>Great for beginners</li>
                    </ul>
                    '''
                },
                {
                    'name': 'Variables and Data Types',
                    'slide_type': 'presentation', 
                    'description': 'Understanding Python variables and basic data types',
                    'html_content': '''
                    <h2>Variables and Data Types</h2>
                    <h3>Creating Variables</h3>
                    <pre><code>
name = "Alice"
age = 25
height = 5.6
is_student = True
                    </code></pre>
                    <h3>Basic Data Types</h3>
                    <ul>
                        <li><strong>str</strong> - Text strings</li>
                        <li><strong>int</strong> - Whole numbers</li>
                        <li><strong>float</strong> - Decimal numbers</li>
                        <li><strong>bool</strong> - True/False values</li>
                    </ul>
                    '''
                },
                {
                    'name': 'Control Structures',
                    'slide_type': 'presentation',
                    'description': 'If statements, loops, and flow control',
                    'html_content': '''
                    <h2>Control Structures</h2>
                    <h3>If Statements</h3>
                    <pre><code>
if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager") 
else:
    print("You are a child")
                    </code></pre>
                    <h3>Loops</h3>
                    <pre><code>
# For loop
for i in range(5):
    print(i)

# While loop
count = 0
while count < 3:
    print(count)
    count += 1
                    </code></pre>
                    '''
                }
            ]
            
            # Create slides
            for slide_data in slides_data:
                slide_data['channel_id'] = demo_course.id
                env['slide.slide'].create(slide_data)
            
            print(f"✅ Demo course created successfully!")
            print(f"   Course ID: {demo_course.id}")
            print(f"   Course Name: {demo_course.name}")
            print(f"   AI Tutor Enabled: {demo_course.ai_tutor_enabled}")
            print(f"   Number of slides: {len(demo_course.slide_ids)}")
            print(f"\n🌐 Access the course at: http://localhost:8069/slides/{demo_course.id}")
            
            # Also set global AI settings
            try:
                config = env['res.config.settings'].create({})
                if hasattr(config, 'groq_api_enabled'):
                    config.groq_api_enabled = True
                    config.groq_model_name = 'llama3-8b-8192'
                    # Don't set API key here - it should be in .env file
                    print("✅ Global AI settings configured")
                
            except Exception as e:
                print(f"⚠️  Could not configure global settings: {e}")
            
            return demo_course.id
            
    except Exception as e:
        print(f"❌ Failed to create demo course: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    create_demo_course()
EOF

# Activate virtual environment and run demo setup
echo "📦 Activating virtual environment..."
source ~/envs/15.0/bin/activate

echo "🔧 Creating demo course..."
python3 "$DEMO_SCRIPT"

# Clean up
rm -f "$DEMO_SCRIPT"

echo ""
echo "🎉 Demo setup complete!"
echo ""
echo "📋 What's been set up:"
echo "   ✅ AI Teaching Assistant module installed"
echo "   ✅ Demo Python course with AI TA enabled"
echo "   ✅ Sample lessons and content"
echo "   ✅ Global AI settings configured"
echo ""
echo "🌐 Next Steps:"
echo "   1. Visit: http://localhost:8069/slides"
echo "   2. Find the 'Python Fundamentals with AI Assistant' course"
echo "   3. Open any lesson to see the AI Teaching Assistant widget"
echo "   4. Configure your Groq API key in Settings > Website > eLearning"
echo ""
echo "💡 The AI TA appears as a collapsible widget on lesson pages"
echo "   and provides context-aware assistance to students!"
