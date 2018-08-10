import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
inference_path = os.path.join(currentdir,"inference")
sys.path.insert(0,inference_path) 

import cv2
from mtcnn.mtcnn import MTCNN
import numpy as np
import apply_gender_mobilenet, apply_age_mobilenet


def get_np_array_from_file_obj(buffer):
    '''converts a buffer from a tar file in np.array'''
    return np.asarray(
        bytearray(buffer)
        , dtype=np.uint8)


def detect(buffer):
    detector = MTCNN()
    image = cv2.imdecode(
        get_np_array_from_file_obj(buffer)
        , cv2.IMREAD_UNCHANGED )
    cv2.imwrite('testout.png', image)
    boxes = detector.detect_faces(image)
    ret=[]
    for box in boxes:
        face_position = box['box']
        print(face_position)
        crop = image[face_position[1]:face_position[1] + face_position[3],
                       face_position[0]: face_position[0] + face_position[2]]
        gender=apply_gender_mobilenet.infer_gender(crop)
        age=float(apply_age_mobilenet.infer_age(crop)[0][0])
        print(age)
        ret.append({'box': face_position, 'gender': gender, 'age': age})
        # cv2.imwrite('{0}.png'.format(file_path.split('.')[0] + '_' + 'face'), crop)
    return ret

