# Emotion Detection (tutorial)
The goal of this repo is to teach/show a basic (but not trivial) example of how to use computer vision techniques to accurately classify facial emotions. I've tried to make it as easy as possible to follow my code by heavily documenting it (probably over documenting it), and putting it in notebooks.  


If you want to learn about the basics of opencv, Convolutional Neural Networks, 
or just want a fun project idea, you're in the right place.

Although you can learn most of the techniques in this project on the fly. 
There are some things that I recommend you have if you want to get the most out of the project.
- Intermediate knowledge of python
- Basic high level knowledge of Neural Networks
- Familiarity with the concept of threading
- Decent computer, Nvidia GPU is a big bonus
- Ability to make many angry looking faces to create your own face/emotion dataset

## Project Description/Goals
Obviously I'm trying to create a system to classify emotions on someones face, so here's the plan.
1. Capture video camera feed
2. Extract faces from the video camera images
3. Use a Convolutional Neural Network to classify the emotion on the face
4. Make our own face/emotion dataset to train the Neural Network on
5. Use the classification to do something? Change Hue lights?

# Requirements
Tensorflow 2.0
Skimage
tqdm
matplotlib
phue (if you want to control hue lights)

# Creating Our Own Dataset
This is both the easiest part, and the most boring. But i've tried to make it as simple as possible. To easily create your own labels and take pictures from your desktop I recommend the app I made [https://github.com/ablacklama/FaceLabeler](https://github.com/ablacklama/FaceLabeler/releases). This works well for this project because the folder layout and a lot of the files used are the same. There is also an exe version of the labeler that you can put into your main folder and get up and running quickly. Just check the instructions on the [repo](https://github.com/ablacklama/FaceLabeler)

Labels are defined in the `labelList.csv` file. Each row has an index and it's corisponding label. Add whatever labels you want to this or use the defaults.

Images are saved to the `Images` folder and the image name along with the label is saved to `faceLabels.csv`.

The goal here is to create a representative and diverse dataset. So make sure to take pictures under all the conditions that you want the program to run in. Glasses on/off, different lighting, different hair style, ect.

Try to get several hundred pictures with each label. It doesn't take that long I promise.


# Multi-Threading
A lot of what we want to do in this project requires a lot of computation. We have a video feed that is reading images from our webcam and displaying them and up to 60fps, a face detector that's running a cpu heavy feature extractor, and a Convolutional Neural Network that is trying to classify images as fast as it can.  
If we try having the program run linearly (read image->find face->classify emotion), we will end up with a lot of lag. And I should know, i tried. So instead of staring at a slideshow that updates once or twice a second, I decided to use muiltithreading. 

If you're not familiar with multi-threaded applications, I'd suggest watching (this video.)[https://www.youtube.com/watch?v=7ENFeb-J75k]  
But the basic idea is that we're enabling those three parts of the program to run simultaneously. So the video is being displayed at the same time that faces are being detected and emotions are being classified. 

These three threads (four if you include controlling my hue lights) need to send data to eachother. So i created an instance of a shared data class that they can all read data from and write to. So the video thread is constantly updating the latest image so the face detection thread can read it. And the face detection thread is constantly updating the data class with the latest image of a face it's detected. And then the neural network can use the latest face to classify the emotion, and put that classification back in the data class.

Since we're using jupyter notebooks, we can't just assume threads will stop when the program ends. So I created a `done` bool in the `data` class so that if one thread encounters an exception or the user presses esc, all threads will know to stop.

That all make sense? If it doesn't don't worry, i'll go into more detail below, and you can also look at the comments in the code.



# Video Capture
Video capture and displaying is done in the `display` class. Here I use opencv to initialize the default webcam. The majority of the video capture loop is reading an image, changing it to greyscale (so that the face detector can run on it), and putting it into the shared data class. But after that's done, we read the latest face dimentions and emotion label from the shared data class, and draw them on screen. 



# Face Detection 
So now that we've got our greyscale images into the shared data folder, it's time to get those faces. To do that I used a the haar cascade object recognition algorithm. The algorithm works by first using lots of different filters to extract features in the image and match them to some template that you setup. Or something like that. Point is, we're using a face template that someone way smarter that me already created. This is running in a loop, and when a face is detected, it puts the coordinates of that face box (x,y,width,height) into the shared data class.


# Emotion Detector
This is the real meat of the program, the convolutional neural network that classifies our emotions. I'm using a basic network with a few convolutional layers to extract features, a few fully connected layers at the bottom for classification, and a few normalization layers to prevent overfitting (read "memorizing") the dataset. 

`Reshape`  
`Convolutional`  
`Max Pooling `  
`Batch Normalization`  
`Convolutional`  
`Max Pooling`  
`Dropout`  
`Flattening`  
`Fully Connected`  
`Fully Connected`  
`Softmax (output)`  


I'm using Tensorflow 2.0's Keras interface to define the model in `Expression_Network.py`.

When actually running the whole system, I run the `prediction_loop` in a thread by itself. This runs the network on the latest face image from the shared data class. Then puts the prediction (in the form of an index) back into the dataclass so that the display thread can show it. If you want to create a program that does something based on the emotion detected, this value is what you should pay attention too.



# Training the Network
This is all defined and explained in `Train_Network.ipynb`, but i'll give an overview here.  
Keras makes training very easy, so most of the notebook is devoted to preprocessing that data. In this case, we need to read all the labels and corresponding images. make sure all the photos are of uniform size and greyscale. And the labels need to be turned into integers and then converted to [one-hot-encoded](https://hackernoon.com/what-is-one-hot-encoding-why-and-when-do-you-have-to-use-it-e3c6186d008f) arrays.
