import tensorflow as tf
from nets import mobilenet_v1
from preprocess import simple_prerpocess
import cv2

slim = tf.contrib.slim

image_size = 224
train_dir = './ckpt/mobilenet_gender'

def infer_gender(img_dir):
    with tf.Graph().as_default():
        tf.logging.set_verbosity(tf.logging.INFO)

        np_img = cv2.imread(img_dir, cv2.IMREAD_COLOR)
        print(np_img.shape)
        img_tensor = tf.convert_to_tensor(np_img)
        img_tensor = tf.expand_dims(img_tensor, 0)
        processed_images = simple_prerpocess.preprocess_image(img_tensor, image_size, image_size)

        with slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
            logits, _ = mobilenet_v1.mobilenet_v1(processed_images, depth_multiplier=1.0, num_classes=2, is_training=False)

        probabilities = tf.nn.softmax(logits)

        checkpoint_path = tf.train.latest_checkpoint(train_dir)
        init_fn = slim.assign_from_checkpoint_fn(
              checkpoint_path,
              slim.get_variables_to_restore())

        with tf.Session() as sess:
            with slim.queues.QueueRunners(sess):
                sess.run(tf.local_variables_initializer())
                init_fn(sess)
                np_probabilities = sess.run([probabilities])
                predicted_label = np.argmax(np_probabilities[:])
                predicted_gender = 'female' if predicted_label == 0 else 'male'
                print(predicted_gender)
                return predicted_gender
