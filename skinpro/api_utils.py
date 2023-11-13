import time
import requests


API_SKINCARE_URL = "https://api-inference.huggingface.co/models/varun1505/face-characteristics"
API_GENDER_URL = "https://api-inference.huggingface.co/models/Leilab/gender_class"
headers = {"Authorization": "Bearer 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"}

def query(file):
    
    with open(file, "rb") as f:
        data = f.read()
    skinres = requests.post(API_SKINCARE_URL, headers=headers, data=data)
    genres = requests.post(API_GENDER_URL, headers=headers, data=data)
    
    # preprosessing data
    gen_res_data = genres.json()
    skin_res_data = [{k: v for k, v in reversed(item.items())} for item in skinres.json()]
    gen_res = None
    
    if gen_res_data[0]["label"] == "men":
        gen_res = "man"
    else:
        gen_res = "woman"
        
    time.sleep(5)
    return {'skinres': skin_res_data,'genres': gen_res}