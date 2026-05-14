from django.core.management.base import BaseCommand
from api.supabase_client import get_supabase_client
from django.utils import timezone
from datetime import timedelta
import json

class Command(BaseCommand):
    help = 'Retrain Nova based on conversation data'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)
        supabase = get_supabase_client()
        response = supabase.table('conversations').select('*').gte('timestamp', week_ago.isoformat()).execute()
        conversations = response.data
        
        if not conversations:
            self.stdout.write('No new conversations to retrain on.')
            return
        
        # Analyze conversations for patterns
        user_messages = [conv['user_message'] for conv in conversations]
        ai_responses = [conv['ai_response'] for conv in conversations]
        
        # Simple analysis: find common topics
        topics = {}
        for msg in user_messages:
            if 'account' in msg.lower():
                topics['account'] = topics.get('account', 0) + 1
            if 'price' in msg.lower() or 'cost' in msg.lower():
                topics['pricing'] = topics.get('pricing', 0) + 1
            if 'help' in msg.lower() or 'support' in msg.lower():
                topics['support'] = topics.get('support', 0) + 1
        
        # Generate improved system prompt based on data
        improved_prompt = f"""You are Nova-Pilot, a highly skilled Client Support Specialist for Nova Pay.
        Based on recent interactions, focus areas include:
        - Account creation: {topics.get('account', 0)} mentions
        - Pricing questions: {topics.get('pricing', 0)} mentions  
        - General support: {topics.get('support', 0)} mentions
        
        Be conversational, helpful, and remember context. Provide personalized responses."""
        
        # Save improved prompt to a file or database
        with open('improved_system_prompt.json', 'w') as f:
            json.dump({'prompt': improved_prompt, 'topics': topics}, f)
        
        self.stdout.write(f'Retrained on {len(conversations)} conversations. Improved prompt saved.')