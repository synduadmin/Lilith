// static/js/chat.js
const roomName = 'chatbot';
const chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/chatbot/' + roomName + '/'
);

chatSocket.onmessage = function(event) {
    const message = event.data;
    const messageContainer = document.querySelector('#message-container');
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    messageContainer.appendChild(messageElement);
};

document.querySelector('#chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const messageInput = document.querySelector('#chat-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInput.value = '';
});
