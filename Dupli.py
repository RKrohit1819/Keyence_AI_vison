# ------------------CMT 2 Station 2-------------------#

import csv
import time
import struct
import logging
import requests
import json
MACHINE_ID="CMT2-2-001"

from snap7.types import Areas
from snap7.client import Client

logger = logging.getLogger(__name__)
import snap7
import codecs
unique = set()

plc = snap7.client.Client()
plc.connect("192.168.1.11", 0, 1)  # IP address, rack, slot i.e 192.168.1.11 is IP address
print(plc.get_cpu_state())

def readBool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset, 1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    return a

def writeBool(db_number, start_offset, bit_offset, value):
    reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, 1)
    snap7.util.set_bool(reading, 0, bit_offset, value)
    plc.write_area(snap7.types.Areas.DB, db_number, start_offset, reading)
    print(f"DB Number: {db_number}, Bit: {start_offset}.{bit_offset}, Value: {value}")

def read_char_list(db_number, start_offset, num_chars):
    bar_code = []
    for i in range(num_chars):
        reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset + i, 1)
        bar_code.append(chr(reading[0]))
    return bar_code

def add_to_csv(filename, data):
    try:
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return True
    except Exception as e:
        print(f"An error occurred while adding data to the CSV file: {e}")
        return False

def send_data_to_api(machine_id, data):
    api_url = "http://192.168.2.28/eol/module/autoprn/API/welding_cell_api/api.php?mac_id=machine1&dmc_code=nbhasf"  # Replace with your actual API endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "YOUR_API_KEY"  # Replace with your actual API key if needed
    }
    payload = {
        "machine_id": machine_id,
        "data": data
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Data sent to API. Response: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")python 
        return False

bool_to_read = readBool(7, 0, 2)
try:
    while True:
        bool_to_read = readBool(7, 0, 2)
        if bool_to_read:
            print(f"Bit 2 is {bool_to_read}")
            time.sleep(2)

            char_data = read_char_list(7, 2, 27)
            string_data = ''.join(char_data)
            print(string_data)

            # Check if string_data is unique
            if string_data not in unique:
                unique.add(string_data)

                file = "CMT2_2_data.csv"
                success_csv = add_to_csv(file, [string_data])

                # Send data to API
                success_api = send_data_to_api(MACHINE_ID, string_data)

                if string_data[:4] == "B205":
                    time.sleep(2)
                    writeBool(7, 0, 3, True)
                    time.sleep(1)
                    writeBool(7, 0, 3, False)
                else:
                    writeBool(7, 0, 4, True)
                    time.sleep(1)
                    writeBool(7, 0, 4, False)
            else:
                print("Duplicate string data. Ignoring...")
                # You can add additional handling if needed

except KeyboardInterrupt:
    print("Exiting due to KeyboardInterrupt")
