
import urllib3
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def get_key(filename):
    mod = int(input("decryption code:"))
    with open(filename, 'r') as f:
        key_str = f.read()
        
    r_key = ([chr(ord(i)-mod) for i in key_str])
    r_key = "".join(r_key)

    return r_key


# aihub 에서  응답받은 데이터를 기반으로 그림 그리기
def draw_status(image_file, status_list, confidence_threshold=0.6):

    im = Image.open(image_file)

    plt.imshow(im)

    ax = plt.gca()

    for status in status_list:
        confidence = float(status['confidence'])
        if confidence < confidence_threshold:
            continue
        x = float(status['x'])
        y = float(status['y'])
        width = float(status['width'])
        height = float(status['height'])
        text = f"{status['class']}:{confidence:.2f}"


        rect = patches.Rectangle((x,y),
                     width,
                     height,
                     linewidth=2,
                     edgecolor='blue',
                     fill = False)

        ax.add_patch(rect)
        ax.text(x+5,y+20, text, c="blue")

    plt.show()

# aihub 의 API 호출
def human_status(filename:str):
    
    #-*- coding:utf-8 -*-
    import urllib3
    import json
    import base64
    openApiURL = "http://aiopen.etri.re.kr:8000/HumanStatus"
    accessKey = get_key("key.txt")
    imageFilePath = filename
    file_type = "png"

    file = open(imageFilePath, "rb")
    imageContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "type": file_type,
            "file": imageContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    response_json = json.loads(response.data)
    
    print("-------------------")
    print("[responseCode] " + str(response.status))
    print("[responBody]")
    print(json.dumps(response_json, indent=2))
    print("-------------------")
    
    if response_json['result'] == -1:
        return None
    
    return response_json


if __name__ == "__main__":
    image_file = "sample1.png"
    status_list = human_status(image_file)['return_object'][0]["data"][1:]
    draw_status(image_file, status_list, confidence_threshold=0.7)
