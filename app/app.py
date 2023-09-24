from flask import Flask, render_template, send_file
from flask import request
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image
import os
import numpy as np
import io

app = Flask(__name__)


output_path = "static/images/"

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'No image file provided', 400
    file = request.files['image'].read()
    input_img = np.array(Image.open(io.BytesIO(file)))
    output_img = remove(input_img)
    img = Image.fromarray(output_img)
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()
    return send_file(io.BytesIO(byte_arr), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
