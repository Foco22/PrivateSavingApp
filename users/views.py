from django.contrib.auth import get_user_model
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from users.serializers import UserSerializer
from users import services as user_services


template_name = '/django/web/templates/home.html'

def Home(request):
    return render(request, template_name)

