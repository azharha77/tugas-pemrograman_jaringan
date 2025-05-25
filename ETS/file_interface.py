import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.makedirs('files/', exist_ok=True)
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def upload(self,params=[]):
        try:
            filename = params[0]
            filedata_b64 = params[1]
            if (filename == '' or filedata_b64 == ''):
                return None
            fp = open(f"{filename}",'wb')
            fp.write(base64.b64decode(filedata_b64))
            return dict(status='OK',data=filename)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def delete(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            os.remove(filename)
            return dict(status='OK',data=filename)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
