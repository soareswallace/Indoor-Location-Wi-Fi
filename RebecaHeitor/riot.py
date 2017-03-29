#Codigo que ira rodar nos riots

import subprocess
import time
from pymongo import MongoClient

def vectorFile(file):
    try:
            openedFile = open(file, "r")
    except IOError:
        print "Error File",file,"does not exist"
        Exit(1)

    data = openedFile.xreadlines()
    cleanedData = []
    for line in data:
        cleanedData.append(line.rstrip())

    openedFile.close()
    return cleanedData

def readVector(data):
    dicionario = {}

    for line in data:
        l=line.split(',')
        # print l
        power1 = l[2]
        mac = l[0]
        if(mac != ""):
            mac = mac[1:18]                  #Tirando as aspas da entrada
            power1 = power1[1:len(power1)]    #Idem
            if power1!='':
                if(dicionario.has_key(mac)):#Se existir o mac, adiciona ao vetor
                    p = dicionario[mac]
                    dicionario[mac] = p + [power1]
                else:
                    dicionario[mac] = [power1]      #senao insere 

            # print power1
            # print mac
            # raw_input()             

            # print dicionario[mac]
        # else:
        #     print "no mac"
    # print dicionario
    return dicionario     
        #"34:bb:26:ac:f6:fe",,"-57","Apr 25, 2016 10:06:00.883871000"

# def insertDatabase(dicionario, db):
#     for line in dicionario:
#         db.riot1.insert({'mac:'line[mac],'power':[dicionario[po]]})
        

if __name__ == "__main__":
    aux = 0
    banco_riot = "riotdb"
    connection_riot = MongoClient()
    db = connection_riot["riotdb"]

    while (1):
        # TsharkCommand = "sudo tshark -S -l -i wlan0mon  -T fields -e wlan.sa -e wlan_mgt.ssid -e radiotap.dbm_antsignal -e frame.time -E separator=, -E quote=d >> file.txt"
        # Tshark = subprocess.Popen("exec " + TsharkCommand,stdout=subprocess.PIPE,shell=True)
        # time.sleep(60)
        # Tshark.terminate()
        # Tshark.kill()
        # print "aux"
        # ++aux
        cleanData = vectorFile('file.txt');
        dic = readVector(cleanData)
        for d in dic:
            db.riot1.insert({'mac':d, 'power':dic[d]})
        #deleta o file
        # removeCommandLine = "rm file.txt"
        # remove = subprocess.Popen(removeCommandLine,stdout=subprocess.PIPE,shell=True)
        wait = db.go.find({'_id':1})[0]['value'] #se puder capturar novamente go vai esta com 1
        while(not wait):
            print "aqui"
            wait = db.go.find({'_id':1})[0]['value']
        # print(len(cleanData))
        print "SAIUUU"
        raw_input()