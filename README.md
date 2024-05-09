Metrics Simulation and Logging Script

This Python script simulates metrics within specified ranges and sends the corresponding log messages to a designated HTTP endpoint. It's designed to be fully configurable via a config.json file.

Configuration

Before running the script, ensure you have a config.json file in the same directory. This file should specify:

Metrics, their ranges, and corresponding log message thresholds.
The HTTP endpoint to send the data.
The authorization token.
The sleep time between data generations.
An example structure of config.json can be found in the previous explanations.

Dependencies

Install the required dependencies by running:

bash
Copy code
pip install -r requirements.txt
The requirements.txt file should contain:

Copy code
requests
Functions

read_config(config_path): Reads and parses the config.json file from the specified path and returns the configuration as a dictionary.
simulate_metric_value(metric): Simulates a random value for a given metric based on its defined range (min and max).
determine_log_message(metric, value): Determines the appropriate log message for a metric value based on predefined thresholds. This function checks if the value falls within specified ranges and selects the corresponding message.
send_data(endpoint, token, data): Sends the simulated data to the configured HTTP endpoint using the specified authorization token. It formats the data as JSON and includes necessary headers.
main(): The main function that orchestrates the entire process. It continuously generates metric values, determines corresponding log messages, and sends the data to the HTTP endpoint. It respects the sleep time set in the configuration to control the frequency of data generation and sending.
Usage

To run the script, use the following command:

bash
Copy code
python script_name.py
Replace script_name.py with the actual name of your script file. The script will continuously simulate metrics, generate log messages, and send them to the configured HTTP endpoint as per the sleep interval defined in config.json.

Customization

You can add more metrics or change existing ones by modifying the config.json file. Ensure each metric has a name, range, thresholds with min and max values, a type, a message, and a source.
