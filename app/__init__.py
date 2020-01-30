from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

import pandas as pd
import jsonify
import os

from .dataset import Data

app = Flask(__name__)

bootstrap = Bootstrap(app)

SECRET_KEY = 'development'
app.config.from_object(__name__)

frame = dataset.Data()
data = frame.parseData(frame.readData())


@app.route('/', methods=['POST','GET'])
def getData():

    tempData = data
    slideDic = {}
    slideVals = frame.getSlideValues(data)
    dic = {'sent': 1, 'delivered': 1, 'delRate': 1, 'openRate': 1, 'clickRate': 1}

    export = request.args.get('export')

    if export == '1':
        x = tempData.to_csv('FilteredEmailData.csv')

    if request.method == "POST":
        
        dic = dic.fromkeys(dic, 0)

        selected = request.form.getlist('check')

        for i in selected:
            if i in dic.keys():
                dic[i] = 1

        slideDic['slide1'] = (request.form["slide11"], request.form["slide12"])
        slideDic['slide2'] = (request.form["slide21"], request.form["slide22"])
        slideDic['slide3'] = (request.form["slide31"], request.form["slide32"])
        slideDic['slide4'] = (request.form["slide41"], request.form["slide42"])
        slideDic['slide5'] = (request.form["slide51"], request.form["slide52"])

        tempData = frame.editCells(data, slideDic)    

    print(data.columns)
    return render_template('index.html', data=tempData, dic=dic, slideDic=slideDic, slideVals=slideVals, prevDate="99")



