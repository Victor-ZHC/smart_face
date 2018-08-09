import apply_gender_mobilenet
import apply_age_mobilenet

img_dir = 'XX.jpg'

age = apply_age_mobilenet.infer_age(img_dir)
gender = apply_gender_mobilenet.infer_gender(img_dir)