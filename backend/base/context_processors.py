from .models import Organiser
from datetime import datetime
import pytz

def clock_widget(request):
    casablanca_tz = pytz.timezone('Africa/Casablanca')
    now = datetime.now(casablanca_tz)
    
    return {
        'current_time': now.strftime('%H:%M:%S'),
        'current_date': now.strftime('%A, %B %d, %Y'),
        'weather_temp': '24°C',
        'weather_location': 'Casablanca'
    }

def site_title(request):
    return {
        'site_title': "Eventify",
    }

# from django.contrib import messages

# def header_data(request):
#     if not request.user.is_authenticated:
#         return {}
    
#     unread_messages_count = 0  # Default
#     if hasattr(request.user, 'received_messages'):
#         unread_messages_count = request.user.received_messages.filter(is_read=False).count()
    
#     system_messages = []
#     if not request.user.is_profile_complete():
#         system_messages.append("Please complete your profile")
    
#     django_messages = messages.get_messages(request)
#     for message in django_messages:
#         system_messages.append(str(message))
    
#     return {
#         'unread_messages_count': unread_messages_count,
#         'messages': system_messages,
#     }