document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotContainer = document.querySelector('.chatbot-container');
    const chatbotClose = document.querySelector('.chatbot-close');
    const messageInput = document.querySelector('.chatbot-message-input');
    const sendButton = document.querySelector('.chatbot-send');
    const messagesContainer = document.querySelector('.chatbot-messages');
    const quickQuestions = document.querySelectorAll('.quick-question');
    
    // Toggle chatbot visibility
    chatbotToggle.addEventListener('click', function() {
        chatbotContainer.classList.add('active');
        chatbotToggle.classList.add('hidden');
    });
    
    chatbotClose.addEventListener('click', function() {
        chatbotContainer.classList.remove('active');
        chatbotToggle.classList.remove('hidden');
    });
    
    // Send message function
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            typingIndicator.innerHTML = `
                <span></span>
                <span></span>
                <span></span>
            `;
            messagesContainer.appendChild(typingIndicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Simulate bot response after delay
            setTimeout(() => {
                messagesContainer.removeChild(typingIndicator);
                const botResponse = getBotResponse(message);
                addMessage(botResponse, 'bot');
            }, 1500);
        }
    }
    
    // Send message on button click or Enter key
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Quick question buttons
    quickQuestions.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.textContent;
            addMessage(question, 'user');
            
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            typingIndicator.innerHTML = `
                <span></span>
                <span></span>
                <span></span>
            `;
            messagesContainer.appendChild(typingIndicator);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Simulate bot response after delay
            setTimeout(() => {
                messagesContainer.removeChild(typingIndicator);
                const botResponse = getBotResponse(question);
                addMessage(botResponse, 'bot');
            }, 1500);
        });
    });
    
    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Simple bot response logic (replace with real API calls)
    function getBotResponse(question) {
        const lowerQuestion = question.toLowerCase();
        
        if (lowerQuestion.includes('create') && lowerQuestion.includes('event')) {
            return "To create an event, go to your dashboard and click 'Create Event'. Fill in the details like event name, date, location, and ticket options. You can then publish it when ready!";
        } else if (lowerQuestion.includes('ticket') || lowerQuestion.includes('manage')) {
            return "You can manage tickets in the 'Events' section. Click on your event, then 'Ticket Management' to set up different ticket types, prices, and availability.";
        } else if (lowerQuestion.includes('issue') || lowerQuestion.includes('trouble')) {
            return "For technical issues, try refreshing the page first. If the problem persists, you can contact our support team directly through the contact form on this page.";
        } else {
            return "I'm here to help with Eventify-related questions. You can ask about creating events, managing tickets, or troubleshooting issues. For more complex questions, our support team is available 24/7.";
        }
    }
});

