import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Reshape, Dropout
from tensorflow.keras import Model
import traceback

#TESTING
import cv2
import time
#TESTING
class Expression_Network(object):
    def __init__(self,num_classes,Training=False):
        #hardcode in num_classes
        try:
            self.Training = Training
            self.num_classes = num_classes        
            self.loaded = False
        except:
            print("exception in model creation/restoration")
            traceback.print_exc()
            
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
    
    #def call(self,x):
    #    x = tf.keras.backend.expand_dims(x,-1)
    #    x = self.conv1(x)
    #    x = self.pool1(x)
    #    x = self.poolnorm(x)
    #    x = self.conv2(x)
    #    x = self.pool2(x)
    #    x = self.pool2norm(x)
    #    x = self.flat(x)
    #    x = self.dense(x)
    #    x = self.densenorm(x)
    #    x = self.dense2(x)
    #    return x
    
    def build_model(self):
        # batch,128,128,1
        model = tf.keras.models.Sequential([
            Reshape((128,128,1),input_shape=(128,128)),      
            Conv2D(32, 9, activation='relu'),
            MaxPooling2D(pool_size=4),
            BatchNormalization(),
            Conv2D(64, 11, activation='relu'),
            MaxPooling2D(pool_size=4),
            Dropout(.2),
            Flatten(),
            Dense(256, activation=tf.nn.leaky_relu, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(self.num_classes,activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.001))
        ])
        return model