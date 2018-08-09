# face data download from:
#
#     https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
#
# For both the IMDb and Wikipedia images we provide a separate .mat file
# which can be loaded with Matlab containing all the meta information. The format is as follows:
#
# dob:
#     date of birth (Matlab serial date number)
# photo_taken:
#     year when the photo was taken
# full_path:
#     path to file
# gender:
#     0 for female and 1 for male, NaN if unknown
# name:
#     name of the celebrity
# face_score:
#     detector score (the higher the better).
#     Inf implies that no face was found in the image and the face_location then just returns the entire image
# second_face_score:
#     detector score of the face with the second highest score.
#     This is useful to ignore images with more than one face. second_face_score is NaN if no second face was detected.
# celeb_names (IMDB only):
#     list of all celebrity names
# celeb_id (IMDB only):
#     index of celebrity name


import argparse
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import tensorflow as tf
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
from mtcnn.mtcnn import MTCNN
import cv2

FLAGS = None


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


# Converts a dataset to tfrecords.
def convert_to(data_set, name, base_path, dataset_name):
    file_name = data_set.file_name
    genders = data_set.gender
    ages = data_set.age
    face_score = data_set.score
    second_face_score = data_set.second_score

    num_examples = data_set.shape[0]
    if dataset_name == "imdb":
        image_base_dir = os.path.join(base_path, "imdb_crop")
    elif dataset_name == "wiki":
        image_base_dir = os.path.join(base_path, "wiki_crop")
    else:
        raise NameError

    output_path = os.path.join(base_path, 'face', name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    detector = MTCNN()

    total = 0
    multi_face = 0

    for index in range(num_examples):
        file_path = os.path.join(image_base_dir, str(file_name[index][0]))
        if not os.path.exists(file_path):
            continue
        if face_score[index] < 0.75:
            continue
        if not (0 <= ages[index] <= 100):
            continue
        if np.isnan(genders[index]):
            continue

        # load the input image
        image = cv2.imread(file_path)
        boxes = detector.detect_faces(image)
        if len(boxes) != 1:
            multi_face = multi_face + 1
        else:
            face_position = boxes[0]['box']
            crop = image[face_position[1]:face_position[1] + face_position[3],
                   face_position[0]: face_position[0] + face_position[2]]
            output_file = os.path.join(output_path, '%d_%d_%d.jpg' % (total, int(ages[index]), int(genders[index])))
            cv2.imwrite(output_file, crop)
            total = total + 1
    print("There are %d multi face pictures" % multi_face)
    print("Found %d valid faces" % total)


def get_meta(mat_path, db):
    if len(db) == 2:
        meta = loadmat(mat_path[0])
        full_path = meta[db[0]][0, 0]["full_path"][0]
        dob = meta[db[0]][0, 0]["dob"][0]  # Matlab serial date number
        gender = meta[db[0]][0, 0]["gender"][0]
        photo_taken = meta[db[0]][0, 0]["photo_taken"][0]  # year
        face_score = meta[db[0]][0, 0]["face_score"][0]
        second_face_score = meta[db[0]][0, 0]["second_face_score"][0]
        age = [calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]
        data = {"file_name": full_path, "gender": gender, "age": age, "score": face_score,
                "second_score": second_face_score}
        data_set1 = pd.DataFrame(data)

        meta = loadmat(mat_path[1])
        full_path = meta[db[1]][0, 0]["full_path"][0]
        dob = meta[db[1]][0, 0]["dob"][0]  # Matlab serial date number
        gender = meta[db[1]][0, 0]["gender"][0]
        photo_taken = meta[db[1]][0, 0]["photo_taken"][0]  # year
        face_score = meta[db[1]][0, 0]["face_score"][0]
        second_face_score = meta[db[1]][0, 0]["second_face_score"][0]
        age = [calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]
        data = {"file_name": full_path, "gender": gender, "age": age, "score": face_score,
                "second_score": second_face_score}
        data_set2 = pd.DataFrame(data)
        data_set = pd.concat([data_set1, data_set2], axis=0)
    else:
        meta = loadmat(mat_path)
        full_path = meta[db][0, 0]["full_path"][0]
        dob = meta[db][0, 0]["dob"][0]  # Matlab serial date number
        gender = meta[db][0, 0]["gender"][0]
        photo_taken = meta[db][0, 0]["photo_taken"][0]  # year
        face_score = meta[db][0, 0]["face_score"][0]
        second_face_score = meta[db][0, 0]["second_face_score"][0]
        age = [calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]
        data = {"file_name": full_path, "gender": gender, "age": age, "score": face_score,
                "second_score": second_face_score}
        data_set = pd.DataFrame(data)
    return data_set


def calc_age(taken, dob):
    birth = datetime.fromordinal(max(int(dob) - 366, 1))

    # assume the photo was taken in the middle of the year
    if birth.month < 7:
        return taken - birth.year
    else:
        return taken - birth.year - 1


def main(db_path, db_name, test_size, base_path):
    start_time = time.time()
    data_sets = get_meta(db_path, db_name)

    train_sets, test_sets = train_test_split(data_sets, test_size=test_size, random_state=2018)
    train_sets.reset_index(drop=True, inplace=True)
    test_sets.reset_index(drop=True, inplace=True)

    convert_to(train_sets, 'train', base_path, db_name)
    convert_to(test_sets, 'test', base_path, db_name)

    duration = time.time() - start_time
    print("Running %.3f sec All done!" % duration)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--imdb_db", type=str, default="./data/imdb_crop/imdb.mat")
    parser.add_argument("--wiki_db", type=str, default="./data/wiki_crop/wiki.mat")
    parser.add_argument("--imdb", action="store_true", default=True, help="Set this flag if use imdb datasets")
    parser.add_argument("--wiki", action="store_true", default=False, help="Set this flag if use wiki datasets")
    parser.add_argument("--base_path", type=str, default="./data", help="Base path of datasets and tfrecords")
    parser.add_argument("--test_size", type=float, default=0.1, help="How many items as testset")
    args = parser.parse_args()
    if args.imdb and args.wiki:
        print("Using imdb and wiki datasets")
        main(db_path=[args.imdb_db, args.wiki_db], db_name=["imdb", "wiki"], test_size=args.test_size,
             base_path=args.base_path)
    elif args.imdb:
        print("Using imdb dataset")
        main(db_path=args.imdb_db, db_name="imdb", test_size=args.test_size,
             base_path=args.base_path)
    elif args.wiki:
        print("Using wiki dataset")
        main(db_path=args.wiki_db, db_name="wiki", test_size=args.test_size,
             base_path=args.base_path)
    else:
        raise NameError("You should choose one of --imdb or --wiki when running this script.")

if __name__ == '__main__':
    app.run(debug=True)