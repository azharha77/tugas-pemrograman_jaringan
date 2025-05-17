import sys
import socket
import logging

#set basic logging
logging.basicConfig(level=logging.INFO)

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.16.16.101', 32444)
    logging.info(f"connecting to {server_address}")
    sock.connect(server_address)

    # Send data
    try:
        with open('sent_file.txt', 'rb') as f:
            file = f.read()
        sock.sendall(file)
        logging.info(f"sent a file of size {len(file)}")

        sock.shutdown(socket.SHUT_WR)

        with open('received_back_file.txt', 'wb') as f:
                while True:
                    data = sock.recv(16)
                    if not data:
                        break
                    f.write(data)
                    logging.info(f"received chunk of size {len(data)}")

    except FileNotFoundError:
        logging.info("File not found.")
        exit(1)
        
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
finally:
    logging.info("closing")
    sock.close()
