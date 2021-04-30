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
print(dataframe.describe())

##Step2: Split in to Training and Test Data

x = dataframe["EmailText"] #column label
y = dataframe["Label"]

x_train,y_train = x[0:4457],y[0:4457] #4457 rows to training set remaining to test set
x_test,y_test = x[4457:],y[4457:]



##Step3: Extract Features
cv = CountVectorizer()


#The CV fits the emailtext data and then trnasforms the data into vectorized features

cv.fit(x_train)
features = cv.transform(x_train)

##Step4: Initiate and build different models

tuned_parameters = {'kernel': ['rbf','linear'], 'gamma': [1e-3, 1e-4], #set of parameters for SVM
                     'C': [1, 10, 100, 1000]}

#Initzliae ski-learn 
model = GridSearchCV(svm.SVC(), tuned_parameters)
model2 = MultinomialNB()
model3 = RandomForestClassifier(n_estimators=100)
model4 = LogisticRegression()

#Giving each feature the emailtext data and labels
model.fit(features,y_train)
model2.fit(features, y_train)
model3.fit(features, y_train)
model4.fit(features, y_train)



#initiate pickle file names
cv_file = 'cv.pkl'
svm_file = 'svm_model.pkl'
nb_file = 'nb_model.pkl'
rf_file = 'rf_model.pkl'
lr_file = 'lr_model.pkl'


#dump models into pickle files for quick access
pickle.dump(cv, open(cv_file, 'wb'))
print('CV has loaded')
pickle.dump(model, open(svm_file, 'wb'))
pickle.dump(model2, open(nb_file, 'wb'))
pickle.dump(model3, open(rf_file, 'wb'))
pickle.dump(model4, open(lr_file, 'wb'))
print('models are loaded')









































