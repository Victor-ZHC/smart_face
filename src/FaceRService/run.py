from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
from random import *
import base64

try:
    import face_detect
except:
    from . import face_detect
import random
import string
from PIL import Image
import io

import inspect, sys, os

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.join(os.path.dirname(currentdir), 'inference')
sys.path.insert(0, parentdir)

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
cors = CORS(app, resources={"/*": {"origins": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route("/upload", methods=['post', 'get'])
def upload():
    f = request.files['file']
    print("================f.filename: "+f.filename+"===============")
    if not os.path.isdir('./images'):
        os.mkdir('./images')
    path = './images/'+f.filename
    buffer = f.read()
    return jsonify(
        {'code': 0, 'url': 'http://localhost:5000/images/'+f.filename, 'faces': face_detect.detect(buffer, path)})


@app.route("/camera", methods=['post', 'get'])
def camera():
    photo = request.get_json()
    str = photo.get('photo')
    imgdata = base64.b64decode(str)

    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    filename = './images/'+salt+'.jpg'
    image = Image.open(io.BytesIO(imgdata))
    rgb_im = image.convert('RGB')
    rgb_im.save(filename)

    filer = open(filename, 'rb')
    face_detect.detect(filer.read(), filename)
    filer.close()
    return jsonify({'url': 'http://localhost:5000/images/'+salt+'.jpg'})


@app.route('/images/<filename>', methods=['GET'])
def show_photo(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open('./images/' + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

