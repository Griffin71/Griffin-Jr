function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    let chatBox = document.getElementById('chat-box');
    
    if (userInput.trim() === '') return;

    let userMessage = `<div><strong>You:</strong> ${userInput}</div>`;
    chatBox.innerHTML += userMessage;

    // Send the user's message to the server and get the response
    fetch(`/get?msg=${encodeURIComponent(userInput)}`)
        .then(response => response.text())
        .then(data => {
            let botMessage = `<div><strong>Griffin Jr.:</strong> ${data}</div>`;
            chatBox.innerHTML += botMessage;
            chatBox.scrollTop = chatBox.scrollHeight;
        });

    document.getElementById('user-input').value = '';
}
