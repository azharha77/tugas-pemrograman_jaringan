import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""



class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
    def proses_string(self,string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        try:
            request = json.loads(string_datamasuk)
            command = request.get("command", "").lower()
    
            if command == "upload":
                params = [request.get("filename"), request.get("content")]
            elif command in ["get", "delete"]:
                params = [request.get("filename")]
            else:  # LIST
                params = []
    
            logging.warning(f"memproses request: {command}")
            cl = getattr(self.file,command)(params)
            return json.dumps(cl)
        except Exception:
            return json.dumps(dict(status='ERROR',data='request tidak dikenali'))
