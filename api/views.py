from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import Conversation
from .ai_service import get_nova_response, create_account, compare_prices
from .supabase_client import get_supabase_client
import json
import uuid

# views.py
def chat_page(request):
    # Changed from 'api/chat.html' to just 'chat.html'
    return render(request, 'chat.html')

# 2. KEEP THIS: This handles the AI logic
@csrf_exempt # Move this here to fix the 403 error!
def chat_api(request):
    if request.method == "POST":
        try:
            content_type = request.content_type or ''
            if content_type.startswith('application/json'):
                data = json.loads(request.body)
                user_message = data.get("message") or data.get("query")
                session_id = data.get("session_id", str(uuid.uuid4()))
            else:
                user_message = request.POST.get("message") or request.POST.get("query")
                session_id = request.POST.get("session_id", str(uuid.uuid4()))

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Check for special commands
            if "create account" in user_message.lower():
                response = create_account(user_message)
            elif "compare price" in user_message.lower() or "price comparison" in user_message.lower():
                response = compare_prices(user_message)
            else:
                # Get conversation history for context
                history = Conversation.objects.filter(session_id=session_id).order_by('-timestamp')[:5]
                history_messages = []
                for conv in reversed(history):
                    history_messages.extend([
                        {"role": "user", "content": conv.user_message},
                        {"role": "assistant", "content": conv.ai_response}
                    ])
                
                response = get_nova_response(user_message, history_messages)

            # Log conversation to Supabase and local DB for redundancy
            try:
                supabase = get_supabase_client()
                supabase.table('conversations').insert({
                    'session_id': session_id,
                    'user_message': user_message,
                    'ai_response': response,
                    'timestamp': timezone.now().isoformat()
                }).execute()
            except Exception as err:
                print(f"Supabase log failed: {err}")

            Conversation.objects.create(
                session_id=session_id,
                user_message=user_message,
                ai_response=response
            )

            return JsonResponse({"response": response, "session_id": session_id})

        except Exception as e:
            print(f"View Error: {e}")
            return JsonResponse({"response": "Server side gbege. Check logs."}, status=500)
            
    return JsonResponse({"error": "Invalid method"}, status=405)