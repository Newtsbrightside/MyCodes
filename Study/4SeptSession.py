import geocoder
from datetime import datetime
import pytz

'''API_TOKEN = '7b76467eb564d2'  # Your IPinfo token

g = geocoder.ipinfo('me', token=API_TOKEN)
print("Raw geocoder response:", g.json)  # Debug: show full response

if not g.ok or not g.latlng:
    print("Could not get location. Check your token or internet connection.")
else:
    lat, lng = g.latlng
    # Get timezone from the 'raw' field
    timezone_str = g.json.get('raw', {}).get('timezone', 'UTC')

    timezone = pytz.timezone(timezone_str)
    local_time = datetime.now(timezone)
    print(f"Your location: {g.city}, {g.country}")
    print(f"Timezone: {timezone_str}")
    print("Local time:", local_time.strftime('%Y-%m-%d %H:%M:%S'))

# Example: Get current weather for a city
from pyowm import OWM
owm = OWM('7b76467eb564d2')  # Replace with your OpenWeatherMap API key
mgr = owm.weather_manager()
observation = mgr.weather_at_place('London,GB')
weather = observation.weather
print(weather.status)  # e.g., 'Clouds'
timezone = pytz.timezone('Asia/Kolkata')
local_time = datetime.now(timezone)
print("Local time in Kolkata:", local_time.strftime('%Y-%m-%d %H:%M:%S'))'''

#Temperature Conversion System
'''def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32
def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9
while True:
    print("\nTemperature Conversion Menu:")
    print("1. Convert Celsius to Fahrenheit")
    print("2. Convert Fahrenheit to Celsius")
    print("3. Exit")
    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        current_temp_c = float(input("Enter temperature in Celsius: "))
        current_temp_f = celsius_to_fahrenheit(current_temp_c)
        print(f"Temperature in Fahrenheit: {current_temp_f:.2f}°F")
    elif choice == '2':
        current_temp_f = float(input("Enter temperature in Fahrenheit: "))
        current_temp_c = fahrenheit_to_celsius(current_temp_f)
        print(f"Temperature in Celsius: {current_temp_c:.2f}°C")
    elif choice == '3':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")'''

def main():
    temp = float(input("Enter current temperature: "))
    unit = input("Is this in Celsius (C) or Fahrenheit (F)? ").strip().upper()
    if unit == 'C':
        converted = (temp * 9/5) + 32
        print(f"{temp}°C is {converted:.2f}°F")
    elif unit == 'F':
        converted = (temp - 32) * 5/9
        print(f"{temp}°F is {converted:.2f}°C")
    else:
        print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")

main()

#Instagram Followers Counter
import instaloader
L = instaloader.Instaloader()
profile = input("Enter Instagram username: ")
profile = instaloader.Profile.from_username(L.context, profile)
print(f"{profile.username} has {profile.followers} followers.")
print(f"{profile.username} is following {profile.followees} accounts.")
print(f"{profile.username} has {profile.mediacount} posts.")
print(f"Bio: {profile.biography}")
print(f"Profile picture URL: {profile.profile_pic_url}")
print(f"External URL: {profile.external_url}")