import csv
import time
import struct
import logging
import requests
import json
from snap7.types import Areas
from snap7.client import Client
MACHINE_ID = "CMT2-1-001"
logger = logging.getLogger(__name__)
plc = Client()
plc.connect("192.168.1.11", 0, 1)


def readBool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset, 1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    return a


def writeBool(db_number, start_offset, bit_offset, value):
    reading = plc.read_area(Areas.DB, db_number, start_offset, 1)
    snap7.util.set_bool(reading, 0, bit_offset, value)
    plc.write_area(Areas.DB, db_number, start_offset, reading)
    print(
        f"DB Number: {db_number}, Bit: {start_offset}.{bit_offset}, Value: {value}")


def read_char_list(db_number, start_offset, num_chars):
    bar_code = []
    for i in range(num_chars):
        reading = plc.read_area(Areas.DB, db_number, start_offset + i, 1)
        bar_code.append(chr(reading[0]))
    bar_code_str = "".join(bar_code)
    return bar_code_str


def add_to_csv(filename, data):
    try:
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return True
    except Exception as e:
        print(f"An error occurred while adding data to the CSV file: {e}")
        return False


def data_to_server():
    api_url = "http://192.168.2.28:8008/eol/module/autoprn/API/welding_cell_api/api.php"
    data_to_send = {"mac_id": MACHINE_ID, "dmc_code": read_char_list(7, 30, 27)}
    try:
        response = requests.post(api_url, json=data_to_send)
        response.raise_for_status()
        print("Data sent successfully!")
        api_response = response.json()
        print("API Response:", api_response)
        status = api_response.get("status", -1)
        if status == 1:
            time.sleep(2)
            writeBool(7, 1, 0, True)
            time.sleep(1)
            writeBool(7, 1, 0, False)
        else:
            writeBool(7, 1, 1, True)
            time.sleep(1)
            writeBool(7, 1, 1, False)
    except requests.exceptions.RequestException as e:
        print("Error sending or reading data from API:", e)


bool_to_read = readBool(7, 0, 7)
try:
    while True:
        bool_to_read = readBool(7, 0, 7)
        if bool_to_read:
            print(f"Bit 2 is {bool_to_read}")
            time.sleep(2)
            data = read_char_list(7, 30, 27)
            print(data)
            file = "CMT2_1_data.csv"
            success = add_to_csv(file, data)
            data_to_server()
except KeyboardInterrupt:
    print("Exiting due to KeyboardInterrupt")
