import json
import random
import requests
import time
from faker import Faker
from datetime import datetime

def get_us_land_coordinates(fake):
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
    log_messages = []
    for threshold in metric['thresholds']:
        if threshold['min'] <= value < threshold['max']:
            log_messages.append(f"{threshold['type']}: {threshold['message']} (Value: {value})")
    for condition in metric.get('log_conditions', []):
        if condition['condition'] == ">" and value > condition['value']:
            log_messages.append(f"{condition['type']}: {condition['message']} (Value: {value})")
    return log_messages if log_messages else ["No specific log message for this value"]

def initialize_host_geolocation(hosts_config, fake):
    geolocation_info = {}
    for host in hosts_config:
        hostname = host['hostname']
        if hostname not in geolocation_info:
            geolocation_info[hostname] = {
                "hostname": hostname,
                "ip_address": fake.ipv4_public(),  # Generate dynamic external IP address once
                **get_us_land_coordinates(fake)
            }
    return geolocation_info

def send_data(endpoint, token, data):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=data)
    return response.status_code

def generate_app_logs(app_log_config, geolocation_info, fake):
    logs = []
    for log_template in app_log_config:
        for hostname, info in geolocation_info.items():
            if random.randint(1, 100) <= log_template['frequency']:
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "log_message": log_template['message'],
                    "type": log_template['type'],
                    "hostname": info['hostname'],  # Ensure hostname is included
                    "event_code": log_template['event_code'],
                    "event_meaning": log_template['event_meaning']
                }
                for metadata in log_template['metadata']:
                    if metadata == "timestamp":
                        log_entry[metadata] = datetime.utcnow().isoformat() + "Z"
                    elif metadata == "hostname":
                        log_entry[metadata] = info['hostname']
                    elif metadata == "service_name":
                        log_entry[metadata] = fake.word()  # Simulate a service name
                    elif metadata == "error_code":
                        log_entry[metadata] = fake.random_int(min=100, max=599)  # Simulate an error code
                    elif metadata == "debug_info":
                        log_entry[metadata] = fake.sentence()  # Simulate debug information
                    elif metadata == "user_id":
                        log_entry[metadata] = fake.uuid4()  # Simulate a user ID
                    elif metadata == "session_id":
                        log_entry[metadata] = fake.uuid4()  # Simulate a session ID
                logs.append(log_entry)
    return logs

def main():
    config = read_config('config.json')
    http_endpoint = config['httpEndpoint']
    token = config['token']
    sleep_time = config['sleepTime']
    app_log_interval = config.get('appLogInterval', sleep_time)  # Default to sleep_time if not specified
    seed = config.get('seed', None)
    
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)
    
    geolocation_info = initialize_host_geolocation(config['hosts'], fake)
    last_app_log_time = time.time()

    while True:
        current_time = time.time()
        
        for host_info in config['hosts']:
            for metric in config['metrics']:
                metric_value = simulate_metric_value(metric)
                log_messages = determine_log_message(metric, metric_value)
                dynamic_info = geolocation_info[host_info['hostname']]

                for log_message in log_messages:
                    log_entry = {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "metric_name": metric['name'],
                        "value": metric_value,
                        "log_message": log_message,
                        "source_info": dynamic_info
                    }
                    for metadata in metric.get('log_metadata', []):
                        log_entry[metadata] = dynamic_info.get(metadata)
                    
                    print(f"Sending data: {log_entry}")
                    status_code = send_data(http_endpoint, token, log_entry)
                    print(f"Data sent with status code: {status_code}")

        # Generate and send application logs at the specified interval
        if current_time - last_app_log_time >= app_log_interval:
            app_logs = generate_app_logs(config.get('app_logs', []), geolocation_info, fake)
            for app_log in app_logs:
                print(f"Sending application log: {app_log}")
                status_code = send_data(http_endpoint, token, app_log)
                print(f"Application log sent with status code: {status_code}")
            last_app_log_time = current_time
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
