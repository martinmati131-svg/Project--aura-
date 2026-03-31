import requests

# Configuration
API_KEY = "YOUR_OPENWEATHER_API_KEY"
CITY = "Juja,KE"
THRESHOLD_MM = 10.0  # Alert if more than 10mm of rain is predicted

def check_rain_forecast():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    # Check the next 24 hours (8 periods of 3-hour forecasts)
    for forecast in response['list'][:8]:
        rain_val = forecast.get('rain', {}).get('3h', 0)
        time = forecast.get('dt_txt')
        
        if rain_val > THRESHOLD_MM:
            print(f"⚠️ ALERT: Heavy rain ({rain_val}mm) predicted at {time}")
            return True, rain_val
    return False, 0

is_heavy, amount = check_rain_forecast()

if is_heavy:
    print(f"Action Required: Delay fertilizer application to prevent leaching.")
else:
    print("Weather Clear: Safe to proceed with nutrient roadmap.")
