from django.urls import path
from .views import RegisterView, VerifyView, Home
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/", VerifyView.as_view(), name="verify"),
    path("login/", LoginView.as_view(template_name='login.html'), name="login"),
    path("home/", Home.as_view(), name="home"),
]