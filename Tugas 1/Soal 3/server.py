import sys
import socket
import logging

logging.basicConfig(level=logging.INFO)

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(10)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1 )

    # Bind the socket to the port
    server_address = ('0.0.0.0', 32444) #--> gunakan 0.0.0.0 agar binding ke seluruh ip yang tersedia

    logging.info(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    #1 = backlog, merupakan jumlah dari koneksi yang belum teraccept/dilayani yang bisa ditampung, diluar jumlah
    #             tsb, koneks akan direfuse
    while True:
        # Wait for a connection
        logging.info("waiting for a connection")
        connection, client_address = sock.accept()
        logging.info(f"connection from {client_address}")
        # Receive the data in small chunks and retransmit it
        try:
            file_data = bytearray()
            while True:
                data = connection.recv(32)
                if not data:
                    break
                file_data.extend(data)
                logging.info(f"received chunk of size {len(data)}")

            with open('received_file.txt', 'wb') as f:
                f.write(file_data)

            # Send it back to client
            logging.info("sending back the received file")
            connection.sendall(file_data)
        finally:
            # Clean up the connection
            connection.close()
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
finally:
    logging.info('closing')
    sock.close()
