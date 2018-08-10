import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS
from random import *
import os
import face_detect 

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
cors = CORS(app, resources={"/*": {"origins": "*"}})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")


@app.route("/upload", methods=['post', 'get'])
def upload():
    f = request.files['file']
    print("================f.filename: "+f.filename+"===============")
    if not os.path.isdir('./images'):
        os.mkdir('./images')
    path = './images/'+f.filename
    buffer = f.read()
    outf = open(path, 'wb')
    outf.write(buffer)
    outf.close()
    return jsonify({'code': 0, 'url': 'http://localhost:5000/images/'+f.filename, 'faces': face_detect.detect(buffer)})
    #return jsonify(face_detect.detect(f))


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
    app.run(debug=True)