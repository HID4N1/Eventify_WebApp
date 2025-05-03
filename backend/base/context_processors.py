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