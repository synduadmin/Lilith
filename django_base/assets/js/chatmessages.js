document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const input = document.querySelector('#message');
    const messages = document.querySelector('#messages');
    const roomName = generateUUID();
    const isSecure = window.location.protocol === 'https:';
    const wsProtocol = isSecure ? 'wss://' : 'ws://';
    const asgiWebSocketUrl = wsProtocol + window.location.host + '/chat_asgi/' + roomName + '/';
    const reconnectInterval = 1000;
    let socket;
  
    function generateUUID() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }
  
    function setupWebSocket() {
      socket = new WebSocket(asgiWebSocketUrl);
  
      socket.onopen = (event) => {
        console.log('WebSocket connected:', event);
      };
  
      socket.onmessage = (event) => {
        console.log('WebSocket message received:', event);
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
  
      socket.onerror = (event) => {
        console.error('WebSocket error:', event);
      };
  
      socket.onclose = (event) => {
        console.warn('WebSocket closed:', event);
        setTimeout(() => {
          setupWebSocket();
        }, reconnectInterval);
      };
    }
  
    setupWebSocket();
  
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const uniqueId = 'msg';
      const timestamp = new Date().getTime();
      const messageId = `${uniqueId}-${timestamp}`;
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
  