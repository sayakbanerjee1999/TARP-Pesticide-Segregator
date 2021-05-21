# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 20:56:22 2021

@author: Sayak, Ritayan, Itsav
"""


# res_map = {'Potato___Early_blight': 0, 'Potato___Late_blight': 1, 'Potato___healthy': 2}


# Importing the required keraas library and Viz Libraries
from keras.models import Sequential
from keras.layers import Conv2D,Dense,MaxPooling2D,Activation,Dropout,Flatten
from keras.layers import GlobalAveragePooling2D
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.layers.normalization import BatchNormalization
from keras.callbacks import History

import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Image Dimension
image_size = 224
target_size = (image_size, image_size)
input_shape = (image_size, image_size, 3)


# Loading Images and Image Augmentation
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        'train',
        target_size=(image_size, image_size),
        batch_size=32,
        class_mode='categorical')

test_set = test_datagen.flow_from_directory(
        'test',
        target_size=(image_size, image_size),
        batch_size=32,
        class_mode='categorical')


# Building the Model
num_classes = 3
history = History()

model = Sequential()

model.add(Conv2D(32, (5, 5),input_shape=input_shape,activation='relu',name="conv2d_1"))
model.add(MaxPooling2D(pool_size=(3, 3),name="max_pooling2d_1"))
model.add(Conv2D(32, (3, 3),activation='relu',name="conv2d_2"))
model.add(MaxPooling2D(pool_size=(2, 2),name="max_pooling2d_2"))
model.add(Conv2D(64, (3, 3),activation='relu',name="conv2d_3"))
model.add(MaxPooling2D(pool_size=(2, 2),name="max_pooling2d_3"))   
model.add(Flatten(name="flatten_1"))

model.add(Dense(512,activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(128,activation='relu'))          
model.add(Dense(num_classes,activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics=['accuracy'])


# Fitting the model
history_1 = model.fit_generator(
        training_set,
        steps_per_epoch = None,
        epochs=10,
        validation_data= test_set,
        verbose=1,
        shuffle=True,
        callbacks = [history])



# Save the Model
model_name = 'potato_disease.h5'
model.save(model_name)



'''Accuracy, Loss Plot'''
plt.plot(history_1.history['accuracy'])
plt.plot(history_1.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# summarize history for loss
plt.plot(history_1.history['loss'])
plt.plot(history_1.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')




from keras.models import load_model
model = load_model('potato_disease.h5')
model.summary()




'''Prediction'''
pred = model.predict(test_set)
Y_pred = np.argmax(pred, axis = 1)



'''Checking the Result'''
from keras.preprocessing import image
test_image = image.load_img("single_prediction/PotatoEarlyBlight1.jpg", target_size = (224, 224))
plt.imshow(test_image)
test_image = image.img_to_array(test_image)    
test_image = np.expand_dims(test_image, axis = 0)   #convert image to 4 dimensions which the predict method expects
result = model.predict(test_image)

training_set.class_indices    #indicates which class is encoded

if result[0][0] == 1:
    prediction = "The Potato Leaf is detected to have Early Blight Disease"
elif result[0][1] == 1:
    prediction = "The Potato Leaf is detected to have Late Blight Disease"
elif result[0][2] == 1:
    prediction = "The Potato Leaf is healthy."
    
print(prediction)

