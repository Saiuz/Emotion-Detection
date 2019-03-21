import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras import Model
import traceback


class Expression_Network(Model):
    def __init__(self,num_classes,Training=False):
        #hardcode in num_classes
        try:
            super(Expression_Network, self).__init__()
            self.Training = Training
            self.num_classes = num_classes
            # batch,128,128,1
            
            # first convolution
            self.conv1 = Conv2D(32, 9, activation='relu')

            #batch,120,120,32
            #subsample
            self.pool1 = MaxPooling2D(pool_size=4)

            #batch,30,30,32
            self.poolnorm = BatchNormalization()

            #second convolution
            self.conv2 = Conv2D(64, 11, activation='relu')
            #batch,20,20,64

            #subsample
            self.pool2 = MaxPooling2D(pool_size=4)
            #batch,5,5,64
            self.pool2norm = BatchNormalization()

            #flatten
            self.flat = Flatten()
            #batch,1600


            #fully connected
            self.dense = Dense(256, activation=tf.nn.leaky_relu,input_shape=(1600,))

            self.densenorm = BatchNormalization()


            #batch,256
            self.dense2 = Dense(self.num_classes,activation="softmax")
            
            
          
            if not self.Training:
                self.load_weights("checkpoints/weights.best.hdf5")

        except:
            print("exception in model creation/restoration")
            traceback.print_exc()
            


    def predict_loop(self, data):
        try:
            while not data.done:
                if data.faceim is not None:
                    data.prediction = np.argmax(self.predict([data.faceim]))
        except Exception as e:
            print("exception in predict loop")
            traceback.print_exc()
            data.done = True


    def predict(self, img):
        return self.model.predict(img)
    def call(self,x):
        x = tf.keras.backend.expand_dims(x,-1)
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.poolnorm(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.pool2norm(x)
        x = self.flat(x)
        x = self.dense(x)
        x = self.densenorm(x)
        x = self.dense2(x)
        return x
    
    def build_model(self):
        # batch,128,128,1
   
        # first convolution
        self.conv1 = Conv2D(32, 9, activation='relu')

        #batch,120,120,32
        #subsample
        self.pool1 = MaxPooling2D(pool_size=4)
        
        #batch,30,30,32
        self.poolnorm = BatchNormalization()

        #second convolution
        self.conv2 = Conv2D(64, 11, activation='relu')
        #batch,20,20,64

        #subsample
        self.pool2 = MaxPooling2D(pool_size=4)
        #batch,5,5,64
        self.pool2norm = BatchNormalization()

        #flatten
        self.flat = Flatten()
        #batch,1600
        

        #fully connected
        self.dense = Dense(256, activation=tf.nn.leaky_relu,input_shape=(1600,))
                       
        self.densenorm = BatchNormalization()


        #batch,256
        self.dense2 = Dense(self.num_classes,activation="softmax")


