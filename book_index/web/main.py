# coding: utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import Flask, render_template, request, json
from flask_cors import CORS

import numpy as np
import io

from PIL import Image
import json

from ml.procs.txt.level_model_handle import LevelModelHandeler
from ml.procs.img.page_text_check import PageTxtChecker

from utils.utils import *


txt_model_handle = LevelModelHandeler()
img_model_chekcer = PageTxtChecker()

#-------------------------------------------------
# app 설정
app = Flask(__name__, static_url_path='/static')

cors = CORS(app)

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='[[',
    variable_end_string=']]',
    comment_start_string='{#',
    comment_end_string='#}'
))
app.jinja_options = jinja_options

@app.route("/predict_text", methods=['GET','POST'])
def predict_text():
    if request.method == 'POST':

        page_text = json.loads(request.data.decode('utf8'))
        sentence = page_text['page_text']

        try:
            output = txt_model_handle.predict(sentence)[0]
            level = round(output, 2)

        except TypeError:
            level = '정보가 더 필요합니다.'

        result = {
            'level' : level
        }

    return result, 200

@app.route("/analyze_img", methods=['GET', 'POST'])
def analyze_img():

    if request.method == 'POST':

        f = request.files['file']
        img = Image.open(f.stream)
        img = np.array(img)

        drawed_img = img_model_chekcer.draw_txt_bboxes(img)

        # convert numpy array to PIL Image
        img = Image.fromarray(drawed_img.astype('uint8'))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return img_byte_arr, 200

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)