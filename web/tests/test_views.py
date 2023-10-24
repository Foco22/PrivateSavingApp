from django.contrib.messages import get_messages
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.test.client import Client
import pytest

from web.views.views import HomeView
from users.models import User
from users import services as user_services
from users.models import Plan

