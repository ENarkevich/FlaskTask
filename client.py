import requests
import cv2
import numpy as np
import base64
import json
from config import CLIENT_FOLDER, SERV

if __name__ == "__main__":
    parts_number = 6
    request_data = {}
    #request fot cropp
    request_data["parts_number"] = parts_number
    request_data["path_file"] = f'{CLIENT_FOLDER}pict.jpg'
    responce_parts = requests.post(SERV, json=request_data)  
    if (responce_parts.status_code==200):
        parts = responce_parts.json()
        # request for concatenate 
        for_concatenate=parts
        from_conc = requests.post(f'{SERV}concatenate', json=for_concatenate)
        from_conc = from_conc.json()
        pict = base64.b64decode(from_conc["result"])
        decoded = cv2.imdecode(np.frombuffer(pict, dtype=np.uint8), flags=1)
        cv2.imwrite(f'{CLIENT_FOLDER}result.jpg', decoded)

