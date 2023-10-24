from django.shortcuts import rende
from .models import Recipe
from bank.models import DataBanks
from rest_framework import viewsets
from .serializers import RecipeSerializer


class bank_view_set(viewsets.ModelViewSet):
    # define queryset
    queryset = DataBanks.objects.all()
    serializer_class = RecipeSerializer