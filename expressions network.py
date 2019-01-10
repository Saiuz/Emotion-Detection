import numpy as np
import tensorflow as tf



def Expression_Network():
    def __init__(self):
        #hardcode in num_classes
        self.num_classes = 8
        self.x = tf.placeholder(dtype=tf.float32, shape=(None,128,128),name='x')

    def build_model(self, input):
        self.reshaped = tf.expand_dims(input, -1)
        # batch,128,128,1

        # first convolution
        self.conv = tf.contrib.layers.conv2d(
            self.reshaped,
            32,
            (9, 9),
            stride=(1, 1),
            padding='VALID',
            weights_initializer=tf.initializers.random_normal)
        # batch,120,120,32

        # subsample
        self.pool = tf.contrib.layers.max_pool2d(
            self.conv,
            (4, 4),
            stride=(4, 4))
        # batch,30,30,32

        # second convolution
        self.conv2 = tf.contrib.layers.conv2d(
            self.pool,
            64,
            (11, 11),
            stride=(1, 1),
            padding='VALID',
            weights_initializer=tf.initializers.random_normal)
        # batch,20,20,64

        # subsample
        self.pool2 = tf.contrib.layers.max_pool2d(
            self.conv2,
            (4, 4),
            stride=(4, 4))
        # batch,5,5,64

        # flatten
        self.flat = tf.contrib.layers.flatten(self.pool2)
        # batch,1600

        # fully connected
        self.fc = tf.contrib.layers.fully_connected(
            self.flat,
            1024,
            activation_fn=tf.nn.relu,
            weights_initializer=tf.initializers.random_normal)
        # batch,256
        self.logits = tf.contrib.layers.fully_connected(
            self.fc,
            self.num_classes,
            weights_initializer=tf.initializers.random_normal,
            activation_fn=None)

        self.prediction = tf.nn.softmax(self.logits, )