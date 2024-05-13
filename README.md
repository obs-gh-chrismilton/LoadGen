# Load Generator Script README

## Overview
This Load Generator Script is specifically designed to generate logs and metric data for loading simulated data into the Observe platform. Designed for use by Observe technical teams to prove out or simulate environments for labs or customer demonstrations. The script's behavior is configured through a `config.json` file, which defines the metrics to be simulated, the hosts involved, and other operational parameters.

## Installation
To use this script, you need Python installed on your system. Follow these steps to set up:

1. **Ensure Python is Installed**: The script is compatible with Python 3. Make sure it is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).

2. **Install Required Libraries**: The script depends on the `requests` and `Faker` libraries, which are listed in the `requirements.txt` file. Install them using pip:
   ```
   pip install -r requirements.txt
   ```

## How the Script Works
The script operates by looping through a set of predefined metrics and hosts, generating data based on the configurations specified in `config.json`. For each host, it simulates the values for each metric, applies the appropriate log messages based on thresholds, and sends this data to the configured HTTP endpoint.

- **Metric Simulation**: For each metric, the script generates a value within the specified range and then determines the corresponding log message based on threshold evaluations.

- **Data Sending**: The generated data, along with geolocation details for each host, is sent to the specified HTTP endpoint using the token for authentication.

- **Continuous Operation**: The script runs in a continuous loop, with a configurable sleep time between iterations to control the data sending frequency.

## Customizing the `config.json` File
The `config.json` file is central to how the script operates. Here’s how you can customize it for different scenarios:

### Metrics
- **Add or Modify Metrics**: You can add new metrics or modify existing ones by adjusting the `name`, `range`, and `thresholds` in the `metrics` array. This allows you to simulate different system behaviors or monitor additional parameters.

### Hosts
- **Configure Hosts**: The `hosts` section allows you to define which hosts are involved in the simulation. Each host should have a `hostname` and an `ip_address`. You can add more hosts or change existing ones to simulate data from different sources.

### Operational Settings
- **HTTP Endpoint and Token**: The `httpEndpoint` and `token` are used to configure where and how the data is sent. Update these to match your data ingestion endpoint and authentication method.

- **Sleep Time**: The `sleepTime` controls how often the script generates and sends data. Adjust this value to increase or decrease the frequency of data transmission.

## Scenarios for Customization
- **Load Testing**: Increase the frequency and range of metric values to simulate high load conditions and observe how your monitoring setup handles intense data flow.

- **Fault Simulation**: Set thresholds to generate more critical errors and observe how your system responds to simulated faults.


By adjusting these settings and parameters in `config.json`, you can tailor the simulation to fit a wide range of testing and monitoring needs, making the script a versatile tool for demonstrating and testing the capabilities of the Observe platform.
