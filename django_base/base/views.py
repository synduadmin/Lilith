from allauth.account.views import LoginView, SignupView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from chatbot.urls import chatbot
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


class CustomLoginView(LoginView):
    template_name = 'account/custom_login.html'
    success_url = reverse_lazy('chatbot:chatbot')

    def get_success_url(self):
        return self.success_url

class CustomSignupView(SignupView):
    template_name = 'account/custom_signup.html'

    def get_success_url(self):
        # Redirect users to a custom page after login
        return redirect('account_login')