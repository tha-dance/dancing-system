'''
This will be the program to predict the class of each dance move during actual scenario
'''
import pandas
from keras.models import model_from_json
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import preprocessing
from sklearn.externals import joblib

# Load model from storage
loaded_model = joblib.load('model/model_df.joblib')

print('Model loaded from disk. ')

dataframe = pandas.read_csv('processed_test.csv', header=0)
dataset = dataframe.values
len_data = len(dataset[0])
print(len_data)

feature = dataset[:, :len_data-1].astype(float)
label = dataset[:, len_data-1].astype(int)
label_names = [1,2,3,4,5,6,7,8,9,10,11]

# Load scaler from storage
scaler = joblib.load('model/scaler_df.joblib')
feature = scaler.transform(feature)
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
