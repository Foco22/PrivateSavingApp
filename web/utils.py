from django.urls import path
from web.views import views 

urlpatterns = [
    path('', views.Home, name='home'),
    path('', views.Details, name='details'),
    path('', views.Start, name='start'),
    path('', views.Tables, name='table'),
    path('', views.Chat, name='chat'),
    path('', views.inversions, name='inversions'),
    path('', views.Comportamiento, name='comportamiento'),

]