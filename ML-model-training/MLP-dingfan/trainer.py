'''
This will be the program to train the model during training scenario
'''

import pandas
import numpy as np
import pickle

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model
from keras.models import model_from_json
from keras.utils import np_utils, to_categorical
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn import cross_validation, preprocessing
from sklearn.metrics import confusion_matrix, accuracy_score
from keras.optimizers import SGD, Adam
from sklearn.model_selection import cross_val_score, StratifiedKFold
from keras import regularizers
from sklearn.externals import joblib

dataframe = pandas.read_csv('processed_train.csv', header=0)
dataset = dataframe.values

label_reference = [1,2,3,4,5,6,7,8,9,10,11]

len_data = len(dataset[0])
feature = dataset[:, 0:len_data-1].astype(float)
label = dataset[:, len_data-1].astype(int)

NUM_FEATURE = len_data-1
print('num of feature is ' + str(NUM_FEATURE))
NUM_LABEL = len(label_reference)+1

# The key is the scaler, previously the preprocessing.normalize() scale the values too low 
# and the model cannot detect the difference between different values. Hence cannot get effective prediction 
scaler = preprocessing.StandardScaler()
scaler.fit(feature) 
feature = scaler.transform(feature)
print(feature[0])

feature_train, feature_test, label_train, label_test = cross_validation.train_test_split(feature, label, test_size=0.2, random_state=4)

def fully_connected_model():
    # create model 
    model = Sequential()

    # build layers
    model.add(Dense(64, input_dim=NUM_FEATURE, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    # add dropout layer to avoid overfitting issues 
    model.add(Dropout(0.25))

    # The number of neurons in the last layer == number of classes 
    model.add(Dense(NUM_LABEL, activation='softmax')) # use softmax to represented predicted probabilty

    # compile model
    opt = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return model

estimator = KerasClassifier(build_fn=fully_connected_model, epochs=100, batch_size=100, verbose=1)
estimator.fit(feature, label)
model = estimator.model

'''
model got more parameters ==> more representation power(high capacity) ==> easy to get overfit since representation power is high
different techniques to avoid overfitting issues 
1. L1 or L2 regularization 
2. decay learning rate
3. add dropout layer ==> find optimal dropout rate
'''



label_pred_index = model.predict_classes(feature_test)
print(label_pred_index)
print(max(label_pred_index))
label_names = [1,2,3,4,5,6,7,8,9,10,11]
label_pred = []
for index in label_pred_index:
    label_pred.append(label_names[index])

matrix = confusion_matrix(label_test, label_pred)
accuracy = accuracy_score(label_test, label_pred)
print(matrix)
print(accuracy)

# Try different methods to save and load models since previously I am curious about whether there is any difference of these methods 
# if saving model in 64 bit system but loading model in 32 bit system

# pickle 
with open('model/pickle_saved.pickle', 'wb') as f:
    pickle.dump(model, f)
print('model saved in pickle. ')

with open('model/scaler.pickle', 'wb') as f:
    pickle.dump(scaler, f)
print('scaler saved in pickle. ')

# joblib
joblib.dump(model, 'model/model_df.joblib')
joblib.dump(scaler, 'model/scaler_df.joblib')

# Keras model saving
model_json = model.to_json()
with open('model/nn_structure.json', 'w') as f:
    f.write(model_json)
model.save_weights("model/weights.h5")
print('Model saved to disk with model.to_json(). ')

