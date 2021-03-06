# This is version 8 of my code. As of v7.2, the code is capable of training a
# reliable CNN model. From here onwards, I will attempt to integrate a GAN into
# the code base to augment dataset.

# Check that imports for the rest of the file work.
import numpy as np
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow_gan as tfgan
import tensorflow as tf

# For testing on Jupyter for immediate visual feedback later
# Allow matplotlib images to render immediately.
# %matplotlib inline

# Checking datasets
import os
paths = os.listdir(path="chest_xray")

path_train = "chest_xray/train"
path_val = "chest_xray/val"
path_test = "chest_xray/test"

img = glob(path_train+"/PNEUMONIA/*.jpeg")  # Getting all images in this folder
img = np.asarray(plt.imread(img[0]))

img = glob(path_train + "/NORMAL/*.jpeg")  # Getting all images in this folder
img = np.asarray(plt.imread(img[0]))

# Data preprocessing and analysis
classes = ["NORMAL", "PNEUMONIA"]
train_data = glob(path_train+"/NORMAL/*.jpeg")
train_data += glob(path_train+"/PNEUMONIA/*.jpeg")
data_gen = ImageDataGenerator()  # Augmentation happens here
# But in this example we're not going to give the ImageDataGenerator method any parameters to augment our data.


train_batches = data_gen.flow_from_directory(
    path_train,
    target_size=(226, 226),
    classes=classes,
    class_mode="categorical"
)

val_batches = data_gen.flow_from_directory(
    path_val,
    target_size=(226, 226),
    classes=classes,
    class_mode="categorical"
)

test_batches = data_gen.flow_from_directory(
    path_test,
    target_size=(226, 226),
    classes=classes,
    class_mode="categorical"
)

train_batches.image_shape

# This is a Convolutional Artificial Neural Network
# VGG16 Model
model = Sequential()
model.add(ZeroPadding2D((1, 1), input_shape=train_batches.image_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(256, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(ZeroPadding2D((1, 1)))
model.add(Conv2D(512, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.summary()

# OPTIMISERS
optimizer = Adam(lr=0.0001)

early_stopping_monitor = EarlyStopping(
    patience=3,
    monitor="val_acc",
    mode="max",
    verbose=2
)

model.compile(
    loss="categorical_crossentropy",
    metrics=["accuracy"],
    optimizer=optimizer
)

history = model.fit(
    x=train_batches,
    # batch_size=32,
    epochs=5,
    verbose=1,
    callbacks=[early_stopping_monitor],
    validation_split=0.0,
    validation_data=val_batches,
    shuffle=True,
    class_weight=None,
    sample_weight=None,
    initial_epoch=0,
    steps_per_epoch=163,
    validation_steps=10,
    validation_freq=1,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False
)

prediction = model.predict(
    train_batches,
    batch_size=None,
    verbose=1,
    steps=100,
    callbacks=None,
    max_queue_size=10,
    workers=1,
    use_multiprocessing=False
)

model.save('save/v7.1')

'''
Source: Jason Brownlee
Site: https://machinelearningmastery.com/display-deep-learning-model-training-history-in-keras/
'''
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()
