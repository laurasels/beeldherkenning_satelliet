#open numpy arrays created in generator.py and trains top layers with these images.

#retrieved from
#https://gist.github.com/fchollet/f35fbc80e066a49d65f1688a7e99f069

import numpy as np
import keras
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dropout, Dense, , GlobalMaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping,ModelCheckpoint
import os
import pickle
import random

os.chdir("../")

#%% parameters and folders 
img_width, img_height = 1000, 1000 #dimensions of our images

weights_path = "weights/top_model.h5"
hist_path = "hist/top_model.pickle"
train_data_dir = "../data/satelliet/train"
test_data_dir = "../data/satelliet/test"
nb_train_samples = 2800
nb_test_samples = 675
epochs = 50
batch_size = 25 #divisioner of nb_train_samples and nb_test_samples

#%% load train and test data from created numpy arrays in generator.py and create labels

train_data = np.load(open('features/train_features.npy','rb')) 

train_labels = np.array(
        [0] * (len(os.listdir(train_data_dir+"/no"))) + [1] * (len(os.listdir(train_data_dir+"/yes"))))

test_data = np.load(open('features/test_features.npy','rb'))#opens features stored in numpy array

test_labels = np.array(
        [0] * (len(os.listdir(test_data_dir+"/no"))) + [1] * (len(os.listdir(test_data_dir+"/yes"))))

#%% create the top model
model = Sequential()
model.add(GlobalMaxPooling2D(input_shape=train_data.shape[1:]))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(BatchNormalization())
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=1e-5),
                  loss='binary_crossentropy', metrics=['accuracy'])

es = EarlyStopping(monitor='val_acc', mode='max', min_delta=0.001,patience=10)
mc = ModelCheckpoint(weights_path, monitor='val_acc', mode='max', save_best_only=True)

#class_weight = {0: 1., 1: 4202./2798.} # use if unbalanced dataset {0: 1., nb_no_samples./nb_yes_samples.}

#%% train the model
history = model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(test_data, test_labels),callbacks=[es,mc]) #add class_weight=class_weight if unbalanced dataset is used

#saves history of training proces of every epoch in pickle file
with open(hist_path, 'wb') as file_pi:
    pickle.dump(history.history, file_pi)
