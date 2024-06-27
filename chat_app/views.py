import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def room(request, room):
    return render(request, "chat_app/room.html", {"room": room})


@login_required
def send_message(request, room):
    if request.method == "POST":
        data = json.loads(request.body)
        message_content = data.get("message", "")

        # Create Message object
        Message.objects.create(
            room=room,
            content=message_content,
            user=request.user,
        )

        return JsonResponse({"status": "ok", "message": "Message sent successfully."})
    return JsonResponse({"status": "error", "message": "Failed to send message."})


@login_required
def fetch_messages(request, room):
    messages = Message.objects.filter(room=room).order_by("timestamp")[:50]
    message_data = [
        {"user": msg.user.username, "content": msg.content} for msg in messages
    ]
    return JsonResponse(message_data, safe=False)
