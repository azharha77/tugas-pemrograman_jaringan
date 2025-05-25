import socket
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
import json
import struct

from file_protocol import  FileProtocol
fp = FileProtocol()


def recvall(conn, n):
    data = b''
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(conn, addr):
    logging.warning(f"Handling client from {addr}")
    try:
        while True:
            raw_msglen = recvall(conn, 4)
            if not raw_msglen:
                break
            msglen = struct.unpack("!I", raw_msglen)[0]
            data = recvall(conn, msglen)
            if not data:
                break

            request = data.decode()
            logging.warning(f"Received request: {request}")
            try:
                result = fp.proses_string(request.strip())
            except Exception as e:
                logging.warning(f"Protocol processing error: {e}")
                result = json.dumps(dict(status='ERROR', data='Internal server error'))

            response_bytes = result.encode()
            response_length = struct.pack("!I", len(response_bytes))
            conn.sendall(response_length + response_bytes)

    except Exception as e:
        logging.warning(f"Exception handling client {addr}: {e}")
    finally:
        conn.close()

class ThreadPoolServer:
    def __init__(self,host='0.0.0.0',port=10000,max_workers=50):
        self.host = host
        self.port = port
        self.max_workers = max_workers
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        logging.warning(f"ThreadPoolServer listening on {(self.host, self.port)} with pool size {self.max_workers}")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                try:
                    conn, addr = self.sock.accept()
                    executor.submit(handle_client, conn, addr)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logging.warning(f"Server error: {e}")
        self.sock.close()


def main():
    if len(sys.argv) == 2:
        max_workers = int(sys.argv[1])
    else:
        max_workers = 50

    svr = ThreadPoolServer(host='172.16.16.101', port=10000, max_workers=max_workers)
    svr.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()

