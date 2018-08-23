import cv2
from mtcnn.mtcnn import MTCNN
import numpy as np
import inspect, sys, os

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.join(os.path.dirname(currentdir), 'inference')
sys.path.insert(0, parentdir)

import apply_gender_mobilenet
import apply_age_mobilenet

detector = MTCNN()


def get_np_array_from_file_obj(buffer):
    '''converts a buffer from a tar file in np.array'''
    return np.asarray(
        bytearray(buffer)
        , dtype=np.uint8)


def print_text(image,pos,text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = pos
    fontScale = 1
    fontColor = (0,0,255)
    lineType = 2

    cv2.putText(image,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


def detect(buffer,path):
    
    image = cv2.imdecode(
        get_np_array_from_file_obj(buffer)
        , cv2.IMREAD_UNCHANGED )
    outimage = image.copy()
    #cv2.imwrite('testout.png', image)
    boxes = detector.detect_faces(image)
    ret=[]
    idx=1
    for box in boxes:
        face_position = box['box']
        print(face_position)
        crop = image[face_position[1]:face_position[1] + face_position[3],
                       face_position[0]: face_position[0] + face_position[2]]
        gender = apply_gender_mobilenet.infer_gender(crop)
        age = float(apply_age_mobilenet.infer_age(crop)[0][0])
        #print(age)
        ret.append({'box': face_position, 'gender': gender, 'age': age})
        simple_gender='F'
        if gender=="male":
            simple_gender="M"
        cv2.rectangle(outimage, (face_position[0], face_position[1]), 
            (face_position[0] + face_position[2], face_position[1] + face_position[3]), (255,0,0), 2)
        print_text(outimage,(face_position[0], face_position[1]),"%.0f %s" % (age,simple_gender))
        idx+=1        
        # cv2.imwrite('{0}.png'.format(file_path.split('.')[0] + '_' + 'face'), crop)
    cv2.imwrite(path,outimage)
    return ret


if __name__ == "__main__":
    f=open("images/1.jpg",'rb')
    buf=f.read()
    detect(buf,"out.png")

