# views.py
from django.views.generic import CreateView, View, TemplateView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import RegisterForm
from .models import Token
from .utils import generate_uuid
from .services import send_verify_link
from django.utils import timezone
from datetime import timedelta





class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = generate_uuid()
        email = user.email
        Token.objects.create(user=user, token=token)

        path = reverse("verify")
        link = self.request.build_absolute_uri(f"{path}?token={token}")

        send_verify_link(email, link)

        messages.success(self.request, "Account created! Check your email to verify.")
        return super().form_valid(form)





class VerifyView(View):
    def get(self, request):
        token = request.GET.get("token")

        if not token:
            messages.error(request, "Token missing")
            return redirect("login")

        try:
            test_obj = Token.objects.get(token=token)
        except Token.DoesNotExist:
            messages.error(request, "Invalid token")
            return redirect("login")

        if timezone.now() - test_obj.created_at > timedelta(hours=24):
            messages.error(request, "Token expired")
            return redirect("register")

        if test_obj.is_used:
            messages.warning(request, "Token already used")
            return redirect("login")

        user = test_obj.user
        user.is_active = True
        user.save()

        test_obj.is_used = True
        test_obj.save()

        messages.success(request, "Account verified successfully!")
        return redirect("login")

class Home(TemplateView):
    template_name = "home.html"