import helper
import requests
from flask import Flask, request, Response, render_template, redirect 
import json
import time
# from requests import get, post
import urllib
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def get_image():
    # Get and analyze the image from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        url = req["image"]
        text = get_text_from_url(url)

        text_to_db = '\n'.join(text)
        res_data = helper.add_to_list(url, text_to_db)
        if res_data is None:
            response = Response("{'error': 'text not added - " + text_to_db + "'}", status=400 , mimetype='application/json')
            return response

        return render_template("result.html", text=text) 



    # return render_template("/index.html")
    # return render_template("index.html")

    # req_data = request.get_json()
    # text = req_data[text]

    # # Add comment to the list
    # res_data = helper.add_to_list(text)

    # # Return error if comment not added
    # if res_data is None:
    #     response = Response("{'error': 'text not added - " + text + "'}", status=400 , mimetype='application/json')
    #     return response

    # # Return response
    # response = Response(json.dumps(res_data), mimetype='application/json')



def get_text_from_url(url_image):
    print(os.environ['COMPUTER_VISION_ENDPOINT'])
    missing_env = False
    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        print("From Azure Cogntivie Service, retrieve your endpoint and subscription key.")
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
        missing_env = True

    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("From Azure Cogntivie Service, retrieve your endpoint and subscription key.")
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
        missing_env = True

    if missing_env:
        print("**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    # subscription_key = '6ca982264ca74eeaa7995357bd115af4'
    # endpoint = 'https://projet-ocr-msp2.cognitiveservices.azure.com'

    text_recognition_url = endpoint + "/vision/v3.0/read/analyze"

    # Set image_url to the URL of an image that you want to recognize.
    image_url = url_image

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, json=data)
    response.raise_for_status()

    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        
        print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False


    polygons = []
    if ("analyzeResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

    # Display the image and overlay it with the extracted text.
    image = Image.open(BytesIO(requests.get(image_url).content))
    fig = plt.figure()
    ax = plt.imshow(image)
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i+1])
                    for i in range(0, len(polygon[0]), 2)]
        text = polygon[1]
        patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
    # plt.show()
    fig.savefig('static/result.png', bbox_inches='tight')

    # Making the text response
    text = []
    for line in analysis['analyzeResult']['readResults'][0]['lines']:
        text.append(line['text'])

    return text

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')