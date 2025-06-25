# -*- coding: utf-8 -*-

import json
import logging
import os
from odoo import http, fields, _
from odoo.http import request

# Import Groq client
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logging.getLogger(__name__).warning("Groq client not installed. Please install with: pip install groq")

_logger = logging.getLogger(__name__)


class WebsiteSlidesAITutor(http.Controller):

    @http.route('/slides/ai_tutor/chat', type='json', auth='user', website=True)
    def ai_tutor_chat(self, message, channel_id=None, slide_id=None, **kwargs):
        """Handle AI tutor chat messages"""
        try:
            # Get course context
            channel = None
            if channel_id:
                try:
                    channel = request.env['slide.channel'].browse(int(channel_id))
                    if not channel.exists():
                        channel = None
                        _logger.warning(f"Channel {channel_id} does not exist")
                    else:
                        _logger.info(f"Found channel: {channel.name} (ID: {channel.id})")
                        # Check if AI is enabled, but don't block if it's not
                        if hasattr(channel, 'ai_tutor_enabled') and not channel.ai_tutor_enabled:
                            _logger.info(f"AI not enabled for channel {channel.name}, but allowing anyway")
                except (ValueError, TypeError) as e:
                    _logger.error(f"Invalid channel_id {channel_id}: {e}")
                    channel = None
            
            # Get slide context if provided
            slide = None
            if slide_id:
                try:
                    slide = request.env['slide.slide'].browse(int(slide_id))
                    if not slide.exists():
                        slide = None
                        _logger.warning(f"Slide {slide_id} does not exist")
                    else:
                        _logger.info(f"Found slide: {slide.name} (ID: {slide.id})")
                except (ValueError, TypeError) as e:
                    _logger.error(f"Invalid slide_id {slide_id}: {e}")
                    slide = None
            
            # Build comprehensive context for AI
            course_name = channel.name if channel else 'General Course'
            course_description = ''
            course_short_description = ''
            course_type = ''
            course_tags = []
            instructor_name = ''
            course_stats = {}
            
            if channel:
                # Main description
                if hasattr(channel, 'description') and channel.description:
                    course_description = channel.description
                
                # Short description for course cards
                if hasattr(channel, 'description_short') and channel.description_short:
                    course_short_description = channel.description_short
                
                # Course type (training/documentation)
                if hasattr(channel, 'channel_type') and channel.channel_type:
                    course_type = channel.channel_type
                
                # Course tags for subject matter
                if hasattr(channel, 'tag_ids') and channel.tag_ids:
                    course_tags = [tag.name for tag in channel.tag_ids]
                
                # Instructor information
                if hasattr(channel, 'user_id') and channel.user_id:
                    instructor_name = channel.user_id.name
                
                # Course statistics for context
                if hasattr(channel, 'total_slides'):
                    course_stats = {
                        'total_slides': getattr(channel, 'total_slides', 0),
                        'total_time': getattr(channel, 'total_time', 0),
                        'members_count': getattr(channel, 'members_count', 0),
                        'nbr_video': getattr(channel, 'nbr_video', 0),
                        'nbr_document': getattr(channel, 'nbr_document', 0),
                        'nbr_quiz': getattr(channel, 'nbr_quiz', 0),
                    }
            
            # Get additional course context from AI tutor settings
            course_context = ''
            if channel and hasattr(channel, 'ai_tutor_course_context') and channel.ai_tutor_course_context:
                course_context = channel.ai_tutor_course_context
            
            context = {
                'user_message': message,
                'course_name': course_name,
                'course_description': course_description,
                'course_short_description': course_short_description,
                'course_type': course_type,
                'course_tags': course_tags,
                'instructor_name': instructor_name,
                'course_stats': course_stats,
                'course_context': course_context,
                'slide_name': slide.name if slide else '',
                'slide_content': slide.description if slide else '',
                'user_name': request.env.user.name,
                'user_is_student': not request.env.user.has_group('website_slides.group_website_slides_officer'),
            }
            
            _logger.info(f"AI Tutor context: course={course_name}, description_available={bool(course_description)}, user={context['user_name']}, is_student={context['user_is_student']}")
            
            
            # For real AI implementation using Groq API
            response = self._generate_ai_response_groq(context, channel)
            
            return {
                'success': True,
                'response': response,
                'timestamp': fields.Datetime.now().isoformat(),
            }
            
        except Exception as e:
            _logger.error(f"AI Tutor error: {e}")
            return {
                'error': 'Sorry, I encountered an error. Please try again later.',
                'success': False
            }

    def _generate_ai_response(self, context, channel=None):
        """Generate AI tutor response (demo implementation)"""
        message = context['user_message'].lower()
        user_name = context['user_name']
        course_name = context['course_name']
        
        # Simple rule-based responses for demo
        if any(word in message for word in ['hello', 'hi', 'hey']):
            personality = channel.ai_tutor_personality if channel else 'friendly'
            if personality == 'friendly':
                return f"Hello {user_name}! 😊 I'm so excited to help you learn {course_name}. What can I assist you with today?"
            elif personality == 'professional':
                return f"Good day, {user_name}. I'm your AI learning assistant for {course_name}. How may I help you?"
            else:
                return f"Hi {user_name}! I'm here to support your learning journey in {course_name}. What would you like to know?"
        
        elif any(word in message for word in ['help', 'stuck', 'confused', 'difficult']):
            return f"I understand this can be challenging, {user_name}. Let me break this down for you. Can you tell me specifically what part you're finding difficult? I'm here to guide you step by step! 💪"
        
        elif any(word in message for word in ['quiz', 'test', 'exam', 'assessment']):
            return f"Great question about assessments! Remember, the key to success is understanding the concepts, not just memorizing. Would you like me to help you review the key points for {course_name}?"
        
        elif any(word in message for word in ['progress', 'how am i doing', 'performance']):
            return f"You're making progress, {user_name}! 🎯 Learning is a journey, and every step counts. Keep practicing and don't hesitate to ask questions. What specific area would you like to focus on improving?"
        
        elif any(word in message for word in ['thanks', 'thank you', 'appreciate']):
            return f"You're very welcome, {user_name}! 🌟 I'm always here to help. Remember, there's no such thing as a silly question - keep learning and growing!"
        
        else:
            # Default intelligent response
            return f"That's an interesting question about {course_name}, {user_name}! 🤔 While I'd love to give you a detailed answer, I think the best approach would be to: 1) Review the relevant course materials, 2) Try to identify the specific concept you're unclear about, and 3) Feel free to ask me more specific questions. I'm here to guide your learning journey!"

    @http.route('/slides/ai_tutor/config/<int:channel_id>', type='json', auth='user', website=True)
    def get_ai_tutor_config(self, channel_id, **kwargs):
        """Get AI tutor configuration for a specific channel"""
        try:
            channel = request.env['slide.channel'].browse(channel_id)
            if not channel.exists():
                return {'error': 'Course not found'}
            
            return {
                'success': True,
                'config': channel._get_ai_tutor_config()
            }
        except Exception as e:
            _logger.error(f"AI Tutor config error: {e}")
            return {'error': 'Could not load AI tutor configuration'}

    def _generate_ai_response_groq(self, context, channel=None):
        """Generate AI Teaching Assistant response using Groq API"""
        try:
            # Check if Groq is available
            if not GROQ_AVAILABLE:
                _logger.error("Groq client not available")
                return self._generate_fallback_response(context, channel)
            
            # Get API key from environment or system parameters
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                # Fallback to system parameters
                api_key = request.env['ir.config_parameter'].sudo().get_param('website_slides_ai_tutor.api_key')
            
            if not api_key:
                _logger.error("No Groq API key configured")
                return self._generate_fallback_response(context, channel)
            
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Build comprehensive context for the TA
            system_prompt = self._build_ta_system_prompt(context, channel)
            user_message = context['user_message']
            
            # Create chat completion
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast and efficient model
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=500,
                temperature=0.7,
                top_p=0.9,
                stream=False  # Set to False for simpler response handling
            )
            
            # Extract response
            if completion.choices and len(completion.choices) > 0:
                ai_response = completion.choices[0].message.content.strip()
                return ai_response
            else:
                _logger.error("No response from Groq API")
                return self._generate_fallback_response(context, channel)
                
        except Exception as e:
            _logger.error(f"Groq API request failed: {e}")
            return self._generate_fallback_response(context, channel)

    def _build_ta_system_prompt(self, context, channel=None):
        """Build comprehensive system prompt for AI Teaching Assistant"""
        user_name = context['user_name']
        course_name = context['course_name']
        is_student = context['user_is_student']
        slide_name = context['slide_name']
        slide_content = context['slide_content']
        course_description = context['course_description']
        course_short_description = context['course_short_description']
        course_type = context['course_type']
        course_tags = context['course_tags']
        instructor_name = context['instructor_name']
        course_stats = context['course_stats']
        course_context = context.get('course_context', '')
        
        personality = "friendly and encouraging"
        if channel and hasattr(channel, 'ai_tutor_personality') and channel.ai_tutor_personality:
            personality_map = {
                'friendly': 'friendly and encouraging',
                'professional': 'professional and direct',
                'adaptive': 'adaptive and personalized',
                'strict': 'structured and disciplined'
            }
            personality = personality_map.get(channel.ai_tutor_personality, 'friendly and encouraging')
        
        if is_student:
            role_context = f"You are a Teaching Assistant helping a student named {user_name}. Explain concepts clearly, provide study guidance, and encourage learning."
        else:
            role_context = f"You are a Teaching Assistant helping an instructor named {user_name}. Assist with course design, teaching strategies, and pedagogical questions."
        
        # Build comprehensive course information section
        context_info = f"Course Name: {course_name}"
        
        # Add main description if available
        if course_description:
            context_info += f"\nCourse Description: {course_description}"
        elif course_short_description:
            context_info += f"\nCourse Description: {course_short_description}"
        
        # Add course type and tags for subject context
        if course_type:
            type_label = "Training Course" if course_type == "training" else "Documentation"
            context_info += f"\nCourse Type: {type_label}"
        
        if course_tags:
            context_info += f"\nCourse Topics: {', '.join(course_tags)}"
        
        # Add instructor information
        if instructor_name:
            context_info += f"\nInstructor: {instructor_name}"
        
        # Add course statistics for context
        if course_stats and course_stats.get('total_slides', 0) > 0:
            stats_text = []
            if course_stats.get('total_slides'):
                stats_text.append(f"{course_stats['total_slides']} lessons")
            if course_stats.get('total_time'):
                hours = course_stats['total_time']
                if hours >= 1:
                    stats_text.append(f"{hours:.1f} hours duration")
                else:
                    stats_text.append(f"{int(hours * 60)} minutes duration")
            if course_stats.get('nbr_video'):
                stats_text.append(f"{course_stats['nbr_video']} videos")
            if course_stats.get('nbr_document'):
                stats_text.append(f"{course_stats['nbr_document']} documents")
            if course_stats.get('nbr_quiz'):
                stats_text.append(f"{course_stats['nbr_quiz']} quizzes")
            if stats_text:
                context_info += f"\nCourse Content: {', '.join(stats_text)}"
        
        # Add additional context if available
        if course_context:
            context_info += f"\nAdditional Context: {course_context}"
        
        # Add current lesson context if applicable
        if slide_name:
            context_info += f"\nCurrent Lesson: {slide_name}"
            if slide_content:
                context_info += f"\nLesson Content: {slide_content[:200]}..." if len(slide_content) > 200 else f"\nLesson Content: {slide_content}"
        
        system_prompt = f"""You are an AI Teaching Assistant for {course_name}.

{role_context}

Course Information:
{context_info}

Be {personality}, helpful, and supportive. When asked about the course, use the specific information above to provide detailed answers about what this course covers, its structure, and content. Address the user as {user_name}."""
        
        return system_prompt

    def _generate_fallback_response(self, context, channel=None):
        """Generate fallback response when API fails"""
        user_name = context['user_name']
        is_student = context['user_is_student']
        
        if is_student:
            return f"Hi {user_name}! I'm having some technical difficulties right now, but I'm still here to help! Could you try rephrasing your question, or let me know what specific topic you'd like to discuss? I'll do my best to assist you with your learning. 📚"
        else:
            return f"Hello {user_name}! I'm experiencing some connectivity issues at the moment, but I'm ready to help with your teaching needs. What aspect of your course would you like to discuss - content creation, student engagement, or assessment strategies? 👨‍🏫"

    def _generate_ai_response_groq_stream(self, context, channel=None):
        """Generate AI Teaching Assistant response using Groq API with streaming"""
        try:
            # Check if Groq is available
            if not GROQ_AVAILABLE:
                _logger.error("Groq client not available")
                return self._generate_fallback_response(context, channel)
            
            # Get API key from environment or system parameters
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                api_key = request.env['ir.config_parameter'].sudo().get_param('website_slides_ai_tutor.api_key')
            
            if not api_key:
                _logger.error("No Groq API key configured")
                return self._generate_fallback_response(context, channel)
            
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Build comprehensive context for the TA
            system_prompt = self._build_ta_system_prompt(context, channel)
            user_message = context['user_message']
            
            # Create streaming chat completion
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                max_tokens=500,
                temperature=0.7,
                top_p=0.9,
                stream=True,
                stop=None
            )
            
            # Collect streamed response
            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            
            return full_response.strip() if full_response else self._generate_fallback_response(context, channel)
                
        except Exception as e:
            _logger.error(f"Groq streaming API request failed: {e}")
            return self._generate_fallback_response(context, channel)

    @http.route('/slides/ai_tutor/health', type='json', auth='user', website=True)
    def ai_tutor_health_check(self, **kwargs):
        """Check AI Teaching Assistant service health"""
        try:
            # Check if user has permission to see health status
            if not request.env.user.has_group('website_slides.group_website_slides_officer'):
                return {'error': 'Insufficient permissions'}
            
            health_status = {
                'groq_available': GROQ_AVAILABLE,
                'api_key_configured': bool(os.getenv('GROQ_API_KEY') or 
                                          request.env['ir.config_parameter'].sudo().get_param('website_slides_ai_tutor.api_key')),
                'service_status': 'healthy'
            }
            
            # Test API connection if key is available
            if health_status['groq_available'] and health_status['api_key_configured']:
                try:
                    api_key = os.getenv('GROQ_API_KEY') or request.env['ir.config_parameter'].sudo().get_param('website_slides_ai_tutor.api_key')
                    client = Groq(api_key=api_key)
                    
                    # Simple test call
                    test_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=10
                    )
                    
                    if test_completion.choices:
                        health_status['api_test'] = 'success'
                    else:
                        health_status['api_test'] = 'failed'
                        health_status['service_status'] = 'degraded'
                        
                except Exception as e:
                    health_status['api_test'] = f'failed: {str(e)}'
                    health_status['service_status'] = 'degraded'
            else:
                health_status['service_status'] = 'unavailable'
            
            return {
                'success': True,
                'health': health_status
            }
            
        except Exception as e:
            _logger.error(f"Health check failed: {e}")
            return {
                'success': False,
                'error': 'Health check failed'
            }
