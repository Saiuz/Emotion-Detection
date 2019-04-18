import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Reshape, Dropout
import traceback

class Expression_Network(object):
    def __init__(self,num_classes,Training=False):
        self.Training = Training
        self.num_classes = num_classes
        self.loaded = False

    def load_model(self):
        self.model = self.build_model()
        self.model.build(input_shape=(128,128))
        self.model.load_weights("checkpoints/model.h5")
        self.loaded = True

    def predict_loop(self, data):
        try:
            self.load_model()
            while not data.done:
                if data.faceim is not None:
                    data.prediction = np.argmax(self.predict([data.faceim]))
            data.done = True
        except Exception as e:
            print("exception in predict loop")
            traceback.print_exc()
            data.done = True

    def predict(self, img):
        if not self.loaded:
            self.load_model()
        return self.model.predict([img])

    def build_model(self):
        model = tf.keras.models.Sequential([
            # greyscale images don't have a third channel, so in order for conv2D to accept them, we need to
            # add another dimension. This doesn't change the contents of the picture, just the format.
            Reshape((128,128,1),input_shape=(128,128)),      
            Conv2D(32, 9, activation='relu'),
            MaxPooling2D(pool_size=4),
            BatchNormalization(),
            Conv2D(64, 11, activation='relu'),
            MaxPooling2D(pool_size=4),
            Dropout(rate=.2),
            # Flatten our data down to 1 dimension so it can be fed into our dense layers
            Flatten(),
            Dense(256, activation=tf.nn.leaky_relu, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(self.num_classes,activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.001))
        ])
        return model
