import requests​
url_image = "https://www.accede-web.com/wp-content/uploads/2015/06/justification-01.jpg"
endpoint = "https://projet-ocr-msp2.cognitiveservices.azure.com"
subscription_key = '6ca982264ca74eeaa7995357bd115af4'
ocr_url = endpoint + "vision/v3.0/ocr"
​
headers = {"Ocp-Apim-Subscription-Key": subscription_key,
           'Content-type': 'application/json'}
#params = {"includeTextDetails": True}
​
data = {"url" : url_image}
response = requests.post(url=ocr_url,
                         headers=headers,
                         json=data,
                         #params = params
                         )
​
print(response.text)
​
print(response.json()['regions'])
​
for index, line in enumerate(response.json()['regions'][0]['lines']):
    print(line['words'])
    for word in range(len(line['words'])):
        print(word)
        
for index, line in enumerate(response.json()['regions'][0]['lines']):
    print(line['words'])
    for word in range(len(line['words'])):
        print(word)        
​
