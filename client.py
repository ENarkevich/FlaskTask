import requests
import cv2
import numpy as np
import base64
import json
from INIT import CLIENT_FOLDER, SERV


requests.post(SERV, data=CLIENT_FOLDER+'pict.jpg')  
responce_parts = requests.get(SERV +'save_parts')
parts = responce_parts.json()

for i in range(1,5):
    pict = base64.b64decode(parts[str(i)])
    decoded = cv2.imdecode(np.frombuffer(pict, np.uint8), -1)
    cv2.imwrite(CLIENT_FOLDER + 'part' + str(i) +'.jpg', decoded)

files={}
for i in range(1,5):
    files[str(i)] = CLIENT_FOLDER +'part'+str(i) +'.jpg'

r = requests.post(SERV + 'concatenate', json=files)  

result = requests.get(SERV + 'result')

decoded = cv2.imdecode(np.frombuffer(result.content, np.uint8), -1)
cv2.imwrite(CLIENT_FOLDER + 'result_inv.jpg', decoded)


