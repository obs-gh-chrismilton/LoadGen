import json
import random
import requests
import time
from faker import Faker

fake = Faker()

# Read the configuration from the config.json file
def read_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

# Simulate a metric value based on its range
def simulate_metric_value(metric):
    return random.uniform(metric['range']['min'], metric['range']['max'])

# Determine the log message based on the value and thresholds
def determine_log_message(metric, value):
    for threshold in metric['thresholds']:
        if threshold['min'] <= value < threshold['max']:
            return f"{threshold['type']}: {threshold['message']} (Value: {value})"
    return "No specific log message for this value"

# Generate or retrieve consistent dynamic source information using faker
def initialize_metric_info(metric, config_hosts):
    hostname = choose_hostname(config_hosts) if config_hosts else fake.hostname()
    ip_address = fake.ipv4()
    dynamic_info = {
        "hostname": hostname,
        "ip_address": ip_address,
        "city": fake.city(),
        "state": fake.state(),
        "country": "United States",
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude())
    }
    return dynamic_info

# Choose a hostname from config or generate dynamically
def choose_hostname(config_hosts):
    return random.choice(config_hosts)

# Send data to the HTTP endpoint
def send_data(endpoint, token, data):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=data)
    return response.status_code

# Main function to generate and send data
def main():
    config = read_config('config.json')
    http_endpoint = config['httpEndpoint']
    token = config['token']
    sleep_time = config['sleepTime']
    config_hosts = config.get('hosts', [])
    
    # Initialize consistent information for each metric
    metric_info = {}
    for metric in config['metrics']:
        metric_info[metric['name']] = initialize_metric_info(metric, config_hosts)

    while True:
        for metric in config['metrics']:
            metric_value = simulate_metric_value(metric)
            log_message = determine_log_message(metric, metric_value)
            dynamic_info = metric_info[metric['name']]

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
