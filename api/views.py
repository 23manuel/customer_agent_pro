from django.shortcuts import render # Add this import!
from django.http import JsonResponse
from .ai_service import get_nova_response
import json

# views.py
def chat_page(request):
    # Changed from 'api/chat.html' to just 'chat.html'
    return render(request, 'chat.html')

# 2. KEEP THIS: This handles the AI logic
def chat_api(request):
    if request.method == "POST":
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                user_message = data.get("message")
            else:
                user_message = request.POST.get("message")

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            ai_response = get_nova_response(user_message)
            return JsonResponse({"response": ai_response})

        except Exception as e:
            print(f"View Error: {e}")
            return JsonResponse({"response": "Server side gbege. Check logs."}, status=500)
            
    return JsonResponse({"error": "Invalid method"}, status=405)