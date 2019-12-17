#script to create numpy arrays of pictures which have been through the first 5 blocks of the VGG16 algorithm and saves them in folder 'features'
#this script does not train

#retrieved from
#https://gist.github.com/fchollet/f35fbc80e066a49d65f1688a7e99f069

import numpy as np
import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras import applications
from keras.applications.vgg16 import preprocess_input
import os

os.chdir("../")

#%% parameters and folders 
img_width, img_height = 1000, 1000 # dimensions of our images

train_data_dir = "../data/satelliet/train"
test_data_dir = "../data/satelliet/test"
nb_train_samples = 2800
nb_test_samples = 675
batch_size = 25 #divisioner of nb_train_samples and nb_test_samples

# build the VGG16 network with weights="imagenet" or path to these weights
model = applications.VGG16(include_top=False, weights="weights/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5",input_shape=(1000,1000,3))

#%%generator

datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    
bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)

#save features in folder
np.save(open('features/train_features.npy', 'wb'),
            bottleneck_features_train)

generator = datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    
bottleneck_features_test = model.predict_generator(
        generator, nb_test_samples // batch_size)

#save features in folder
np.save(open('features/test_features.npy', 'wb'),
            bottleneck_features_test)
