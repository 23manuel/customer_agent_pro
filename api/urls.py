from django.urls import path
from .views import chat_api, chat_page

urlpatterns = [
    path('chat/', chat_api, name='chat'),      # Path for the logic
    path('dashboard/', chat_page, name='dashboard'), # Path for the HTML
]