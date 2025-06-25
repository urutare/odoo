# -*- coding: utf-8 -*-
{
    'name': 'eLearning AI Tutor',
    'version': '1.0.0',
    'category': 'Website/eLearning',
    'summary': 'Add AI Tutor functionality to eLearning courses',
    'description': """
eLearning AI Tutor Enhancement
==============================

This module extends the Odoo eLearning platform with AI Tutor capabilities:

Features:
* AI Tutor widget on student pages
* AI Tutor assistant for instructors
* Course-specific AI guidance
* Interactive learning assistance
* Custom student support interface

Installation:
This module depends on website_slides and should be installed after it.
""",
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': [
        'website_slides',
        'website_profile',
    ],
    'external_dependencies': {
        'python': ['groq'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/website_slides_templates_ai_tutor.xml',
        'views/slide_channel_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_slides_ai_tutor/static/src/js/ai_tutor.js',
            'website_slides_ai_tutor/static/src/css/ai_tutor.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
