import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, confusion_matrix, f1_score #does the sensisitvity need to be imported
import pickle

##Step1: Load Dataset

dataframe = pd.read_csv("spam.csv")
#print(dataframe.describe())

##Step2: Split in to Training and Test Data

x = dataframe["EmailText"] #column label
y = dataframe["Label"]

x_train,y_train = x[0:4457],y[0:4457] #4457 rows to training set remaining to test set
x_test,y_test = x[4457:],y[4457:]
y_true = y_test.tolist() #actual values for the labels of the EmailText. gets all labels from testing data it knows the true values

'''
##Step3: Extract Features
cv = CountVectorizer()


#Everything below has been used to train the models and dump the models into two seperate pickle files

cv.fit(x_train)
features = cv.transform(x_train)
'''
##Step4: Initiate and build different models
'''

tuned_parameters = {'kernel': ['rbf','linear'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]}

model = GridSearchCV(svm.SVC(), tuned_parameters)
model2 = MultinomialNB()
model3 = RandomForestClassifier(n_estimators=100)
model4 = LogisticRegression()

model.fit(features,y_train)
model2.fit(features, y_train)
model3.fit(features, y_train)
model4.fit(features, y_train)

'''

#initiate pickle file names
cv_file = 'cv.pkl'
svm_file = 'svm_model.pkl'
nb_file = 'nb_model.pkl'
rf_file = 'rf_model.pkl'
lr_file = 'lr_model.pkl'
'''

#dump models into pickle files for quick access
pickle.dump(cv, open(cv_file, 'wb'))
print('CV has loaded')
pickle.dump(model, open(svm_file, 'wb'))
pickle.dump(model2, open(nb_file, 'wb'))
pickle.dump(model3, open(rf_file, 'wb'))
pickle.dump(model4, open(lr_file, 'wb'))
print('models are loaded')

'''
cv = pickle.load(open(cv_file, 'rb')) #load count vectorizer from pickle file
loaded_svm_model = pickle.load(open(svm_file, 'rb'))
loaded_nb_model = pickle.load(open(nb_file, 'rb'))
loaded_rf_model = pickle.load(open(rf_file, 'rb'))
loaded_lr_model = pickle.load(open(lr_file, 'rb'))

prediction_set = x_test.tolist() #set of data we are trying to prdict takes all emailtext from test set of data
svm_predicted_set = [] #initilze a list to store the predictive labels
nb_predicted_set = []
rf_predicted_set = []
lr_predicted_set = []
for row in prediction_set: #for loop goes through each emailtext in the prediction set 
	row = [row] 
	transform = cv.transform(row) #transforming the emailtext you want tp predict using the cv
	svm_result = loaded_svm_model.predict(transform) #predicting using the transformed data 
	nb_result = loaded_nb_model.predict(transform)
	rf_result = loaded_rf_model.predict(transform)
	lr_result = loaded_lr_model.predict(transform)
	svm_predicted_set.append(svm_result) #adding to each list above
	nb_predicted_set.append(nb_result)
	rf_predicted_set.append(rf_result)
	lr_predicted_set.append(lr_result)


#svm confusion matrix

svm_confusion_matrix = confusion_matrix(y_true, svm_predicted_set, labels=['ham','spam'])
svm_sensitivity = svm_confusion_matrix[0,0]/(svm_confusion_matrix[0,0]+svm_confusion_matrix[0,1])
svm_specifity = svm_confusion_matrix[1,1]/(svm_confusion_matrix[1,0]+svm_confusion_matrix[1,1])

#nb confusion matrix

nb_confusion_matrix = confusion_matrix(y_true, nb_predicted_set, labels=['ham','spam'])
nb_sensitivity = nb_confusion_matrix[0,0]/(nb_confusion_matrix[0,0]+nb_confusion_matrix[0,1])
nb_specifity = nb_confusion_matrix[1,1]/(nb_confusion_matrix[1,0]+nb_confusion_matrix[1,1])

#rf confusion matrix

