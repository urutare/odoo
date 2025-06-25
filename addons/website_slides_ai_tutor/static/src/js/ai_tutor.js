odoo.define('website_slides_ai_tutor.ai_tutor', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var rpc = require('web.rpc');
var _t = core._t;

publicWidget.registry.AITutorWidget = publicWidget.Widget.extend({
    selector: '.o_ai_tutor_widget, .o_ai_tutor_instructor_widget',
    events: {
        'click #toggleAITutor': '_toggleTutor',
        'click #toggleInstructorAI': '_toggleInstructorAI',
        'click #sendAIMessage': '_sendMessage',
        'click #sendInstructorAIMessage': '_sendInstructorMessage',
        'keypress #aiTutorInput': '_onKeypress',
        'keypress #instructorAIInput': '_onInstructorKeypress',
        'click .ai-quick-action': '_onQuickAction',
    },

    start: function () {
        this._super.apply(this, arguments);
        this._initializeAITutor();
        return this._super.apply(this, arguments);
    },

    _initializeAITutor: function () {
        // Get current slide/channel context
        var currentUrl = window.location.pathname;
        this.channelId = this._extractChannelId(currentUrl);
        this.slideId = this._extractSlideId(currentUrl);
        this.isInstructor = this.$el.hasClass('o_ai_tutor_instructor_widget');
        
        // Load AI tutor configuration
        if (this.channelId) {
            this._loadAIConfig();
        }
    },

    _extractChannelId: function (url) {
        var match = url.match(/\/slides\/(?:course-)?(\d+)/);
        return match ? parseInt(match[1]) : null;
    },

    _extractSlideId: function (url) {
        var match = url.match(/\/slides\/slide\/(\d+)/);
        return match ? parseInt(match[1]) : null;
    },

    _loadAIConfig: function () {
        var self = this;
        rpc.query({
            route: '/slides/ai_tutor/config/' + this.channelId,
        }).then(function (result) {
            if (result.success) {
                self.aiConfig = result.config;
            }
        });
    },

    _toggleTutor: function (ev) {
        ev.preventDefault();
        var $body = this.$('#aiTutorBody');
        var $icon = this.$(ev.currentTarget).find('i');
        
        $body.slideToggle();
        $icon.toggleClass('fa-chevron-up fa-chevron-down');
    },

    _toggleInstructorAI: function (ev) {
        ev.preventDefault();
        var $body = this.$('#instructorAIBody');
        var $icon = this.$(ev.currentTarget).find('i');
        
        $body.slideToggle();
        $icon.toggleClass('fa-chevron-up fa-chevron-down');
    },

    _onKeypress: function (ev) {
        if (ev.which === 13) { // Enter key
            this._sendMessage();
        }
    },

    _onInstructorKeypress: function (ev) {
        if (ev.which === 13) { // Enter key
            this._sendInstructorMessage();
        }
    },

    _sendMessage: function (ev) {
        if (ev) ev.preventDefault();
        var $input = this.$('#aiTutorInput');
        var message = $input.val().trim();
        
        if (!message) return;
        
        this._addUserMessage(message, '#aiTutorChat');
        $input.val('');
        this._sendToAI(message, false);
    },

    _sendInstructorMessage: function (ev) {
        if (ev) ev.preventDefault();
        var $input = this.$('#instructorAIInput');
        var message = $input.val().trim();
        
        if (!message) return;
        
        this._addUserMessage(message, '#instructorAIChat');
        $input.val('');
        this._sendToAI(message, true);
    },

    _onQuickAction: function (ev) {
        ev.preventDefault();
        var action = this.$(ev.currentTarget).data('action');
        var message = this._getQuickActionMessage(action);
        
        this._addUserMessage(message, '#instructorAIChat');
        this._sendToAI(message, true);
    },

    _getQuickActionMessage: function (action) {
        switch (action) {
            case 'content-ideas':
                return 'As a TA, can you suggest some engaging content ideas and activities for my course that would help students learn better?';
            case 'engagement-tips':
                return 'What are some proven teaching strategies to increase student engagement and participation in online learning?';
            case 'assessment-help':
                return 'Help me design effective assessments that truly measure student understanding and provide meaningful feedback.';
            default:
                return 'As my teaching assistant, how can you help me improve the effectiveness of my course?';
        }
    },

    _addUserMessage: function (message, chatContainer) {
        var $chat = this.$(chatContainer);
        var userMessageHtml = 
            '<div class="user-message mb-2">' +
                '<div class="d-flex align-items-start justify-content-end">' +
                    '<div class="bg-primary text-white p-2 rounded shadow-sm" style="max-width: 80%;">' +
                        '<span>' + _.escape(message) + '</span>' +
                    '</div>' +
                    '<i class="fa fa-user text-primary ml-2 mt-1"></i>' +
                '</div>' +
            '</div>';
        
        $chat.append(userMessageHtml);
        $chat.scrollTop($chat[0].scrollHeight);
    },

    _addAIMessage: function (message, chatContainer, isInstructor) {
        var $chat = this.$(chatContainer);
        var iconClass = isInstructor ? 'fa-graduation-cap text-success' : 'fa-robot text-primary';
        var aiMessageHtml = 
            '<div class="ai-message mb-2">' +
                '<div class="d-flex align-items-start">' +
                    '<i class="fa ' + iconClass + ' mr-2 mt-1"></i>' +
                    '<div class="bg-white p-2 rounded shadow-sm flex-grow-1">' +
                        '<span>' + _.escape(message) + '</span>' +
                    '</div>' +
                '</div>' +
            '</div>';
        
        $chat.append(aiMessageHtml);
        $chat.scrollTop($chat[0].scrollHeight);
    },

    _addTypingIndicator: function (chatContainer, isInstructor) {
        var $chat = this.$(chatContainer);
        var iconClass = isInstructor ? 'fa-graduation-cap text-success' : 'fa-robot text-primary';
        var typingHtml = 
            '<div class="ai-typing mb-2">' +
                '<div class="d-flex align-items-start">' +
                    '<i class="fa ' + iconClass + ' mr-2 mt-1"></i>' +
                    '<div class="bg-light p-2 rounded shadow-sm">' +
                        '<div class="typing-dots">' +
                            '<span></span><span></span><span></span>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>';
        
        $chat.append(typingHtml);
        $chat.scrollTop($chat[0].scrollHeight);
    },

    _removeTypingIndicator: function (chatContainer) {
        this.$(chatContainer).find('.ai-typing').remove();
    },

    _sendToAI: function (message, isInstructor) {
        var self = this;
        var chatContainer = isInstructor ? '#instructorAIChat' : '#aiTutorChat';
        
        this._addTypingIndicator(chatContainer, isInstructor);
        
        rpc.query({
            route: '/slides/ai_tutor/chat',
            params: {
                message: message,
                channel_id: this.channelId,
                slide_id: this.slideId,
                is_instructor: isInstructor,
            }
        }).then(function (result) {
            self._removeTypingIndicator(chatContainer);
            
            if (result.success) {
                self._addAIMessage(result.response, chatContainer, isInstructor);
            } else {
                self._addAIMessage(result.error || 'Sorry, I encountered an error. Please try again.', chatContainer, isInstructor);
            }
        }).catch(function (error) {
            self._removeTypingIndicator(chatContainer);
            self._addAIMessage('Sorry, I\'m having trouble connecting. Please try again later.', chatContainer, isInstructor);
        });
    },
});

return publicWidget.registry.AITutorWidget;

});
