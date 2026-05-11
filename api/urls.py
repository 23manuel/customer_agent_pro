from django.urls import path
from .views import chat_endpoint, chat_page

urlpatterns = [
    path('chat/', chat_endpoint, name='chat'),      # Path for the logic
    path('dashboard/', chat_page, name='dashboard'), # Path for the HTML
]