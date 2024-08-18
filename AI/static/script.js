document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    function sendMessage() {
        const message = inputField.value.trim();
        if (message) {
            // Add the user's message to the chat box
            chatBox.innerHTML += `<div class="message user-message">You: ${message}</div>`;
            // Scroll to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
            // Clear the input field
            inputField.value = '';

            // Fetch response from the server
            fetch(`/get?msg=${encodeURIComponent(message)}`)
                .then(response => response.text())
                .then(botResponse => {
                    // Add the bot's response to the chat box
                    chatBox.innerHTML += `<div class="message bot-message">Griffin Jr.: ${botResponse}</div>`;
                    // Scroll to the bottom
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }

    // Send message when "Enter" is pressed
    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action (e.g., new line)
            sendMessage();
        }
    });
});
