import numpy as np
import csv
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import subprocess
import time
from pymongo import MongoClient

def openCsvFile(filename, cabecalho):

    file = open(filename, "rb")     #Abre arquivo
    csvFile = csv.reader(file)      #converte pra csv

    dataCsv = []
    dicionario = {}

    for i in csvFile:               #Passa pra vetor
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
    #                                             riot1: {-30,-27,-30, ... ,-32}
    #                                             riot2: {vetor de potencias do riot2 para cada setor}
    #                                             riot3: {vetor de potencias do riot3 para cada setor}                      

    
    return dicionario

def prepData(dicionario):
    X = []
    y = []

    for i in dicionario["setor"]:
        k = int(i)
        X.append( [dicionario["riot1"][k-1]] + [dicionario["riot2"][k-1]]+ [dicionario["riot3"][k-1]] )
        y = y + [k]

    return X,y

def dataKNN(X,y, vec_device):
    neigh = KNeighborsClassifier(n_neighbors=1)
    knn = neigh.fit(X, y)
    out = knn.predict([vec_device])

    return out

if __name__ == "__main__":
    banco_riot = "riotdb"
    connection_riot = MongoClient()
    db = connection_riot["riotdb"]
    dicionario = openCsvFile("dataPower.csv", True)
    print dicionario
    X,y = prepData(dicionario)

    #para cada device pego pelo riot1
    for device in db.riot1.find():
        mac = device['mac']
        power_r1 = device['power'][0:10] #vetor de power do mac pego pelo riot1
        device2 = db.riot2.find_one({'mac':mac})
        power_r2 = [0]
        if device2 != None:
            power_r2 = device2['power'][0:10] #vetor de power do mac pego pelo riot2
        device3 = db.riot3.find_one({'mac':mac})
        power_r3 = [0]
        if device3 != None:
            power_r3 = device3['power'][0:10] #vetor de power do mac pego pelo riot3

        media1 = 0
        for p1 in power_r1:
            media1 = media1+p1

        media1 = media1/len(power_r1)

        media2 = 0
        for p2 in power_r2:
            media2 = media2+p2

        media2 = media2/len(power_r2)

        media3 = 0
        for p3 in power_r3:
            media3 = media3+p3

        media3 = media3/len(power_r3)

        print media1, media2, media3
        outKnn = dataKNN(X,y,[media1,media2,media3])
        print "Mac: ",mac, "Regiao: ",outKnn
        raw_input()
