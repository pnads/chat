// chat.js

document.addEventListener('DOMContentLoaded', function () {
    const chatMessageInput = document.querySelector('#chat-message-input');
    const chatLog = document.querySelector('#chat-log');

    const roomName = chatMessageInput.dataset.roomName;
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        chatLog.innerHTML += data.message + '<br>';
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    chatMessageInput.focus();
    chatMessageInput.addEventListener('keyup', function (event) {
        if (event.keyCode === 13) {  // Enter key
            const message = chatMessageInput.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            chatMessageInput.value = '';
        }
    });
});
