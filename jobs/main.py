import gpxpy
import os
import uuid
import time
import json
import random
import requests
from datetime import datetime, timedelta
from confluent_kafka import Producer
from geopy.distance import geodesic

# ========================== Configuration ==========================
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_key_here')
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENAIRQUALITY_API_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")

VEHICLE_TOPIC = "vehicle_data"
WEATHER_TOPIC = "weather_data"
FAILURE_TOPIC = "failure_data"
DEVICE_ID = "motorbike-001"

GPX_FILE = "data/2022-12-02 12_12_41.gpx"
MYTRACKS_NAMESPACE = "http://mytracks.stichling.info/myTracksGPX/1/0"
CENTRAL_POINT = (36.70828195217619, -4.465170324163806)  # Traffic office
RADIUS_KM = 1.0

SUSPENSION_REASONS = [
    'Failure to stop',
    'Yield sign ignored',
    'Amber light not respected',
    'Pedestrian crossing not respected',
    'Wrong way taken'
]

# ========================== Kafka Setup ==========================
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
last_weather_fetch_time = None
last_weather_data = {}
last_air_quality_data = {}
last_suspension_time = None

# ========================== GPX Reading ==========================
def get_extension_value(extensions, tag, namespace):
    for ext in extensions:
        if ext.tag.endswith(tag) and ext.text:
            return ext.text
    return None

def read_gpx_file(file_path):
    points = []
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    speed = get_extension_value(point.extensions, 'speed', MYTRACKS_NAMESPACE)
                    length = get_extension_value(point.extensions, 'length', MYTRACKS_NAMESPACE)
                    points.append({
                        'latitude': point.latitude,
                        'longitude': point.longitude,
                        'elevation': point.elevation,
                        'time': point.time.isoformat() if point.time else None,
                        'speed': float(speed) if speed else None,
                        'length': float(length) if length else None
                    })
    return points

# ========================== Weather & Failure Simulation ==========================
def fetch_weather_data(lat, lon, timestamp):
    global last_weather_fetch_time, last_weather_data, last_air_quality_data

    current_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if not last_weather_fetch_time or (current_time - last_weather_fetch_time >= timedelta(minutes=10)):
        last_weather_fetch_time = current_time

        weather = requests.get(f"{OPENWEATHER_API_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric")
        air = requests.get(f"{OPENAIRQUALITY_API_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}")

        if weather.status_code == 200:
            data = weather.json()
            last_weather_data = {
                "temperature": data["main"]["temp"],
                "weatherCondition": data["weather"][0]["main"],
                "windSpeed": data["wind"]["speed"],
                "humidity": data["main"]["humidity"]
            }

        if air.status_code == 200:
            air_data = air.json()
            last_air_quality_data = {
                "airQualityIndex": air_data["list"][0]["main"]["aqi"]
            }

    return {
        **last_weather_data,
        **last_air_quality_data,
        "id": DEVICE_ID,
        "timestamp": timestamp
    }

def is_within_radius(point, center=CENTRAL_POINT, radius=RADIUS_KM):
    return geodesic(point, center).km <= radius

def simulate_failure(location, timestamp):
    global last_suspension_time
    current_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if is_within_radius((location["latitude"], location["longitude"])) and \
        (last_suspension_time is None or (current_time - last_suspension_time) >= timedelta(minutes=5)):

        last_suspension_time = current_time
        return {
            "id": str(uuid.uuid4()),
            "deviceID": DEVICE_ID,
            "incidentId": str(uuid.uuid4()),
            "type": "Test Drive Suspension",
            "timestamp": timestamp,
            "location": location,
            "description": f"{random.randint(1, 5)} suspensions: {random.choice(SUSPENSION_REASONS)}",
            "num_failures": random.randint(1, 10)
        }
    return None

# ========================== Send to Kafka ==========================
def send(topic, data):
    producer.produce(topic, key=str(uuid.uuid4()), value=json.dumps(data).encode("utf-8"))
    producer.flush()

# ========================== Main ==========================
def main():
    gpx_points = read_gpx_file(GPX_FILE)
    for point in gpx_points:
        timestamp = point["time"]
        location = {"latitude": point["latitude"], "longitude": point["longitude"]}

        # Send vehicle data
        vehicle_record = {
            **point,
            "id": str(uuid.uuid4()),
            "deviceID": DEVICE_ID,
            "timestamp": timestamp
        }
        send(VEHICLE_TOPIC, vehicle_record)

        # Send weather
        weather_data = fetch_weather_data(point["latitude"], point["longitude"], timestamp)
        if weather_data:
            send(WEATHER_TOPIC, weather_data)

        # Send simulated failure if applicable
        failure = simulate_failure(location, timestamp)
        if failure:
            send(FAILURE_TOPIC, failure)

        print(f"Data sent at {timestamp}")
        time.sleep(1)

if __name__ == "__main__":
    main()
