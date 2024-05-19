from keras.models import load_model
from keras.preprocessing import image
import cv2 as cv
import numpy as np
from keras.layers import Conv2D
from flask import Flask, request, jsonify, render_template
import os

dic = {0: 'Normal', 1: 'Doubtful', 2: 'Mild', 3: 'Moderate', 4: 'Severe'}

app = Flask(__name__)

class CustomConv2D(Conv2D):
    def __init__(self, filters, **kwargs):
        super(CustomConv2D, self).__init__(filters, **kwargs)

    def call(self, inputs):
        outputs = super(CustomConv2D, self).call(inputs)
        return outputs


img_size = 256


model = load_model('model.h5', custom_objects={'CustomConv2D': CustomConv2D})
model.make_predict_function()

def predict_label(img_path):
    img = cv.imread(img_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    resized = cv.resize(gray, (img_size, img_size))
    i = image.img_to_array(resized) / 255.0
    i = np.reshape(i, (1, img_size, img_size, 1))
    
    p = model.predict(i)
    p_class = np.argmax(p, axis=1)
    return dic[p_class[0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part in the request", 400
    f = request.files['file']
    if f.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join('static', f.filename)
    f.save(file_path)
    label = predict_label(file_path)
    if (label == 'Normal'):
        label = 'Your osteoarthritis Xray is Normal, No need to worry!'
    elif (label == 'Doubtful'):
        label = 'It is doubtful to say anything, try consulting doctor!'
    elif (label == 'Mild'):
        label = 'Found mild chances of osteoarthritis, please consult a doctor!'
    elif (label == 'Moderate'):
        label = 'Found moderate chances of osteoarthritis, please consult a doctor!'
    else:
        label = 'Found huge chances of osteoarthritis, please consult a doctor immediately!'
    return render_template('index.html', label=label, img_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)