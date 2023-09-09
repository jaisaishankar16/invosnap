import json
import requests


url = 'https://ocr.asprise.com/api/v1/receipt'
image = "static/files/invoice2.jpg"


res = requests.post(url,
                   data={
                       'api_key':'TEST',
                       'recognizer':'auto',
                       'ref_no':'ocr_python_api'
                   },
                    files={
                        'file':open(image,'rb')
                    }
                   )

with open("response3.json",'w') as f:
    json.dump(json.loads(res.text),f)


with open("response3.json","r") as f:
    data = json.load(f)


print(data['receipts'][0])