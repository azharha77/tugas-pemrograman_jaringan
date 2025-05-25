import socket
import json
import base64
import logging
import os
import struct

server_address=('172.16.16.101',10000)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        encoded = command_str.encode()
        msg = struct.pack("!I", len(encoded)) + encoded
        sock.sendall(msg)

        # Read 4-byte length prefix
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            raise ValueError("Failed to receive message length")
        msglen = struct.unpack("!I", raw_msglen)[0]

        full_msg = recvall(sock, msglen)
        return json.loads(full_msg.decode())

    except Exception as e:
        print(f"Error during communication: {e}")
        return False
    finally:
        sock.close()

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def remote_list():
    payload = json.dumps({"command": "LIST"})
    hasil = send_command(payload)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    payload = json.dumps({
        "command": "GET",
        "filename": filename
    })
    hasil = send_command(payload)
    if (hasil and hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    if not os.path.exists(filepath):
        print("File tidak ditemukan.")
        return False
    filename = os.path.basename(filepath)
    fp = open(filepath,'rb')
    encoded = base64.b64encode(fp.read()).decode()
    payload = json.dumps({
        "command": "UPLOAD",
        "filename": filename,
        "content": encoded
    })
    hasil = send_command(payload)
    if (hasil and hasil['status']=='OK'):
        return True
    else:
        print("Gagal")
        return False

def remote_delete(filename=""):
    payload = json.dumps({
        "command": "DELETE",
        "filename": filename
    })
    hasil = send_command(payload)
    if (hasil and hasil['status']=='OK'):
        return True
    else:
        print("Gagal")
        return False
