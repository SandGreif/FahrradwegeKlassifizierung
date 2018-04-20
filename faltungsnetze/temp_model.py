#coding=utf-8

from __future__ import print_function

try:
    from hyperopt import Trials, STATUS_OK, rand
except:
    pass

try:
    from hyperas import optim
except:
    pass

try:
    from hyperas.distributions import uniform, choice
except:
    pass

try:
    import os
except:
    pass

try:
    import cv2
except:
    pass

try:
    from keras.utils import np_utils
except:
    pass

try:
    from keras.models import Sequential
except:
    pass

try:
    from keras.layers.core import Dense, Dropout, Activation, Flatten
except:
    pass

try:
    from keras.layers.convolutional import Conv2D, MaxPooling2D
except:
    pass

try:
    from keras.optimizers import RMSprop
except:
    pass

try:
    import numpy as np
except:
    pass

try:
    import pandas
except:
    pass

try:
    from sklearn.utils import shuffle
except:
    pass

try:
    from sklearn.model_selection import train_test_split
except:
    pass

try:
    from sklearn.metrics import confusion_matrix
except:
    pass

try:
    import matplotlib
except:
    pass

try:
    import matplotlib.pyplot as plt
except:
    pass

try:
    from mpl_toolkits.axes_grid1 import ImageGrid
except:
    pass

try:
    import seaborn
except:
    pass
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperas.distributions import conditional

# Läd alle Bildaufnahmen der Klasse unbefestigt 
imagePathName = 'C:/Users/morro/Documents/fahrradwegeKlassifizierung/daten/datensatz/22/unbefestigt/zugeschnitten/'
files = os.listdir(imagePathName)
for file in files:
    if "jpg" not in file:
        continue
    images.append(cv2.cvtColor(cv2.imread(imagePathName + file),cv2.COLOR_BGR2RGB))
# Läd alle Bildaufnahmen der Klasse befestigt
startIndexUnpaved = len(images)
imagePathName = 'C:/Users/morro/Documents/fahrradwegeKlassifizierung/daten/datensatz/22/befestigt/zugeschnitten/'
files = os.listdir(imagePathName)
for file in files:
    if "jpg" not in file:
        continue
    images.append(cv2.cvtColor(cv2.imread(imagePathName + file),cv2.COLOR_BGR2RGB))
# Y Klassen Labels zuweisen
yLabels = np.zeros(len(images)) 
yLabels[startIndexUnpaved-1:len(images)] = 1
# Erstellt einen "one hot encoding vector" für die gelabelten Bilder
yLabels = np_utils.to_categorical(yLabels, 0)
# Setzten des RandomState um reproduzierbare Ergebnisse zu erzielen.
np.random.seed(42)
imagesNp = np.array(images)
imagesNp = imagesNp.astype('float32')
# Transfomierung der Bildpunkte auf den Wetebereich von 0 bis 1
imagesNp /= 255

xShuffle, yShuffle = shuffle(imagesNp,yLabels)
# Aufteilung in Trainings und Testdaten
xTrain, xTest, yTrain, yTest = train_test_split(xShuffle, yShuffle, test_size=0.2)
print('data functioN')


def keras_fmin_fnct(space):

    # Parameter für das CNN
    inputShape     = xTrain[0].shape   # Eingangs Array-Form 
    numNeuronsC1   = 32                # Anzahl der Neuronen der 1 Faltungsschicht
    numNeuronsC2   = 64                # Anzahl der Neuronen der 2 Faltungsschicht
    numNeuronsD1   = 64                # Anzahl der Neuronen des Fully connected layer - vollverbundene Schicht  
    convKernelSize = 3                 # Größe des Faltungskern n*n
    model = Sequential()
    model.add(Conv2D(128, (convKernelSize, convKernelSize), padding='valid',input_shape=inputShape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.4))

    model.add(Conv2D(numNeuronsC2, (convKernelSize, convKernelSize)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.4))

    model.add(Flatten())

    model.add(Dense(numNeuronsD1))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))

    model.add(Dense(2))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])
    print('Train...')
    model.fit(xTrain, yTrain, batch_size=32, nb_epoch=2,
              validation_data=(xTest, yTest))
    score, acc = model.evaluate(xTest, yTest, batch_size=32)

    print('Test score:', score)
    print('Test accuracy:', acc)
    return {'loss': -acc, 'status': STATUS_OK, 'model': model}

def get_space():
    return {
    }
