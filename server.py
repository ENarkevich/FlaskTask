from flask import Flask, request, redirect, url_for, Response, make_response, json
import cv2
import numpy as np
import base64
from INIT import SERVER_FOLDER

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_file():
    f = request.data
    image = cv2.imread(f.decode("utf-8"))
    cv2.imwrite(SERVER_FOLDER + "img.jpg", image) 
    return redirect(url_for('crop_file'))

@app.route('/crop')
def crop_file():
    image = cv2.imread(SERVER_FOLDER + "img.jpg")
    height = image.shape[0]
    width = image.shape[1]
    center = [int(height/2), int(width/2)]
    impart1 = image[0:center[0], 0:center[1]]
    impart2 = image[0:center[0], center[1]:width]
    impart3 = image[center[0]:height, 0:center[1]]
    impart4 = image[center[0]:height, center[1]:width]

    cv2.imwrite(SERVER_FOLDER + "1.jpg", impart1)
    cv2.imwrite(SERVER_FOLDER + "2.jpg", impart2)
    cv2.imwrite(SERVER_FOLDER + "3.jpg", impart3)
    cv2.imwrite(SERVER_FOLDER + "4.jpg", impart4)
    return  Response(status=200)

@app.route('/save_parts', methods=['GET'])
def save_parts():
    data = {}
    for i in range(1,5):
        with open(SERVER_FOLDER + str(i)+'.jpg','rb') as fil:
            byte = fil.read()
        encoded = base64.encodebytes(byte) 
        data[str(i)] = encoded.decode('ascii') 
    rr =  json.dumps(data)
    return make_response(rr) 

@app.route('/concatenate', methods=['POST'])
def concatenate_parts():
    f = request.json
    impart1 = cv2.imread(f["1"])
    impart2 = cv2.imread(f["2"])
    impart3 = cv2.imread(f["3"])
    impart4 = cv2.imread(f["4"])
    
    top = np.concatenate((impart1, impart2), axis=1)
    bottom = np.concatenate((impart3, impart4), axis=1)
    all = cv2.bitwise_not(np.concatenate((top, bottom), axis=0))

    cv2.imwrite(SERVER_FOLDER + "res.jpg", all)
    return  Response(status=200)

@app.route('/result', methods=['GET'])
def get_result():
    with open(SERVER_FOLDER + 'res.jpg','rb') as fil:
        byte = fil.read()
    return make_response(byte)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
