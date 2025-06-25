# eLearning AI Teaching Assistant Module

This module extends Odoo's eLearning platform (`website_slides`) with AI-powered Teaching Assistant capabilities using Groq API.

## Features

### For Students
- **AI Teaching Assistant**: Students can ask questions and get instant, contextual help from an AI TA
- **Course-Aware Responses**: AI understands the course content and provides relevant explanations
- **Study Guidance**: Get study tips, concept explanations, and learning strategies
- **24/7 Availability**: Always available to assist with coursework and questions
- **Personalized Support**: Adapts responses based on course context and student needs

### For Instructors  
- **AI Teaching Assistant**: Helps with course design, content creation, and teaching strategies
- **Quick Actions**: Pre-defined prompts for content ideas, engagement tips, and assessment design
- **Pedagogical Support**: AI provides teaching best practices and educational guidance
- **Course Enhancement**: Suggestions for improving student engagement and learning outcomes
- **Assessment Design**: Help creating effective quizzes, assignments, and evaluations

### For Administrators
- **Course-level Configuration**: Enable/disable AI TA per course
- **Personality Settings**: Choose AI TA personality (friendly, professional, adaptive, structured)
- **Custom Messages**: Set custom welcome messages and course context for each course
- **Global Settings**: Configure Groq API integration and default settings

## Installation & Setup

