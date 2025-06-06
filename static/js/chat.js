document.addEventListener('DOMContentLoaded', function() {
    // Mode switching
    const chatMode = document.getElementById('chat-mode');
    const uploadMode = document.getElementById('upload-mode');
    const chatInterface = document.getElementById('chat-interface');
    const uploadInterface = document.getElementById('upload-interface');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');

    // Mode switching functionality
    chatMode.addEventListener('click', () => {
        chatMode.classList.add('active');
        uploadMode.classList.remove('active');
        chatInterface.style.display = 'block';
        uploadInterface.style.display = 'none';
    });

    uploadMode.addEventListener('click', () => {
        uploadMode.classList.add('active');
        chatMode.classList.remove('active');
        uploadInterface.style.display = 'block';
        chatInterface.style.display = 'none';
    });

    // Handle chat form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value;
        if (!message.trim()) return;

        // Add user message
        addMessage(message, 'user');
        userInput.value = '';

        // Show loading state
        addMessage('...', 'bot loading');

        // Get bot response
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: `message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            chatContainer.removeChild(chatContainer.lastChild);
            // Add bot response
            addMessage(data.response, 'bot');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove loading message
            chatContainer.removeChild(chatContainer.lastChild);
            addMessage('Sorry, I encountered an error.', 'bot');
        });
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', `${sender}-message`);
        messageDiv.textContent = text;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});