rf_confusion_matrix = confusion_matrix(y_true, rf_predicted_set, labels=['ham','spam'])
rf_sensitivity = rf_confusion_matrix[0,0]/(rf_confusion_matrix[0,0]+rf_confusion_matrix[0,1])
rf_specifity = rf_confusion_matrix[1,1]/(rf_confusion_matrix[1,0]+rf_confusion_matrix[1,1])

#lr confusion matrix

lr_confusion_matrix = confusion_matrix(y_true, lr_predicted_set, labels=['ham','spam'])
lr_sensitivity = lr_confusion_matrix[0,0]/(lr_confusion_matrix[0,0]+lr_confusion_matrix[0,1])
lr_specifity = lr_confusion_matrix[1,1]/(lr_confusion_matrix[1,0]+lr_confusion_matrix[1,1])


#Get scores for svm model
print('SVM')
print('confusion matrix for SVM')
print(str(svm_confusion_matrix))
print('accuracy of svm = ' + str(loaded_svm_model.score(cv.transform(x_test),y_test)))
print('precision of svm for ham and spam = ' + str(precision_score(y_true, svm_predicted_set, average=None)))
print('recall of svm for ham and spam = ' + str(recall_score(y_true, svm_predicted_set, average=None)))
print('sensitivity and specifity for svm model =' + str(svm_sensitivity) + ' ' + str(svm_specifity))
print('f1 score of svm for ham and spam = ' + str(f1_score(y_true, svm_predicted_set, average=None)))
print('**********************************************************************')

#Get scores for nb model
print('NAIVE BAYES')
print('confusion matrix for NB')
print(str(nb_confusion_matrix))
print('accuracy of nb = ' + str(loaded_nb_model.score(cv.transform(x_test),y_test)))
print('precision of nb for ham and spam = ' + str(precision_score(y_true, nb_predicted_set, average=None)))
print('recall of nb for ham and spam = ' + str(recall_score(y_true, nb_predicted_set, average=None)))
print('sensitivity and specifity for nb model =' + str(nb_sensitivity) + ' ' + str(nb_specifity))
print('f1 score of nb for ham and spam = ' + str(f1_score(y_true, nb_predicted_set, average=None)))
print('**********************************************************************')

#Get scores for rf model
print('RANDOM FOREST')
print('confusion matrix for RF')
print(str(rf_confusion_matrix))
print('accuracy of rf = ' + str(loaded_rf_model.score(cv.transform(x_test),y_test)))
print('precision of rf for ham and spam = ' + str(precision_score(y_true, rf_predicted_set, average=None)))
print('recall of rf for ham and spam = ' + str(recall_score(y_true, rf_predicted_set, average=None)))
print('sensitivity and specifity for rf model =' + str(rf_sensitivity) + ' ' + str(rf_specifity))
print('f1 score of rf for ham and spam = ' + str(f1_score(y_true, rf_predicted_set, average=None)))
print('**********************************************************************')

#Get scores for lr model
print('LOGISTIC REGRESSION')
print('confusion matrix for LR')
print(str(lr_confusion_matrix))
print('accuracy of lr = ' + str(loaded_lr_model.score(cv.transform(x_test),y_test)))
print('precision of lr for ham and spam = ' + str(precision_score(y_true, lr_predicted_set, average=None)))
print('recall of lr for ham and spam = ' + str(recall_score(y_true, lr_predicted_set, average=None)))
print('sensitivity and specifity for lr model =' + str(lr_sensitivity) + ' ' + str(lr_specifity))
print('f1 score of lr for ham and spam = ' + str(f1_score(y_true, lr_predicted_set, average=None)))
print('**********************************************************************')

#print(str(precision_recall_fscore_support(y_true, y_pred, average='macro')))

#this is where we insert single string and get svm + nb predictions
'''
email_text = ['You are a winner, you have won a free phone. Please signup at the following link. SALE SALE SALE FRIDAY FRIDAY. Text 50777']
transform = cv.transform(email_text)
result = loaded_svm_model.predict(transform)
result2 = loaded_nb_model.predict(transform)
result3 = loaded_rf_model.predict(transform)
result4 = loaded_lr_model.predict(transform)
print(result)
print(result2)
print(result3)
print(result4)
'''







































