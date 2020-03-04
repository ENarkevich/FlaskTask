from flask import Flask, request, Response, make_response, json
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
        return Response(status=404, headers={"message":"File not found"}) 
    image = cv2.imread(f["path_file"])
    parts_number = f["parts_number"]
    responce_data={}
    parts, responce_data["ratio_y"], responce_data["ratio_x"] = crop_file(image, parts_number)
    # if number of parts is unreal
    if (parts==None):
        return Response(status=409, headers={"message":"Impossible to cropp to this number of parts"})
    # encode data to json 
    for i in range(parts_number):
        responce_data[str(i)] = base64.b64encode(cv2.imencode('.jpg', parts[i])[1]).decode() 
    return make_response(json.dumps(responce_data)) 
    
def crop_file(image, number_parts):
    height, width, _ = image.shape
    parts = []
    ratio = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    # search for X-proportion
    ratio_x = [i for i in ratio if number_parts%i==0]     
    ratio_x = ratio_x[-1]
    # Y-proportion for cropp
    ratio_y = int(number_parts/ratio_x)
    if (height>width and ratio_x>ratio_y):  
        ratio_x, ratio_y = ratio_y, ratio_x
    # if number of parts is unreal
    if(ratio_x>width or ratio_y>height):
        return None, None, None
    # shift for new points
    x_offset, y_offset = int(width/ratio_x), int(height/ratio_y)  
    x1, y1 = 0, 0     
    x2, y2 = x_offset, y_offset   
    # cropp picture
    for i in range(ratio_y):
        for j in range(ratio_x): 
            parts.append(image[y1:y2,x1:x2])  
            x1 = x1 + x_offset
            x2 = x2 + x_offset
            if (j==ratio_x-1):
                x2 =  width
        y1 = y1 + y_offset
        y2 = y2 + y_offset
        if(i==ratio_y-1):
            y2 = height
        x1, x2 = 0, x_offset  
    return parts, ratio_y, ratio_x

@app.route('/concatenate', methods=['POST'])
def concatenate_parts():
    f = request.json
    ratio_x=f["ratio_x"]
    ratio_y=f["ratio_y"]
    parts=[]
    # decode from json 
    for i in range(ratio_x*ratio_y):
        pict = base64.b64decode(f[str(i)])
        parts.append(cv2.imdecode(np.frombuffer(pict, dtype=np.uint8), flags=1))
    all_picture=np.array([])
    # concatenate horizontal lines to picture
    for i in range(ratio_y):
        frame = parts.pop()
        # concatenate parts to horizontal lines
        for j in range(ratio_x-1):
            frame = np.concatenate((parts.pop(), frame), axis=1)
        if (i>0):
            all_picture = np.concatenate((frame, all_picture), axis=0)
        else:
            all_picture = frame
    all_picture = cv2.bitwise_not(all_picture)
    responce_data={}
    # encode data to json
    responce_data["result"] = base64.b64encode(cv2.imencode('.jpg', all_picture)[1]).decode() 
    return make_response(json.dumps(responce_data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
