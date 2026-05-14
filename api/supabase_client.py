from supabase import create_client, Client
from django.conf import settings

def get_supabase_client() -> Client:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    return create_client(url, key)