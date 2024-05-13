import json
import random
import requests
import time
from faker import Faker

fake = Faker()

def get_us_land_coordinates():
    while True:
        latitude, longitude, place_name, country_code, timezone = fake.location_on_land(coords_only=False)
        if country_code == 'US':
            city_state = place_name.split(', ')
            city = city_state[0] if len(city_state) > 0 else ""
            state = city_state[1] if len(city_state) > 1 else ""
            return {
                "latitude": latitude,
                "longitude": longitude,
                "city": city,
                "state": state,
                "country": country_code
            }

def read_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def simulate_metric_value(metric):
    return random.uniform(metric['range']['min'], metric['range']['max'])

def determine_log_message(metric, value):
    for threshold in metric['thresholds']:
        if threshold['min'] <= value < threshold['max']:
            return f"{threshold['type']}: {threshold['message']} (Value: {value})"
    return "No specific log message for this value"

def initialize_host_geolocation(hosts_config):
    geolocation_info = {}
    for host in hosts_config:
        hostname = host['hostname']
        if hostname not in geolocation_info:
            geolocation_info[hostname] = {
                **host,
                **get_us_land_coordinates()
            }
    return geolocation_info

def send_data(endpoint, token, data):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=data)
    return response.status_code

def main():
    config = read_config('config.json')
    http_endpoint = config['httpEndpoint']
    token = config['token']
    sleep_time = config['sleepTime']
    
    geolocation_info = initialize_host_geolocation(config['hosts'])

    while True:
        for host_info in config['hosts']:
            for metric in config['metrics']:
                metric_value = simulate_metric_value(metric)
                log_message = determine_log_message(metric, metric_value)

                dynamic_info = {
                    "hostname": host_info['hostname'],
                    "ip_address": host_info['ip_address'],
                    **geolocation_info[host_info['hostname']]
                }

                data = {
                    "metric_name": metric['name'],
                    "value": metric_value,
                    "log_message": log_message,
                    "source_info": dynamic_info
                }
                print(f"Sending data: {data}")
                status_code = send_data(http_endpoint, token, data)
                print(f"Data sent with status code: {status_code}")
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
