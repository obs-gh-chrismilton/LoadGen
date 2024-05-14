### README

# LoadGen Script

## Overview
The LoadGen script is designed to generate simulated metrics and logs for the purpose of loading data into the Observe platform. It is intended for use by the Observe technical teams to simulate environments for labs or customer demonstrations, providing valuable insights into system performance and behavior.

## Features
- **Dynamic Metric and Log Generation**: Generates a variety of metrics and logs based on customizable configurations.
- **Geolocation Information**: Each host includes dynamic geolocation information.
- **Reproducibility with Seed Configuration**: Ensures consistent data generation using a specified seed value.
- **Separate Interval for Application Logs**: Allows for a distinct interval for generating application logs independently of metric logs.
- **Enhanced Log Metadata**: Includes additional metadata such as `user_id`, `session_id`, `service_name`, `error_code`, and `debug_info`.

## Installation

### Prerequisites
- Python 3.x
- Required Python libraries listed in `requirements.txt`

### Install Required Libraries
Use the following command to install the necessary libraries:
```bash
pip install -r requirements.txt
```

## Configuration
The script uses a `config.json` file to define metrics, hosts, and log settings. Below is an example configuration:

### Metrics Configuration
- **name**: The name of the metric.
- **range**: The minimum and maximum values for the metric.
- **thresholds**: Defines thresholds with types (info, warning, error) and messages.
- **log_conditions**: Custom conditions to generate additional log messages.
- **log_metadata**: Metadata to be included in log messages (timestamp, hostname, ip_address).

### Hosts Configuration
- **hostname**: The name of the host.

### Application Logs Configuration
- **type**: The type of log (info, warning, error, debug).
- **message**: The log message.
- **frequency**: The likelihood (in percentage) of this log being generated.
- **event_code**: The event code for the log.
- **event_meaning**: The meaning of the event code.
- **metadata**: Additional metadata to include in the log (timestamp, hostname, service_name, user_id, session_id).

### Other Configuration Parameters
- **httpEndpoint**: The HTTP endpoint to which the data will be sent.
- **token**: The token used for authorization.
- **sleepTime**: The interval (in seconds) between each data generation cycle.
- **appLogInterval**: The interval (in seconds) between application log generations.
- **seed**: A seed value to ensure reproducibility in data generation.

## How to Use the Script
1. Ensure Python 3.x is installed on your system.
2. Install the required Python libraries using the `requirements.txt` file.
3. Customize the `config.json` file to define your metrics, hosts, and log settings.
4. Run the script with the following command:
   ```bash
   python LoadGen.py
   ```

## How It Works
### Functions
- **get_us_land_coordinates**: Generates latitude and longitude coordinates guaranteed to be on land in the US.
- **read_config**: Reads the configuration from the `config.json` file.
- **simulate_metric_value**: Simulates a metric value based on its defined range.
- **determine_log_message**: Determines the log message based on the metric value and defined thresholds and conditions.
- **initialize_host_geolocation**: Initializes and returns geolocation information for each host.
- **send_data**: Sends the generated data to the specified HTTP endpoint.
- **generate_app_logs**: Generates application logs based on the defined configuration.

### Main Loop
- Reads the configuration from `config.json`.
- Initializes geolocation information for each host.
- Generates and sends metric data at regular intervals.
- Generates and sends application logs at specified intervals, cycling through the hosts to ensure each log entry is associated with a specific hostname and IP address.

## Customization
- **Metrics**: Customize the metrics to be generated, including their ranges, thresholds, and log conditions.
- **Hosts**: Define the hosts that will be simulated, including their hostnames.
- **Application Logs**: Configure the types of application logs to be generated, including their messages, frequencies, event codes, meanings, and metadata.
- **Intervals**: Adjust the `sleepTime` and `appLogInterval` to control how often data is generated and sent.
- **Seed**: Set the `seed` parameter to ensure reproducibility in data generation.

## Example Customization
Here are examples of how you might customize the `config.json` to generate specific metrics and logs:

### Custom Metrics
- **network_latency**: A metric to simulate network latency, with defined thresholds and log conditions.

### Custom Hosts
- **SERVER-001**, **SERVER-002**: Hostnames for the simulated servers.

### Custom Application Logs
- **High memory usage warning**: An application log entry to be generated with a certain frequency, including metadata such as `user_id` and `session_id`.

### Seed Configuration
- **Seed**: The `seed` parameter ensures reproducibility by making the generated data consistent across multiple runs.
