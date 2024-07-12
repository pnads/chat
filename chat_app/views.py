import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Message


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirect to a 'home' view after login
    else:
        form = AuthenticationForm()
    return render(request, "chat_app/login.html", {"form": form})


@login_required
def home(request):
    return render(request, "chat_app/home.html")


@login_required
def room(request, room):
    return render(request, "chat_app/room.html", {"room": room})


@login_required
def send_message(request, room):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message_content = data.get("message", "").strip()

            if not message_content:
                return JsonResponse(
                    {"status": "error", "message": "Message content cannot be empty."},
                    status=400,
                )

            # Create Message object
            Message.objects.create(
                room=room,
                content=message_content,
                user=request.user,
            )

            return JsonResponse(
                {"status": "ok", "message": "Message sent successfully."}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data."}, status=400
            )

    return HttpResponseBadRequest("Invalid request method.")


@login_required
def fetch_messages(request, room):
    try:
        messages = Message.objects.filter(room=room).order_by("timestamp")[:50]
        message_data = [
            {"user": msg.user.username, "content": msg.content} for msg in messages
        ]
        return JsonResponse(message_data, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
