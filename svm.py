import extract as extract
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
import seaborn as sns
from sklearn import metrics

def build_train(filename):
	extracted = extract.extract(filename)
	train_x = []
	train_y = [] 
	for example in extracted:
		similarity = cosine_similarity(example["reference"],example["candidate"])
		train_x.append([float(example["bleu"]),float(similarity)])
		train_y.append(0 if example["label"] == "H" else 1)
	return np.array(train_x), np.array(train_y)

def build_test(filename):
	extracted = extract.extract(filename)
	test_x = []
	test_y = []
	for example in extracted:
		similarity = cosine_similarity(example["reference"],example["candidate"])
		test_x.append([float(example["bleu"]),float(similarity)])
		test_y.append(0 if example["label"] == "H" else 1)
	return np.array(test_x), np.array(test_y)
	
def cosine_similarity(x,y):
	# tokenization 
	X_list = word_tokenize(x)  
	Y_list = word_tokenize(y)   
	l1 =[];l2 =[]  
	X_set = set(X_list)
	Y_set = set(Y_list)
	# form a set containing keywords of both strings  
	rvector = X_set.union(Y_set)  
	for w in rvector: 
	    if w in X_set: l1.append(1) # create a vector 
	    else: l1.append(0) 
	    if w in Y_set: l2.append(1) 
	    else: l2.append(0) 
	c = 0
	# cosine formula  
	for i in range(len(rvector)): 
	        c+= l1[i]*l2[i] 
	cosine = c / float((sum(l1)*sum(l2))**0.5) 
	return cosine

'''
Support Vector Machine:
	- Input: (1) Bleu Score, (2) Cosine Similarity
'''
def svm_train(clf):
	train_data_x, train_data_y = build_train("train.txt")
	clf.fit(train_data_x, train_data_y)
	return clf

def predict(clf):
	test_data_x, test_data_y = build_test("test.txt")
	predicted = []
	for sample in test_data_x:
		proc_sample = np.array([list(sample)])
		print(proc_sample)
		pred = clf.predict(proc_sample)[0]
		predicted.append(pred)
	return predicted, test_data_y


def predict_train_data(clf):
	train_data_x, train_data_y = build_train("train.txt")
	predicted = []
	for sample in train_data_x:
		proc_sample = np.array([list(sample)])
		print(proc_sample)
		pred = clf.predict(proc_sample)[0]
		predicted.append(pred)
	return predicted, train_data_y


def accuracy(ground_truth, prediction):
	total = len(ground_truth)
	correct = 0
	for i in range(total):
		if ground_truth[i] == prediction[i]:
			correct += 1
	return float(correct)/total

def f1score(ground_truth, prediction, average='macro'):
	return f1_score(ground_truth, prediction)

def classify():
	clf = svm.SVC()
	clf = svm_train(clf)
	pred, ground_truth = predict(clf)
	pred_train, ground_truth_train = predict_train_data(clf)
	print(pred)
	acc = accuracy(ground_truth,pred)
	acc_train =  accuracy(ground_truth_train,pred_train)
	print("The Test % Accuracy is: " + str(float(acc*100)) + "%")
	print("The Test F1 Score computed using Sklearn is: " + str(f1score(ground_truth, pred)))
	print("The Train % Accuracy is: " + str(float(acc_train*100)) + "%")
	print("The Train F1 Score computed using Sklearn is: " + str(f1score(ground_truth_train, pred_train)))
	cm = metrics.confusion_matrix(ground_truth, pred)
	cm_train = metrics.confusion_matrix(ground_truth_train,pred_train)
	print(cm)
	print(cm_train)
	plot_cm(acc, cm)
	plot_cm(acc_train, cm_train)


def plot_cm(acc, cm):
	plt.figure(figsize=(9,9))
	sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r')
	plt.ylabel('Actual label')
	plt.xlabel('Predicted label')
	all_sample_title = 'Accuracy Score: {0}'.format(acc)
	plt.title(all_sample_title, size = 15)
	plt.show()


classify()















