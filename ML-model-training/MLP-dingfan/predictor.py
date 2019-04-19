'''
This will be the program to predict the class of each dance move during actual scenario
'''
import pandas
from keras.models import model_from_json
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import preprocessing
import pickle
from sklearn.externals import joblib

# json_file = open("model/nn_structure.json")
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("model/weights.h5")

# loaded_model = pickle.load(open('model/pickle_saved.pickle', 'rb'))
loaded_model = joblib.load('model/model_df.joblib')

print('Model loaded from disk. ')

# dataframe = pandas.read_csv('raffles.txt', header=None, delim_whitespace=True)
dataframe = pandas.read_csv('processed_test.csv', header=0)
dataset = dataframe.values
len_data = len(dataset[0])
print(len_data)
# feature = dataset[0:, 1:len_data-1].astype(float)
feature = dataset[:, :len_data-1].astype(float)
label = dataset[:, len_data-1].astype(int)
label_names = [1,2,3,4,5,6,7,8,9,10,11]
# print(feature)
# feature = preprocessing.normalize(feature)
# scaler = preprocessing.StandardScaler()
# scaler.fit(feature)
# scaler = pickle.load(open('model/scaler.pickle', 'rb'))
scaler = joblib.load('model/scaler_df.joblib')
feature = scaler.transform(feature)
print(feature.shape)

label_pred_index = loaded_model.predict_classes(feature)
# print(label_pred_index)
label_pred = []
# label = []
for index in label_pred_index:
    label_pred.append(label_names[index])
    # label.append(1)
# print(label.shape)
print(label_pred)

matrix = confusion_matrix(label_pred, label)
accur = accuracy_score(label_pred, label)
print(matrix)
print(accur)
