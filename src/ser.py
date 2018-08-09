from flask import Flask,jsonify,request,send_file

from PIL import Image
from io import BytesIO 
import face_detect

app = Flask(__name__)
idx=0

images=[]

bad_response={'status':1,'description':'The file is empty'}


def get_face(mfile):
    global idx
    faces=face_detect.detect(mfile)
    im = Image.open(mfile)
    area = (100, 100, 300, 300)
    images.append(im.crop(area))
    idx+=1

    return faces#{'status':0,'description':'ok','number_of_faces':1,'id':idx-1} 

@app.route('/')
def index():
    return "Hello, World!"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg','jpeg','png']

@app.route('/facedetect/detect',methods=['POST'])
def upload():
    print("upload")
    print(request.files)
    bad_response['status']=1
    if 'file' not in request.files:
        return jsonify(bad_response),201
    file = request.files['file']
    #dummy = request.form
    #print(dummy)
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        bad_response['status']=2
        return jsonify(bad_response),201
    print(file.filename)
    if file and allowed_file(file.filename):
        return jsonify(get_face(file))
    else:
        bad_response['status']=3
        return jsonify(bad_response),201

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/facedetect/getimg/<imageid>',methods=['GET'])
def getimg(imageid):
    id_image=int(imageid)
    if(0<=id_image<len(images)):
        return serve_pil_image(images[id_image])

if __name__ == '__main__':
    app.run(debug=True)