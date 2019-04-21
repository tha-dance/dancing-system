import pandas as pd
import numpy as np
from pandas import read_csv
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler  
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.model_selection import cross_val_score 
from sklearn.externals import joblib



def load_file(filepath):
	data_frame = read_csv(filepath, header=None, delim_whitespace=True)
	return data_frame.values

def load_dataset_group(group,prefix = ''):
	X = load_file(prefix+group+'/trainx_17april_logout'+'.txt')
	y = load_file(prefix+group+'/trainy_17april_logout'+'.txt')
	print(np.where(np.isnan(X)))
	return X,y


def load_dataset(prefix=''):
	X,Y = load_dataset_group('train',prefix+'./Datasets_new/')

	trainX, testX, trainy, testy = train_test_split(X, Y, test_size=0.05, random_state = 2)
	trainy, testy = trainy[:,0], testy[:,0]
	return trainX, trainy, testX, testy

def evaluate_model (testX,testy,model):
	pred = model.predict(testX);
	pred = model.predict(testX);
	accuracy = accuracy_score(pred,testy);
	print (" Confusion matrix \n", confusion_matrix(testy, pred))

	return accuracy*100.0


trainX, trainy, testX, testy = load_dataset()

scaler = StandardScaler()
scaler.fit(trainX)

trainX = scaler.transform(trainX)
testX = scaler.transform(testX)

kf = StratifiedKFold(n_splits=5,random_state=4)
mlp = MLPClassifier(hidden_layer_sizes=(40,40,40), alpha =0.001)
mlp.fit(trainX,trainy);



joblib.dump(mlp,"mlp_19april_logout")
joblib.dump(scaler, 'scaler_19april_logout.joblib')

model = joblib.load("mlp_19april_logout")

results = evaluate_model (testX,testy,model)
trial = cross_val_score(model,trainX,trainy,cv=kf)
print("iteration x: "+str(trial));
print('results = %.3f' %results,'cross_val_score = %.3f' %(trial.mean()*100));


