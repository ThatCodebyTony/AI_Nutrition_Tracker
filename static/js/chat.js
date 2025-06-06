console.log("chat.js loaded");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    // Mode switching
    const chatMode = document.getElementById('chat-mode');
    const uploadMode = document.getElementById('upload-mode');
    const chatInterface = document.getElementById('chat-interface');
    const uploadInterface = document.getElementById('upload-interface');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');

    console.log("Elements found:", {
        chatMode: !!chatMode,
        uploadMode: !!uploadMode,
        chatInterface: !!chatInterface,
        uploadInterface: !!uploadInterface,
        chatForm: !!chatForm,
        userInput: !!userInput,
        chatContainer: !!chatContainer
    });

    // Mode switching functionality
    if (chatMode && uploadMode) {
        chatMode.addEventListener('click', () => {
            console.log("Chat mode clicked");
            chatMode.classList.add('active');
            uploadMode.classList.remove('active');
            if (chatInterface) chatInterface.style.display = 'block';
            if (uploadInterface) uploadInterface.style.display = 'none';
        });

        uploadMode.addEventListener('click', () => {
            console.log("Upload mode clicked");
            uploadMode.classList.add('active');
            chatMode.classList.remove('active');
            if (uploadInterface) uploadInterface.style.display = 'block';
            if (chatInterface) chatInterface.style.display = 'none';
        });
    }

    // Create a default welcome message
    if (chatContainer) {
        // Add welcome message
        const welcomeDiv = document.createElement('div');
        welcomeDiv.classList.add('chat-message', 'bot-message');
        welcomeDiv.textContent = "Hello! I'm your nutrition assistant. How can I help you today?";
        chatContainer.appendChild(welcomeDiv);
    }

    // Handle chat form submission
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Chat form submitted");

            const message = userInput.value;
            if (!message.trim()) return;

            // Add user message
            addMessage(message, 'user');
            userInput.value = '';

            // Show loading state
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('chat-message', 'bot-message', 'loading');
            chatContainer.appendChild(loadingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            console.log("CSRF Token:", csrfToken);

            // Get bot response
            fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `message=${encodeURIComponent(message)}`
            })
            .then(response => {
                console.log("Response status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Response data:", data);
                
                // Remove loading message
                chatContainer.removeChild(loadingDiv);
                
                // Add bot response
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                console.error('Error:', error);
                // Remove loading message
                chatContainer.removeChild(loadingDiv);
                addMessage('Sorry, I encountered an error.', 'bot');
            });
        });
    } else {
        console.error("Chat form element not found!");
    }

    function addMessage(text, sender) {
        if (!chatContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', `${sender}-message`);
        

        messageDiv.innerHTML = text; 
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        console.log(`Added ${sender} message:`, text);
    }
});