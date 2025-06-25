# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    # AI Teaching Assistant Configuration
    ai_tutor_enabled = fields.Boolean(
        string='Enable AI Teaching Assistant',
        default=True,
        help="Enable AI Teaching Assistant functionality for this course"
    )
    ai_tutor_personality = fields.Selection([
        ('friendly', 'Friendly & Encouraging'),
        ('professional', 'Professional & Direct'),
        ('adaptive', 'Adaptive & Personalized'),
        ('strict', 'Structured & Disciplined'),
    ], string='AI TA Personality', default='friendly',
       help="Choose the personality style for the AI Teaching Assistant")
    
    ai_tutor_welcome_message = fields.Text(
        string='AI TA Welcome Message',
        default="Hello! I'm your AI Teaching Assistant. I'm here to help you succeed in this course by answering questions, explaining concepts, and providing study guidance. Feel free to ask me anything!",
        help="Custom welcome message from the AI Teaching Assistant"
    )
    
    ai_tutor_course_context = fields.Text(
        string='Course Context for AI TA',
        help="Provide specific context about this course that the AI Teaching Assistant should know to give better assistance. Include key topics, learning objectives, prerequisites, etc."
    )
    
    def _get_ai_tutor_config(self):
        """Get AI Teaching Assistant configuration for this channel"""
        self.ensure_one()
        return {
            'enabled': self.ai_tutor_enabled,
            'personality': self.ai_tutor_personality,
            'welcome_message': self.ai_tutor_welcome_message,
            'course_context': self.ai_tutor_course_context,
            'course_name': self.name,
            'course_description': self.description,
        }
