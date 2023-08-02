# maps.py
import googlemaps
import os
from gtts import gTTS

def get_distance_and_duration(api_key, origin, destination):
    gmaps = googlemaps.Client(key=api_key)
    try:
        # Request directions using Google Maps API
        directions_result = gmaps.directions(origin, destination, mode="driving")

        # Extract distance and duration from the response
        distance = directions_result[0]['legs'][0]['distance']['value']  # in meters
        duration = directions_result[0]['legs'][0]['duration']['text']

        return distance, duration
    except Exception as e:
        print("Error:", e)
        return None, None

def calculate_taxi_charge(distance_in_meters, initial_charge, charge_per_km):
    distance_in_km = distance_in_meters / 1000
    total_charge = initial_charge + (charge_per_km * distance_in_km)
    return total_charge

def get_taxi_charge(api_key, initial_charge=2.6, charge_per_km=1):
    origin = input("Enter Orgin: ")
    destination = input("Enter Destination: ")

    distance_in_meters, duration = get_distance_and_duration(api_key, origin, destination)

    if distance_in_meters and duration:
        # Calculate taxi charge
        total_charge = calculate_taxi_charge(distance_in_meters, initial_charge, charge_per_km)

        # Convert the distance to a more human-readable format
        distance_in_km = distance_in_meters / 1000
        distance_readable = f"{distance_in_km:.2f} kilometers"

        # Generate the message and play it out loud
        message = f"The distance between {origin} and {destination} is {distance_readable}. " \
                  f"The estimated taxi charge is £{total_charge:.2f}. The journey will take approximately {duration}."

        speech = gTTS(text=message, lang='en')
        speech.save("output.mp3")
        os.system("afplay -r 1.7 output.mp3")
    else:
        print("Unable to retrieve the distance and duration.")
