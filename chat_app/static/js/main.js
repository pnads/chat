// main.js

document.addEventListener('DOMContentLoaded', function () {
    const chatLog = document.querySelector('#chat-log');
    const chatMessageInput = document.querySelector('#chat-message-input');
    const roomName = chatMessageInput.dataset.roomName;

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if (data.username && data.message) {
            chatLog.insertAdjacentHTML('beforeend', '<div>' + data.username + ': ' + data.message + '</div>');
            chatLog.scrollTop = chatLog.scrollHeight;
        }
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    // Fetch initial messages and render them
    fetch(`/rooms/${roomName}/fetch/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(message => {
                chatLog.insertAdjacentHTML('beforeend', `<div>${message.user}: ${message.content}</div>`);
            });
            chatLog.scrollTop = chatLog.scrollHeight;
        });

    chatMessageInput.focus();
    chatMessageInput.addEventListener('keyup', function (event) {
        if (event.keyCode === 13) {  // Enter key
            const message = chatMessageInput.value;
            fetch(`/rooms/${roomName}/send/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),  // Ensure CSRF token is included
                },
                body: JSON.stringify({
                    'message': message,
                    'room': roomName
                })
            }).then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') {
                        // Message sent successfully
                        chatSocket.send(JSON.stringify({
                            'message': message,
                            'room': roomName
                        }));
                        chatMessageInput.value = '';
                    } else {
                        console.error('Failed to send message');
                    }
                });
        }
    });

    // Function to get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
