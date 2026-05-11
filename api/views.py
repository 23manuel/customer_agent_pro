from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_service import get_nova_response
import json

from django.shortcuts import render # Add this import

def chat_page(request):
    return render(request, 'chat.html')

# Keep your existing chat_endpoint code below this...
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_service import get_nova_response
import json

@csrf_exempt
def chat_endpoint(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("query", "")
            
            # 1. Retrieve existing memory from Django Session
            chat_history = request.session.get('chat_history', [])
            
            # 2. Get AI response using the history
            response_text = get_nova_response(user_query, chat_history)
            
            # 3. Update memory with the new exchange
            chat_history.append({"role": "user", "content": user_query})
            chat_history.append({"role": "assistant", "content": response_text})
            
            # 4. Keep only the last 10 messages so the payload doesn't get too heavy
            request.session['chat_history'] = chat_history[-10:]
            
            # Dev Move: Tell Django we modified the list so it actually saves it!
            request.session.modified = True 
            
            return JsonResponse({"status": "success", "response": response_text})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"message": "Send a POST query to talk to Nova-Pilot."}, status=405)