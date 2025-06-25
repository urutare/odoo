#!/usr/bin/env python3
"""
Quick test script to validate the AI Tutor module installation
"""

import sys
import os

# Add Odoo to path
sys.path.insert(0, '/home/claude/git/odoo/15.0')
os.environ['DB_NAME'] = 'v15_test'

import odoo
from odoo import api, SUPERUSER_ID

def test_ai_tutor_module():
    """Test the AI tutor module installation and functionality"""
    print("🧪 Testing AI Teaching Assistant Module...")
    
    try:
        # Configure Odoo
        odoo.tools.config.parse_config(['--database=v15_test'])
        registry = odoo.registry('v15_test')
        
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            # Test 1: Check module installation
            print("\n1️⃣ Checking module installation...")
            modules = env['ir.module.module'].search([('name', '=', 'website_slides_ai_tutor')])
            if modules and modules.state == 'installed':
                print("✅ Module is installed and active")
            else:
                print(f"❌ Module not found or not installed (state: {modules.state if modules else 'not found'})")
                return False
            
            # Test 2: Check slide.channel model extensions
            print("\n2️⃣ Checking slide.channel model extensions...")
            channel_model = env['slide.channel']
            ai_fields = ['ai_tutor_enabled', 'ai_tutor_personality', 'ai_tutor_welcome_message', 'ai_tutor_course_context']
            for field in ai_fields:
                if hasattr(channel_model, field):
                    print(f"✅ Field '{field}' exists")
                else:
                    print(f"❌ Field '{field}' missing")
            
            # Test 3: Check config settings model extensions
            print("\n3️⃣ Checking config settings extensions...")
            config_model = env['res.config.settings']
            config_fields = ['groq_api_enabled', 'groq_api_key', 'groq_model_name']
            for field in config_fields:
                if hasattr(config_model, field):
                    print(f"✅ Config field '{field}' exists")
                else:
                    print(f"❌ Config field '{field}' missing")
            
            # Test 4: Check view inheritance
            print("\n4️⃣ Checking view inheritance...")
            views = env['ir.ui.view'].search([
                ('model', 'in', ['slide.channel', 'res.config.settings']),
                ('inherit_id', '!=', False),
                ('name', 'ilike', 'ai')
            ])
            print(f"✅ Found {len(views)} AI-related view extensions")
            for view in views:
                print(f"   - {view.name} (extends {view.inherit_id.name})")
            
            # Test 5: Create a test course with AI enabled
            print("\n5️⃣ Creating test course...")
            try:
                test_channel = env['slide.channel'].create({
                    'name': 'AI Test Course',
                    'channel_type': 'training',
                    'ai_tutor_enabled': True,
                    'ai_tutor_personality': 'friendly',
                    'ai_tutor_welcome_message': 'Hello! I am your AI teaching assistant for this course.',
                    'ai_tutor_course_context': 'This is a test course to validate AI functionality.'
                })
                print(f"✅ Test course created with ID: {test_channel.id}")
                print(f"   - AI Tutor Enabled: {test_channel.ai_tutor_enabled}")
                print(f"   - Personality: {test_channel.ai_tutor_personality}")
                
                # Clean up
                test_channel.unlink()
                print("✅ Test course cleaned up")
                
            except Exception as e:
                print(f"❌ Failed to create test course: {e}")
            
            # Test 6: Check templates exist
            print("\n6️⃣ Checking website templates...")
            templates = env['ir.ui.view'].search([
                ('type', '=', 'qweb'),
                ('key', 'ilike', 'ai_tutor')
            ])
            print(f"✅ Found {len(templates)} AI tutor templates")
            for template in templates:
                print(f"   - {template.key}: {template.name}")
            
            print("\n🎉 Module test completed successfully!")
            return True
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_ai_tutor_module()
