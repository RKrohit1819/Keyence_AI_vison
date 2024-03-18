import socket


def read_data_from_ethernet_ip():
    # IP address and port of the PLC
    ip_address = "192.168.1.10"
    port = 9004  # Default port for Ethernet/IP

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Connect to the PLC
            sock.connect((ip_address, port))
            print("Connected to PLC")

            # Example command to read data
            command = b"\x4C\x00\x00\x00\x03\x00\x0A\x00\x00\x00\x00\x00\x00\x00\x00\xB2\x00\x00\x00\x00\x00\x00\x00"  # Example read command
            sock.send(command)

            # Receive response (adjust the buffer size according to your data size)
            response = sock.recv(1024)

            # Process response (you may need to parse the response based on your PLC's protocol)
            print("Response:", response)
        except Exception as e:
            print("Error:", e)
        finally:
            # Close the socket
            sock.close()


if __name__ == "__main__":
    read_data_from_ethernet_ip()
