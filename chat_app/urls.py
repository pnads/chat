from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = "chat"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("rooms/<str:room>/", views.room, name="room"),
    path("rooms/<str:room>/send/", views.send_message, name="send_message"),
    path("rooms/<str:room>/fetch/", views.fetch_messages, name="fetch_messages"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
