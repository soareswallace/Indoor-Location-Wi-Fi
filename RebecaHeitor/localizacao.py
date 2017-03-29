import numpy as np
import csv
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

def openCsvFile(filename, cabecalho):

	file = open(filename, "rb") 	#Abre arquivo
	csvFile = csv.reader(file)		#converte pra csv

	dataCsv = []
	dicionario = {}

	for i in csvFile:				#Passa pra vetor
		dataCsv.append(i)

	
	if cabecalho:
		header=dataCsv.pop(0)
		
		for d in dataCsv:
			for i in xrange(len(header)):
				if(dicionario.has_key(header[i]) == True):
					p = dicionario[header[i]]
					
					dicionario[header[i]] = p + [int(d[i])]
				else:
					dicionario[header[i]]= [int(d[i])] 
					
	else:
		for i in xrange(len(dataCsv[0])):
			dicionario[i]=i;

	#O resultado desse bloco eh um dicionario com setores : { 1, 2, 3, ... , 25} -> 25 setores
	#											  riot1: {-30,-27,-30, ... ,-32}
	#											  riot2: {vetor de potencias do riot2 para cada setor}
	#											  riot3: {vetor de potencias do riot3 para cada setor}						

	
	return dicionario

def prepData(dicionario):
	X = []
	y = []

	for i in dicionario["setor"]:
		k = int(i)
		X.append( [dicionario["riot1"][k-1]] + [dicionario["riot2"][k-1]]+ [dicionario["riot3"][k-1]] )
		y = y + [k]

	return X,y

def dataSVR(X,y):

	svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

	y_rbf = svr_rbf.fit(X, y).predict([[-48,-48,-38]])

	out = []
	for i in y_rbf:
		out.append(round(i)) 

	return out

def dataSVM(X,y):

	clf = SVC()

	svm = clf.fit(X, y)  

	out = svm.predict([[-48,-48,-38]])

	return out


def dataKNN(X,y):
	neigh = KNeighborsClassifier(n_neighbors=1)
	knn = neigh.fit(X, y)

	out = knn.predict([[-48,-48,-38]])

	return out

def main():	
	dicionario = openCsvFile("dataPower.csv", True)

	X,y = prepData(dicionario)

	outSVR = dataSVR(X,y)

	print "Saida para SVR"
	print outSVR			#Resultado ruim - pode ignorar

	outKnn = dataKNN(X,y)
	print "Saida para KNN"
	print outKnn

	print "Saida para SVM"
	outSVM = dataSVM(X,y)
	print outSVM


	# plt.scatter(X, y, c='k', label='data')
	# # plt.hold('on')
	# # plt.plot(X, y_rbf, c='g', label='RBF model')
	# plt.xlabel('data')
	# plt.ylabel('target')
	# plt.title('Support Vector Regression')
	# plt.legend()
	# plt.show()


main()