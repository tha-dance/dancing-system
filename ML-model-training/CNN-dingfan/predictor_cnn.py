'''
This will be the program to predict the class of each dance move during actual scenario
'''
import pandas
import pickle
from keras.models import model_from_json
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix, accuracy_score
from feature_extraction import extract
from sklearn import preprocessing

json_file = open("model/cnn_structure.json")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model/cnn_weights.h5")

print('Model loaded from disk. ')

dataframe = pandas.read_csv('processed_test.csv', header=0)
dataset = dataframe.values
len_data = len(dataset[0])

feature = dataset[:, :len_data-1]
label = dataset[:, len_data-1]
label_names = [1,2,3,4,5,6,7,8,9,10,11]

# Here I initialise the StandardScaler by myself. However, during actual scenario the scaler is loaded from storage.
scaler = preprocessing.StandardScaler()
scaler.fit(feature)
feature = scaler.transform(feature)
feature = feature.reshape(len(feature), 9,6,1)
print(feature.shape)

label_pred_index = loaded_model.predict_classes(feature)

label_pred = []
for index in label_pred_index:
    label_pred.append(label_names[index])
print(label_pred)

matrix = confusion_matrix(label_pred, label)
accur = accuracy_score(label_pred, label)
print(matrix)
print(accur)
