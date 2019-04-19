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

# loaded_model = None
# with open('model/new_model', 'rb') as f:
#     loaded_model = pickle.load(f)


print('Model loaded from disk. ')

# dataframe = pandas.read_csv('raffles.txt', header=None, delim_whitespace=True)
dataframe = pandas.read_csv('processed_test.csv', header=0)
dataset = dataframe.values
len_data = len(dataset[0])
print(len_data)
# feature = dataset[0:, 1:len_data-1].astype(float)
feature = dataset[:, :len_data-1]
label = dataset[:, len_data-1]
label_names = [1,2,3,4,5,6,7,8,9,10,11]
# print(feature)
# feature = preprocessing.normalize(feature)
scaler = preprocessing.StandardScaler()
scaler.fit(feature)
feature = scaler.transform(feature)
feature = feature.reshape(len(feature), 9,6,1)
print(feature.shape)

# feature_train, feature_test, label_train, label_test = cross_validation.train_test_split(feature, label, test_size=0.2, random_state=4)

label_pred_index = loaded_model.predict_classes(feature)
# label_pred_index = loaded_model.predict(feature)
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

# input = extract(feature_test)
# print(input)
# class_index = loaded_model.predict_classes(feature_test[0:1])
# print(class_index) # the predicted output is an array
# print(label_test[0:1], label_names[class_index[0]])
