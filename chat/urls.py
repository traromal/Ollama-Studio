from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('get_models/', views.get_models, name='get_models'),
    path('generate_response/', views.generate_response, name='generate_response'),
]