from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "chat"

urlpatterns = [
    path("rooms/<str:room>/", views.room, name="room"),
    path("rooms/<str:room>/send/", views.send_message, name="send_message"),
    path("rooms/<str:room>/fetch/", views.fetch_messages, name="fetch_messages"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
