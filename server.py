from flask import Flask, request, redirect, url_for, Response, make_response, json
import cv2
import numpy as np
import base64
import os 
from config import SERVER_FOLDER

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_file():
    f = request.json
    if (not(os.path.exists(f["path_file"]))):
        return Response(status=404)
    image = cv2.imread(f["path_file"])
    parts_number = f["parts_number"]
    crop_result = crop_file(image, parts_number)
    parts = crop_result["parts"]
    responce_data={}
    for i in range(parts_number):
        responce_data[str(i)] = base64.b64encode(cv2.imencode('.jpg', parts[i])[1]).decode() 
    responce_data["ratio_y"] = crop_result["ratio_y"]
    responce_data["ratio_x"] = crop_result["ratio_x"]
    return make_response(json.dumps(responce_data)) 
    
def crop_file(image, number_parts):
    height, width = image.shape[0], image.shape[1]
    imparts = []
    ratio = [1, 2, 3, 5, 7, 11]
    for i in ratio:
        if number_parts%i==0:
            ratio_x = i
    ratio_y = int(number_parts/ratio_x)
    if (height>width and ratio_x>ratio_y):
        ratio_x, ratio_y = ratio_y, ratio_x
        
    x_offset, y_offset = int(width/ratio_x), int(height/ratio_y)
    y1, y2, = 0, y_offset
    x1, x2 = 0, x_offset
    for i in range(1,ratio_y+1):
        for j in range(1,ratio_x+1): 
            imparts.append(image[y1:y2,x1:x2])
            x1 = x1 + x_offset
            x2 = x2 + x_offset
            if (j==ratio_x):
                x2 =  width
        y1 = y1 + y_offset
        y2 = y2 + y_offset
        if(i==ratio_y):
            y2 = height
        x1, x2 = 0, x_offset
    return {"parts":imparts, "ratio_y":ratio_y, "ratio_x":ratio_x}

@app.route('/concatenate', methods=['POST'])
def concatenate_parts():
    f = request.json
    ratio_x=f["ratio_x"]
    ratio_y=f["ratio_y"]
    impart=[]
    for i in range(ratio_x*ratio_y):
        pict = base64.b64decode(f[str(i)])
        impart.append(cv2.imdecode(np.frombuffer(pict, dtype=np.uint8), flags=1))
    axis_X = []
    all_picture=np.array([])
    for i in range(ratio_y):
        first = impart.pop()
        for j in range(ratio_x-1):
            top = np.concatenate((impart.pop(), first), axis=1)
        if (i>0):
            all_picture = np.concatenate((top, all_picture), axis=0)
        else:
            all_picture = top

    all_picture = cv2.bitwise_not(all_picture)
    responce_data={}
    responce_data["result"] = base64.b64encode(cv2.imencode('.jpg', all_picture)[1]).decode() 
    return make_response(json.dumps(responce_data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
