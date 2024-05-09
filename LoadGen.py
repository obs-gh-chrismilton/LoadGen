import json
import random
import requests
import time

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
    
    while True:
        for metric in config['metrics']:
            metric_value = simulate_metric_value(metric)
            log_message = determine_log_message(metric, metric_value)
            data = {
                "metric_name": metric['name'],
                "value": metric_value,
                "log_message": log_message,
                "source": metric['source']
            }
            print(f"Sending data: {data}")
            status_code = send_data(http_endpoint, token, data)
            print(f"Data sent with status code: {status_code}")
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
