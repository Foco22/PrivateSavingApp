from django.urls import path
from web.views import views 

urlpatterns = [
    path('', views.Start, name='show_start'),
    path('details/', views.Details, name='show_details'),
    path('tables/', views.Tables, name='show_tables'),
    path('home/', views.Home, name='home'),
    path('clasification/', views.Clasification, name='clasification'),
    path('Chat/', views.Chat, name='chat'),
    path('inversions/', views.inversions, name='inversions'),
    path('comportamiento/', views.Comportamiento, name='comportamiento'),
]

