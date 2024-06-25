from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "chat"

urlpatterns = [
    path("<str:room_name>/", views.room, name="room"),
    path("send_message/<str:room_name>/", views.send_message, name="send_message"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
