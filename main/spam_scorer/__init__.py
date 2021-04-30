import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import pickle


#SVM function with email string as input and spam score as output
#This function is something that can be called. One parameter goes through called emaitext it scores the score the emailtet and gives back ham or spam
def score_svm(email_text):
	##Step1: Load Dataset
	dataframe = pd.read_csv(r"C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\spam.csv")
	print('Scoring emails with svm model')
	##Step2: Split in to Training and Test Data
	x = dataframe["EmailText"]
	y = dataframe["Label"]

	x_train,y_train = x[0:4457],y[0:4457]
	x_test,y_test = x[4457:],y[4457:]

	#loads and opens the cv and the model from the pickle file holding them and then give a prediction and returns from the function
	cv = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\cv.pkl', 'rb'))
	loaded_svm_model = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\svm_model.pkl', 'rb'))
	transform = cv.transform(email_text)
	result = loaded_svm_model.predict(transform)

	return result

#Logisitic Regression function with email string as input and spam score as output

def score_lr(email_text):
	#Step1: Load Dataset
	dataframe = pd.read_csv(r"C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\spam.csv")
	print('Scoring emails with lr model')
	
	#Step2: Split in to Training and Test Data
	x = dataframe["EmailText"]
	y = dataframe["Label"]

	x_train,y_train = x[0:4457],y[0:4457]
	x_test,y_test = x[4457:],y[4457:]

	cv = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\cv.pkl', 'rb'))
	loaded_lr_model = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\lr_model.pkl', 'rb'))
	transform = cv.transform(email_text)
	result = loaded_lr_model.predict(transform)

	return result

#Random Forest function with email string as input and spam score as output

def score_rf(email_text):
	#Step1: Load Dataset
	dataframe = pd.read_csv(r"C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\spam.csv")
	print('Scoring emails with rf model')
	
	#Step2: Split in to Training and Test Data
	x = dataframe["EmailText"]
	y = dataframe["Label"]

	x_train,y_train = x[0:4457],y[0:4457]
	x_test,y_test = x[4457:],y[4457:]

	cv = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\cv.pkl', 'rb'))
	loaded_rf_model = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\rf_model.pkl', 'rb'))
	transform = cv.transform(email_text)
	result = loaded_rf_model.predict(transform)

	return result

#Naive Bayes function with email string as input and spam score as output

def score_nb(email_text):
	#Step1: Load Dataset
	dataframe = pd.read_csv(r"C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\spam.csv")
	print('Scoring emails with nb model')
	
	#Step2: Split in to Training and Test Data
	x = dataframe["EmailText"]
	y = dataframe["Label"]

	x_train,y_train = x[0:4457],y[0:4457]
	x_test,y_test = x[4457:],y[4457:]

	cv = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\cv.pkl', 'rb'))
	loaded_nb_model = pickle.load(open(r'C:\Users\C00230058\Desktop\HazelsProject\main\spam_scorer\nb_model.pkl', 'rb'))
	transform = cv.transform(email_text)
	result = loaded_nb_model.predict(transform)

	return result

'''
##Step1: Load Dataset
dataframe = pd.read_csv("spam.csv")
print(dataframe.describe())

##Step2: Split in to Training and Test Data

x = dataframe["EmailText"]
y = dataframe["Label"]

x_train,y_train = x[0:4457],y[0:4457]
x_test,y_test = x[4457:],y[4457:]


##Step3: Extract Features
cv = CountVectorizer()


#Everything below has been used to train the models and dump the models into two seperate pickle files

cv.fit(x_train)
features = cv.transform(x_train)

##Step4: Initiate and build different models
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


cv = pickle.load(open(cv_file, 'rb'))
loaded_svm_model = pickle.load(open(svm_file, 'rb'))
loaded_nb_model = pickle.load(open(nb_file, 'rb'))
loaded_rf_model = pickle.load(open(rf_file, 'rb'))
loaded_lr_model = pickle.load(open(lr_file, 'rb'))


#Step5: Test Accuracy on svm model + nb model

print(loaded_svm_model.score(cv.transform(x_test),y_test))
print(loaded_nb_model.score(cv.transform(x_test),y_test))
print(loaded_rf_model.score(cv.transform(x_test),y_test))
print(loaded_lr_model.score(cv.transform(x_test),y_test))


#this is where we insert single string and get svm + nb predictions
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