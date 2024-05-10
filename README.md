Metrics Simulation and Dynamic Data Generation Script

This Python script simulates metrics within specified ranges and sends the corresponding log messages along with dynamic geolocation and network data to a designated HTTP endpoint. It's fully configurable via a config.json file.
Configuration

Before running the script, ensure you have a config.json file in the same directory. This file should specify:
Metrics, their ranges, and corresponding log message thresholds.
Optional pre-defined hostnames or dynamic generation of host information.
The HTTP endpoint to send the data.
The authorization token.
The sleep time between data generations.

An example structure of config.json is provided in the subsequent sections.
Dependencies

Install the required dependencies by running:
pip install -r requirements.txt

Functions
read_config(config_path): Reads and parses the config.json file from the specified path and returns the configuration as a dictionary. This is where all initial settings are loaded.
simulate_metric_value(metric): Simulates a random value for a given metric based on its defined range (min and max). This function ensures variability in metric values for realism.
determine_log_message(metric, value): Determines the appropriate log message for a metric value based on predefined thresholds. This function checks if the value falls within specified ranges and selects the corresponding message.
initialize_metric_info(metric, config_hosts): Initializes the hostname, IP address, and geolocation data for each metric. If config_hosts is provided, it selects a hostname from this list; otherwise, it generates one dynamically using Faker.
choose_hostname(config_hosts): Selects a hostname from the provided config_hosts array. If the array is empty, dynamic generation is triggered.
send_data(endpoint, token, data): Sends the simulated data to the configured HTTP endpoint using the specified authorization token. It formats the data as JSON and includes necessary headers.
main(): The main function orchestrates the entire process. It initializes metric information, continuously generates metric values, determines corresponding log messages, and sends the data to the HTTP endpoint, respecting the sleep time set in the configuration.

Customization via config.json

Metrics Definition: Define each metric's name, range, and log message thresholds. Example for one metric:
"metrics": [ { "name": "Metric1", "range": {"min": 10, "max": 50}, "thresholds": [{"min": 10, "max": 20, "type": "Error", "message": "Value is between 10 and 20 for Metric1"}, {"min": 21, "max": 30, "type": "Success", "message": "Value is between 21 and 30 for Metric1"}, {"min": 31, "max": 40, "type": "Status", "message": "Value is between 31 and 40 for Metric1"} ], "source": "Node1" } ]

Hostnames: Specify a list of hostnames to be used for metrics, or leave it empty to generate hostnames dynamically. Example:
"hosts": ["host1.example.com", "host2.example.com"]
Or for dynamic generation:
"hosts": []
HTTP Endpoint and Token: Set the httpEndpoint and token for data submission. Example:
"httpEndpoint": "http://example.com/upload", "token": "your_secure_token_here"

Sleep Time: Configure how frequently (in seconds) data is generated and sent. Example:
"sleepTime": 1



