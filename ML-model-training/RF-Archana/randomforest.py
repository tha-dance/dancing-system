
from pandas import read_csv
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import numpy as np
from matplotlib import pyplot as plt

def load_file(filepath):
	data_frame = read_csv(filepath, header=None, delim_whitespace =True)
	return data_frame.values

def load_features():
	features = load_file('./HARDataset/features.txt')
	return features

def load_dataset_test(filename):
	X = load_file(filename)
	return X;

def load_dataset_group(group,prefix = ''):
	X = load_file(prefix+group+'/trainx_2models'+'.txt')
	y = load_file(prefix+group+'/trainy_2models'+'.txt')
	return X,y

def load_dataset(prefix=''):
	X,Y = load_dataset_group('train',prefix+'./Datasets_new/')

	trainX, testX, trainy, testy = train_test_split(X, Y, test_size=0.4, random_state = 2)
	#print(testX.shape, testy.shape)

	trainy, testy = trainy[:,0], testy[:,0]
	return trainX, trainy, testX, testy
	#return X,Y
def evaluate_model (testX,testy,model):
	pred = model.predict(testX);
	accuracy = accuracy_score(pred,testy);
	print (" Confusion matrix \n", confusion_matrix(testy, pred))

	return accuracy*100.0


#load dataset and split into train and test
trainX,trainy,testX,testy= load_dataset()

# initialise the random forest classifier 
rf = RandomForestClassifier(n_estimators = 200,criterion = "gini", n_jobs= -1);

# sfm helps filter out features that aren't important to the prediciton
sfm = SelectFromModel(rf,threshold = 0.00001)

#fit sfm to train data
sfm.fit(trainX,trainy)

#transform the test and train data
trainX_imp = sfm.transform(trainX);
testX_imp = sfm.transform(testX);

#train random forest
rf.fit(trainX_imp,trainy)

#make predicition
pred = model.predict(testX);

joblib.dump(rf,"rf_final")
model = joblib.load("rf_final")

kf = StratifiedKFold(n_splits=5,random_state=4)
results = evaluate_model(testX_imp,testy,model)


trial = cross_val_score(model,trainX,trainy,cv=kf)
#for name, importance in zip(features, model.feature_importances_):
#	print(name, "=", importance)

 #plt.bar(range(len(model.feature_importances_)), model.feature_importances_)
 #plt.show()

#print("prarameters in use: ",model.get_params());
print('results = %.3f' %results,'cross_val_score = %.3f' %(trial.mean()*100));




