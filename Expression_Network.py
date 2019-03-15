import numpy as np
import tensorflow as tf
import traceback


class Expression_Network(object):
    def __init__(self,num_classes,Training=False):
        #hardcode in num_classes
        try:
            self.Training = Training
            self.num_classes = num_classes


            if not self.Training:
                tf.reset_default_graph()
                self.x = tf.placeholder(dtype=tf.float32, shape=(None,128,128),name='x')
                self.model(self.x)
                self.sess = tf.Session()
                self.saver = tf.train.Saver()
                self.saver.restore(self.sess,"checkpoints/model.ckpt")
        except:
            data.done = True
            print("exception in model creation/restoration")
            traceback.print_exc()
            


    def predict_loop(self, data):
        try:
            while not data.done:
                if data.faceim is not None:
                    data.prediction = self.predict([data.faceim])
        except Exception as e:
            print("exception in predict loop")
            traceback.print_exc()
            data.done = True


    def predict(self, img):
        return self.sess.run(self.prediction, feed_dict={self.x:img})
    
    def model(self, x):
        self.reshaped = tf.expand_dims(x, -1)
        # batch,128,128,1

        # first convolution
        self.conv = tf.contrib.layers.conv2d(
            self.reshaped,
            32,
            (9,9),
            stride=(1,1),
            padding='VALID',
            weights_initializer=tf.initializers.random_normal)
        #batch,120,120,32

        #subsample
        self.pool = tf.contrib.layers.max_pool2d(
            self.conv,
            (4,4),
            stride=(4,4))
        #batch,30,30,32

        #second convolution
        self.conv2 = tf.contrib.layers.conv2d(
            self.pool,
            64,
            (11,11),
            stride=(1,1),
            padding='VALID',
            weights_initializer=tf.initializers.random_normal)
        #batch,20,20,64

        #subsample
        self.pool2 = tf.contrib.layers.max_pool2d(
            self.conv2,
            (4,4),
            stride=(4,4))
        #batch,5,5,64

        #flatten
        self.flat = tf.contrib.layers.flatten(self.pool2)
        #batch,1600

        #fully connected
        self.fc = tf.contrib.layers.fully_connected(
            self.flat,
            256,
            activation_fn=tf.nn.leaky_relu)

        #batch,256
        self.logits = tf.contrib.layers.fully_connected(
            self.fc,
            self.num_classes,
            activation_fn=None)

        self.prediction = tf.nn.softmax(self.logits,)
        if self.Training:
            return self.logits, self.prediction

