# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Simon Fang <sifang@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Import section
from netmiko import ConnectHandler
import yaml
import subprocess
from dotenv import load_dotenv
import os
import datetime

# Load environment variables
load_dotenv()

# Global variables
filename_devices = 'devices.yaml'
SERVER_USERNAME = os.getenv('SERVER_USERNAME')
SERVER_HOST = os.getenv("SERVER_HOST")
DST_FOLDER = os.getenv("DST_FOLDER")
DEVICE_PASSWORD = os.getenv('DEVICE_PASSWORD')

# Helper functions
## Get a list of device from a yaml file
def get_devices_from_file(filename_devices):
    with open(filename_devices, 'r') as file:
        try:
            devices = yaml.safe_load(os.path.expandvars(file.read()))
        except yaml.YAMLError as exc:
            print(exc)
    return devices

## Send the config file to a server
def send_file_to_server(src_file_path, SERVER_USERNAME, SERVER_HOST, dst_file_path):
    response = subprocess.run(["scp", src_file_path, f'{SERVER_USERNAME}@{SERVER_HOST}:{dst_file_path}'])
    return response


# Main function
def main():
    # Obtain the list of devices
    devices = get_devices_from_file(filename_devices)

    # Loop through the list of devices
    for device in devices['devices']:
        # Connect with the device
        conn = ConnectHandler(**device)

        # Obtain the running config
        running_config = conn.send_command("show running-config")

        # Temporarily save the running config
        config_file_path = f'/tmp/{device["host"]}.txt'
        with open(config_file_path, 'w') as file:
            file.write(running_config)

        # Send the running config file to the server
        response = send_file_to_server(config_file_path, SERVER_USERNAME, SERVER_HOST, f"{DST_FOLDER}/{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{device['host']}.txt")
        print(response)


if __name__ == "__main__":
    main()