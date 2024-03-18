import snap7

# Define the IP addresses of the PLCs
plc1_ip = '192.168.0.1'
plc2_ip = '192.168.0.2'

# Connect to PLC1
plc1 = snap7.client.Client()
plc1.connect(plc1_ip, 0, 1)

# Connect to PLC2
plc2 = snap7.client.Client()
plc2.connect(plc2_ip, 0, 1)

# Read data from PLC1
data = plc1.read_area(snap7.types.S7AreaDB, 1, 0, 10)  # Read 10 bytes from DB1, starting from byte 0

# Write data to PLC2
plc2.write_area(snap7.types.S7AreaDB, 1, 0, data)  # Write data to DB1 of PLC2

# Disconnect from PLCs
plc1.disconnect()
plc2.disconnect()
