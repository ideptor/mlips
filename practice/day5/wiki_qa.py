
# pip install urllib3

import urllib3
import json

def get_key(filename):
    mod = int(input("decryption code:"))
    with open(filename, 'r') as f:
        key_str = f.read()
        
    r_key = ([chr(ord(i)-mod) for i in key_str])
    r_key = "".join(r_key)

    return r_key


def wiki_qa(question:str):

    access_key = get_key('key.txt')

    openApiURL = "http://aiopen.etri.re.kr:8000/WikiQA"
    question = question
    engine_type = "hybridqa"

    requestJson = {
    "access_key": access_key,
    "argument": {
        "question": question,
        "type": engine_type
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
    response = wiki_qa("대한민국의 수도는?")
    answer = response['return_object']['WiKiInfo']['AnswerInfo'][0]['answer']
    print("정답:", answer)
