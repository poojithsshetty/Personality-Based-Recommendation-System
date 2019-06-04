from flask import Flask, render_template, request
import requests
import urllib
import urllib.request
import json
import requests
import os
import zipfile
from urllib.request import urlopen
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
import shutil
import pandas as pd
import urllib.request
from lxml import html
import gzip
import io
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import csv
import datetime

app = Flask(__name__)

@app.route('/result', methods=['POST'])
def result():
    hotels = request.form['hotel']
    usernames = request.form['username']
    opens = request.form['open']
    cons = request.form['cons']
    extras = request.form['extra']
    neuros = request.form['neuro']
    agrees = request.form['agree']
    data = {
                "Inputs": {
                        "input1":
                        [
                            {
                                    'username': usernames,   
                                    'open': opens,   
                                    'cons': cons,   
                                    'extra': extras, 
                                    'agree': agrees,   
                                    'neuro': neuros,   
                            }
                        ],
                },
                "GlobalParameters":  {
                }
            }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/c2f8dc5126ac4024b08690eda8426a56/services/e61d656160c3434c85e2c75ffed09010/execute?api-version=2.0&format=swagger'
    api_key = 'Y7nS1x6ohC+l5Udka1g1h1+RBHjNpYeEFUFJXDhpzI+J/R7aBl/D5qHXWYLjqmtOVa1uF3oM4z4ZSa0W3tb9DA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
    except urllib.error.HTTPError as error:
        result = "error"
    result = json.loads(result.decode("utf-8"))
    s = result['Results']['output1'][0]['Assignments']
    kmean = int(s)

    data = {
            "Inputs": {
                    "input1":
                    [
                        {
                                'taObject': hotels,   
                                'kmean': kmean,   
                        }
                    ],
            },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/c2f8dc5126ac4024b08690eda8426a56/services/0efed30347d448769f4235796c8fd62e/execute?api-version=2.0&format=swagger'
    api_key = 'M0WLn8LOvsQ/l96Sooumss7RuExRHZAbxpWFIBeSCSXfjjQ4ZPpXebSVAkRWT2qJrGT66z2Piwnm2Arx2E4oWw==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
    except urllib.error.HTTPError as error:
        result = "error"
    result = json.loads(result.decode("utf-8"))
    s = result['Results']['output1'][0]['Scored Labels']
    s = float(s)
    if s > 0 and s <6:
        return render_template('home.html',delaytime = s)
    else:
        return render_template('home.html',delaytime = "no data available")
    #json_object = response.json
    #r = json_object['output1']['ArrDelayMinutes']
    

@app.route('/')
def index():
       
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)