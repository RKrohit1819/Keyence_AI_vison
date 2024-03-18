# ------------------CMT 2 Station 2-------------------#



# import re

import csv
import time
import struct
import logging
import requests
import json

# from typing import Dict, Union, Callable, Optional, List
# from datetime import date, datetime, timedelta
# from collections import OrderedDict

from snap7.types import Areas
from snap7.client import Client

logger = logging.getLogger(__name__)
import snap7
import codecs

unique = set()
# unique.clear()

# with open("serial_number.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Barcode"])

plc = snap7.client.Client()
plc.connect(
    "192.168.1.11", 0, 1
)  # IP address, rack, slot i.e 192.168.1.11 is IP address
# plc_info = plc.get_cpu_info()
# print(plc_info.ModuleTypeName)
# print(plc_info.Copyright)
print(plc.get_cpu_state())


# This function is for reading the boolean value from PLC
def readBool(db_number, start_offset, bit_offset):
    reading = plc.db_read(db_number, start_offset, 1)
    a = snap7.util.get_bool(reading, 0, bit_offset)
    # print(
    #     "DB Number: "
    #     + str(db_number)
    #     + " Bit: "
    #     + str(start_offset)
    #     + "."
    #     + str(bit_offset)
    #     + " Value: "
    #     + str(a)
    # )
    # print(
    #     f"DB Number {str(db_number)}, Bits {str(start_offset)}.{str(bit_offset)}, Value {str(a)} "
    # )
    return a


# This function is for writing the boolean value in certain memory address in PLC
def writeBool(db_number, start_offset, bit_offset, value):
    # Read the current byte from the specified area
    reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, 1)
    # Set the specified bit to the desired boolean value
    snap7.util.set_bool(reading, 0, bit_offset, value)
    # Write the modified byte back to the PLC
    plc.write_area(snap7.types.Areas.DB, db_number, start_offset, reading)

    print(f"DB Number: {db_number}, Bit: {start_offset}.{bit_offset}, Value: {value}")


def readMemory(start_address, length):
    reading = plc.read_area(snap7.types.Areas.MK, 0, start_address, length)
    value = struct.unpack(">f", reading)  # big-endian
    # print("Start Address: " + str(start_address) + " Value: " + str(value))
    print(f"Start Address {str(start_address)}, Value {str(value)}")


def read_int(db_number, start_offset):
    # Read 2 bytes (16 bits) from the specified area
    reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, 2)
    # Convert the raw data to an integer
    value_int = snap7.util.get_int(reading, 0)
    # print("DB Number:", db_number, "Start Offset:", start_offset, "Value:", value_int)
    print(f"DB Number: {db_number}, Start offset: {start_offset}, Value: {value_int}")
    return value_int


def read_char(db_number, start_offset):
    # Read 1 byte (8 bits) from the specified area
    reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, 1)
    # Convert the raw data to a character
    value_char = chr(reading[0])
    # print("DB Number:", db_number, "Start Offset:", start_offset, "Value:", value)
    print(f"DB Number: {db_number}, Start offset: {start_offset}, Value: {value_char}")
    return value_char


def read_char_list(db_number, start_offset, num_chars):
    # Initialize an empty list to store the characters
    bar_code = []
    # Read specified number of bytes (8 bits per byte) from the specified area
    for i in range(num_chars):
        reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset + i, 1)
        # Convert the raw data to a character and append to the list
        bar_code.append(chr(reading[0]))
        # char_list.append(reading[0])
    return bar_code


# def read_char_list(db_number, start_offset, num_chars):
#     # Read specified number of bytes (8 bits per byte) from the specified area
#     reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, num_chars)
#     if isinstance(reading, int):  # If reading is a single integer
#         return [chr(reading)]
#     else:  # If reading is a list of integers
#         return [chr(byte) for byte in reading]


def add_to_csv(filename, data):
    """
    Add data to a CSV file.

    Args:
    - filename: The name of the CSV file.
    - data: The data to be added. Should be a list where each element represents a row in the CSV.

    Returns:
    - True if the data was successfully added, False otherwise.
    """
    try:
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return True
    except Exception as e:
        print(f"An error occurred while adding data to the CSV file: {e}")
        return False


bool_to_read = readBool(7, 0, 2)
try:
    while True:
        bool_to_read = readBool(7, 0, 2)
        if bool_to_read:
            print(f"Bit 2 is {bool_to_read}")
            time.sleep(2)
            data = read_char_list(7, 2, 27)
            print(data)
            file = "CMT2_2_data.csv"
            sucess = add_to_csv(file, data)
            # send function
            # receive function
            if data[:4] == ["B", "2", "0", "5"]:
                # data = read_char_list(7, 2, 25)
                # print("Character List:", data)
                # if tuple(data) not in unique:
                # with open("serial_number.csv", "w", newline="") as csvfile:
                # writer = csv.writer(csvfile)
                # writer.writerow(["Barcode"])
                # writer.writerow(["".join(data)])
                # unique.add(tuple(data))
                time.sleep(2)
                writeBool(7, 0, 3, True)
                time.sleep(1)
                writeBool(7, 0, 3, False)
                # print(unique_barcodes)
                # else:
                #     writeBool(7, 0, 4, True)
                #     time.sleep(1)
                #     writeBool(7, 0, 4, False)
                #     # unique.clear()
            else:
                data = read_char_list(7, 2, 27)
                # print("Character List:", data)
                # writeBool(7, 0, 3, False)
                writeBool(7, 0, 4, True)
                time.sleep(1)
                writeBool(7, 0, 4, False)
except KeyboardInterrupt:
    print("Exiting due to KeyboardInterrupt")

# bool_to_read = readBool(7, 0, 2)
# try:

0





















#     while True:
#         bool_to_read = readBool(7, 0, 2)
#         # readBool(7, 0, 2)
#         if bool_to_read:
#             print(f"Bit 2 is {bool_to_read}")
#             time.sleep(2)
#             data = read_char_list(7, 2, 25)
#             print(data)
#             print(read_char(7, 2))
#             time.sleep(1)
#             # bar_code = [0]
# except KeyboardInterrupt:
#     print("Exiting due to KeyboardInterrupt")

# read_int(7, 2)