### Prerequisites
- Odoo 15.0 with `website_slides` module installed
- Python 3.7+
- Groq API account (free at [console.groq.com](https://console.groq.com))

### Quick Setup
1. **Run the setup script:**
   ```bash
   cd /path/to/odoo
   ./addons/website_slides_ai_tutor/setup.sh
   ```

2. **Configure API Key:**
   Edit the `.env` file in your Odoo root directory:
   ```bash
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Install the module:**
   ```bash
   ./odoo-bin -d your_database -u website_slides_ai_tutor
   ```

### Manual Installation
1. **Install dependencies:**
   ```bash
   pip install groq>=0.9.0
   ```

2. **Set environment variable:**
   ```bash
   export GROQ_API_KEY="your_groq_api_key"
   ```
   Or add to your `.env` file in Odoo root.

3. **Update Odoo:**
   ```bash
   ./odoo-bin -d your_database -u website_slides_ai_tutor
   ```

### Configuration
- Go to **Website > Configuration > Settings**
- Scroll to **eLearning** section
- Configure AI Teaching Assistant settings
- Enable for specific courses in course settings

## Installation Status ✅

**SUCCESSFULLY INSTALLED AND CONFIGURED**

The AI Teaching Assistant module has been successfully installed on your Odoo 15 instance. Here's what's been implemented:

### ✅ What's Working

1. **Module Installation**: Successfully installed in database `v15_test`
2. **Model Extensions**: Added AI fields to `slide.channel` and `res.config.settings`
3. **View Inheritance**: Course forms, tree views, and configuration settings extended
4. **Website Templates**: AI tutor widgets added to lesson and course pages
5. **Controller Endpoints**: Chat and health check endpoints implemented
6. **Groq API Integration**: Ready to use with your API key
7. **Security Configuration**: Access control rules in place

### 🎯 Current Module Features

- **AI Teaching Assistant Widget**: Appears on lesson pages when enabled
- **Instructor AI Assistant**: Available on course management pages
- **Per-Course Configuration**: Enable/disable AI TA for each course individually
- **Global Settings**: Configure Groq API settings in Website > Configuration > Settings
- **Secure API Key Management**: Uses environment variables and Odoo config
- **Health Check Endpoint**: Monitor AI service status
- **Fallback System**: Graceful degradation when API is unavailable

### 🔧 Current Configuration

1. **API Key Location**: `/home/claude/git/odoo/15.0/.env`
   ```bash
   GROQ_API_KEY=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
   ```

2. **Database**: `v15_test`
3. **Odoo Version**: 15.0
4. **Module Status**: Installed and Active

### 🌐 Access Your Installation

- **Odoo Instance**: http://localhost:8069
- **eLearning Courses**: http://localhost:8069/slides
- **Backend Settings**: Settings > Website > eLearning

### 🚀 Next Steps to See It in Action

1. **Log into Odoo**: Visit http://localhost:8069/web/login
2. **Go to eLearning**: Navigate to Website > Slides
3. **Create/Edit a Course**: Enable "AI Teaching Assistant" in course settings
4. **Add Content**: Create lessons with content
5. **View Frontend**: Visit the course page to see the AI widget

The AI Teaching Assistant will appear as a collapsible widget on lesson pages and provide intelligent, context-aware assistance to both students and instructors.

### 🔍 Verification

To verify the installation is working:
- The module appears in Apps as "eLearning AI Tutor"
- Course editing forms show "AI Teaching Assistant" tab
- Website settings show eLearning AI configuration options
- No errors in Odoo logs during startup

## Usage Examples

### For Students
```
Student: "I don't understand this concept about database normalization"
AI TA: "Great question! Database normalization is like organizing your closet. Just as you wouldn't mix socks with formal shirts, normalization separates different types of data into their own tables to avoid confusion and redundancy. Let me break down the key normal forms..."
```

### For Instructors  
```
Instructor: "How can I make my database course more engaging?"
AI TA: "Here are some proven strategies for database courses:
1. Use real-world examples (social media platforms, e-commerce)
2. Hands-on labs with actual database tools
3. Progressive complexity - start with simple queries
4. Visual tools like ER diagrams
5. Group projects designing databases for local businesses
Would you like me to elaborate on any of these approaches?"
```

## Technical Implementation

### AI Integration
- **Groq Client**: Uses official Groq Python client library
- **Model**: LLaMA 3.1-8b-instant for fast, high-quality responses
- **Context-Aware**: Incorporates course content, lesson materials, and user roles
- **Streaming Support**: Real-time response generation capability
- **Fallback System**: Graceful degradation when API is unavailable
- **Role-Based Responses**: Different AI behavior for students vs instructors

### Security Features
- **Environment Variables**: API keys stored securely in `.env` file
- **Odoo Integration**: Fallback to Odoo system parameters
- **Permission Checks**: Role-based access control
- **Health Monitoring**: API status and connectivity checks
- **Error Handling**: Comprehensive logging and error recovery

### Architecture
```
Frontend (JavaScript) → Odoo Controller → Groq API → AI Response
                     ↓
               Database (Course Context) → Enhanced Prompt
```

### API Endpoints
- `/slides/ai_tutor/chat` - Main chat interface
- `/slides/ai_tutor/config/<channel_id>` - Get course configuration  
- `/slides/ai_tutor/health` - Service health check (admin only)

## Customization

### Adding Custom Personalities
Edit `/models/slide_channel.py`:
```python
ai_tutor_personality = fields.Selection([
    ('friendly', 'Friendly & Encouraging'),
    ('professional', 'Professional & Direct'), 
    ('adaptive', 'Adaptive & Personalized'),
    ('strict', 'Structured & Disciplined'),
    ('custom', 'Your Custom Style'),  # Add this
], ...)
```

### Modifying AI Prompts
Edit `_build_ta_system_prompt` method in `/controllers/main.py` to customize how the AI responds.

### Adding New Models
The system supports different Groq models. Update the model parameter:
```python
model="llama-3.1-70b-versatile"  # For more complex reasoning
model="mixtral-8x7b-32768"       # For longer context
```

## Performance & Limits

### Groq API Limits
- **Free Tier**: 30 requests/minute, 6,000 tokens/minute
- **Response Time**: Typically 200-800ms
- **Max Tokens**: Configurable (default: 500)

### Optimization Tips
- Use streaming for better user experience
- Implement response caching for common questions
- Monitor usage through health check endpoint
- Set appropriate timeout values

## Troubleshooting

### Common Issues

**"Groq client not installed"**
```bash
pip install groq>=0.9.0
```

**"No Groq API key configured"**
- Check `.env` file in Odoo root
- Verify environment variable: `echo $GROQ_API_KEY`
- Check Odoo system parameters

**"API request failed"**
- Verify API key is valid
- Check internet connectivity
- Review Groq API status
- Check logs: `/var/log/odoo/odoo.log`

**Health Check**
Access `/slides/ai_tutor/health` as an instructor to see service status.

## Support & Development

### Contributing
1. Fork the repository
2. Create feature branch
3. Test with different course types
4. Submit pull request

### Logging
Enable debug logging in Odoo configuration:
```ini
[logger_website_slides_ai_tutor]
level = DEBUG
handlers = hand01
qualname = website_slides_ai_tutor
```

### Development Tips
- Use the fallback responses for testing without API
- Implement caching for production environments
- Consider rate limiting for high-traffic sites
- Monitor token usage to manage costs

For technical support or feature requests, contact your system administrator or the module developer.
