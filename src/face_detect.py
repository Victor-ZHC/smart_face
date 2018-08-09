import cv2
from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt
import numpy as np

def get_np_array_from_file_obj(fileobj):
    '''converts a buffer from a tar file in np.array'''
    return np.asarray(
        bytearray(fileobj.read())
        , dtype=np.uint8)

def detect(imgfile):
    detector = MTCNN()
    image = cv2.imdecode(
        get_np_array_from_file_obj(imgfile)
        , cv2.IMREAD_UNCHANGED )
    cv2.imwrite('testout.png', image)
    boxes = detector.detect_faces(image)
    ret=[]
    for box in boxes:
        face_position = box['box']
        print(face_position)
        crop = image[face_position[1]:face_position[1] + face_position[3],
                       face_position[0]: face_position[0] + face_position[2]]
        ret.append({'box':face_position,'gender':0,'age':25})
        #cv2.imwrite('{0}.png'.format(file_path.split('.')[0] + '_' + 'face'), crop)
    return ret

