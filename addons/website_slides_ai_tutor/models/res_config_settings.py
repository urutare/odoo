# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # AI Teaching Assistant Global Settings
    ai_tutor_api_key = fields.Char(
        string='AI TA API Key',
        config_parameter='website_slides_ai_tutor.api_key',
        help="API key for the AI Teaching Assistant service (currently using Groq)"
    )
    
    ai_tutor_service_provider = fields.Selection([
        ('groq', 'Groq (Current)'),
        ('openai', 'OpenAI GPT'),
        ('anthropic', 'Anthropic Claude'),
        ('custom', 'Custom AI Service'),
    ], string='AI Service Provider',
       config_parameter='website_slides_ai_tutor.service_provider',
       default='groq',
       help="Choose the AI service provider for the Teaching Assistant functionality")
    
    ai_tutor_default_enabled = fields.Boolean(
        string='Enable AI Teaching Assistant by Default',
        config_parameter='website_slides_ai_tutor.default_enabled',
        default=True,
        help="Enable AI Teaching Assistant by default for new courses"
    )
