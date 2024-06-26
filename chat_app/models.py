from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    room = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username}: {self.content}"
