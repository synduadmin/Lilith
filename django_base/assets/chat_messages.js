document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const input = document.querySelector('#message');
    const messages = document.querySelector('#messages');

    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    const roomName = generateUUID();

    // Replace 'YOUR_ASGI_WEBSOCKET_URL' with the actual URL of your ASGI WebSocket endpoint
    const asgiWebSocketUrl = 
        'ws://'
        + window.location.host
        + '/ws/chat_asgi/'
        + roomName
        + '/';

    const socket = new WebSocket(asgiWebSocketUrl);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const jsonData = JSON.parse(decodeURIComponent(data.message));

        const messageId = `${Date.now()}-bot`;
        messages.innerHTML += `
            <div id="message-${messageId}" class="message_card">
                <div class="message bot_message p-2">
                    <div class="bot_profile">Lilith:</div>
                    <div class="bot_message_body">
                    ${jsonData.response}
                    </div>
                </div>
            </div>`;
        messages.scrollTop = messages.scrollHeight;
    };

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const uniqueId = 'msg';
        const timestamp = new Date().getTime();
        let messageId = `${uniqueId}-${timestamp}`;

        const message = input.value;
        input.value = '';
        messages.innerHTML += `
            <div id="message-${messageId}" class="message_card">
            <div class="message user_message p-2">
                <div class="you_profile">You:</div>
                <div class="message_body"> ${message}</div>
            </div>
            </div>`;

        const data = {
            message: message
        };
        socket.send(JSON.stringify(data));
    });
});
