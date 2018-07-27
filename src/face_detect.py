import cv2
from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt

detector = MTCNN()
file_path = '1.png'
image = cv2.imread(file_path)
boxes = detector.detect_faces(image)
if len(boxes) != 1:
    pass
else:
    face_position = boxes[0]['box']
    print(face_position)
    crop = image[face_position[1]:face_position[1] + face_position[3],
                   face_position[0]: face_position[0] + face_position[2]]
    cv2.imwrite('{0}.png'.format(file_path.split('.')[0] + '_' + 'face'), crop)
    cv2.imshow("Mouth1", crop)
    cv2.waitKey(0)
