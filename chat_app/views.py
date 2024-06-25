from django.http import JsonResponse
from django.shortcuts import render


def room(request, room_name):
    return render(request, "chat_app/room.html", {"room_name": room_name})


def send_message(request, room_name):
    message = request.POST.get("message")
    # Logic to handle saving and sending the message
    return JsonResponse({"message": message})
