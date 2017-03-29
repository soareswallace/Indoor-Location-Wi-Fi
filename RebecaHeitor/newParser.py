#!/usr/bin/python
#airodump parsing lib
#returns in an array of client and Ap information
#part of the airdrop-ng project
import pymongo
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from sys import exit as Exit
import subprocess



class airDumpParse:

    def parser(self,file,db,dict_manu, dictClientgeral):
        """
        One Function to call to parse a file and return the information
        """
        fileOpenResults = self.airDumpOpen(file)
        parsedResults   = self.airDumpParse(fileOpenResults)
        rtrnList    = self.jsonOut(parsedResults,db,dict_manu,dictClientgeral)
        return rtrnList
        # return parsedResults



    def findESSID(self, bssid, aplist):
        if bssid != 'null':
            for key in (aplist):
                if key == bssid:
                    ap = aplist[key]
                    if ap['essid']=='':
                        return bssid
                    else:
                        return ap['essid']
        return bssid

    def diffTime(self, data1, data2):
        totalseg1 = int(data1[6:]) + int(data1[3:5])*60 + int(data1[:2])*3600 #entrada nova do aircrack
        totalseg2 = int(data2[6:]) + int(data2[3:5])*60 + int(data2[:2])*3600
        # print "difftempo: ",totalseg1-totalseg2
        if (totalseg1-totalseg2<1200):
            return 1
        else:
            return 0

    
    def airDumpOpen(self,file):
        """
        Takes one argument (the input file) and opens it for reading
        Returns a list full of data
        """
        try:
            openedFile = open(file, "r")
        except IOError:
            print "Error Airodump File",file,"does not exist"
            Exit(1)
        data = openedFile.xreadlines()
        cleanedData = []
        for line in data:
            cleanedData.append(line.rstrip())
        openedFile.close()
        return cleanedData
    
    def airDumpParse(self,cleanedDump):
        """
        Function takes parsed dump file list and does some more cleaning.
        Returns a list of 2 dictionaries (Clients and APs)
        """
        try: #some very basic error handeling to make sure they are loading up the correct file
            try:
                apStart = cleanedDump.index('BSSID, First time seen, Last time seen, Channel, Speed, Privacy, Power, # beacons, # data, LAN IP, ESSID')
            except Exception:
                apStart = cleanedDump.index('BSSID, First time seen, Last time seen, channel, Speed, Privacy, Cipher, Authentication, Power, # beacons, # IV, LAN IP, ID-length, ESSID, Key')
            del cleanedDump[apStart]            #remove the first line of text with the headings
            try:
                stationStart = cleanedDump.index('Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs')
            except Exception:
                stationStart = cleanedDump.index('Station MAC, First time seen, Last time seen, Power, # packets, BSSID, ESSID')
        except Exception:
            print "You Seem to have provided an improper input file please make sure you are loading an airodump txt file and not a pcap"
            Exit(1)
    
        del cleanedDump[stationStart]           #Remove the heading line
        clientList = cleanedDump[stationStart:] #Splits all client data into its own list
        del cleanedDump[stationStart:]          #The remaining list is all of the AP information
        apDict = self.apTag(cleanedDump)
        clientDict = self.clientTag(clientList)
        resultDicts = [clientDict,apDict]       #Put both dictionaries into a list
        return resultDicts
    
    def apTag(self,devices):
        """
        Create a ap dictionary with tags of the data type on an incoming list
        """
        dict = {}
        for entry in devices:
            ap = {}
            string_list = entry.split(',')
            #sorry for the clusterfuck but i swear it all makse sense this is builiding a dic from our list so we dont have to do postion calls later

            len(string_list)
            if len(string_list) == 15:
                ap = {"bssid":string_list[0].replace(' ',''),
                    "fts":string_list[1],
                    "lts":string_list[2],
                    "channel":string_list[3].replace(' ',''),
                    "speed":string_list[4],
                    "privacy":string_list[5].replace(' ',''),
                    "cipher":string_list[6],
                    "auth":string_list[7],
                    "power":string_list[8],
                    "beacons":string_list[9],
                    "iv":string_list[10],
                    "ip":string_list[11],
                    "id":string_list[12],
                    "essid":string_list[13][1:],
                    "key":string_list[14]}
            elif len(string_list) == 11:
                ap = {"bssid":string_list[0].replace(' ',''),
                    "fts":string_list[1],
                    "lts":string_list[2],
                    "channel":string_list[3].replace(' ',''),
                    "speed":string_list[4],
                    "privacy":string_list[5].replace(' ',''),
                    "power":string_list[6],
                    "beacons":string_list[7],
                    "data":string_list[8],
                    "ip":string_list[9],
                    "essid":string_list[10][1:]}
            if len(ap) != 0:
                dict[string_list[0]] = ap
                
        return dict
    
    def clientTag(self,devices):
        """
        Create a client dictionary with tags of the data type on an incoming list
        """
        dict = {}
        for entry in devices:
            client = {}
            string_list = entry.split(',')
            if len(string_list) >= 7:
                client = {"station":string_list[0].replace(' ',''),
                    "fts":string_list[1],
                    "lts":string_list[2],
                    "power":string_list[3],
                    "packets":string_list[4],
                    "bssid":string_list[5].replace(' ',''),
                    "probe":string_list[6:][0:]}
            if len(client) != 0:
                dict[string_list[0]] = client
                
        return dict
    
    def jsonOut(self, data,db,dict_manu,dictClientgeral):
        clients = data[0]
        AP = data[1]
        NA = [] #create a var to keep the not associdated clients
        NAP = [] #create a var to keep track of associated clients to AP's we cant see
        apCount = {} #count number of Aps dict is faster the list stored as BSSID:number of essids
        apClient = {} #dict that stores bssid and clients as a nested list
        
        c=1
        # print(len(clients))
        # print dictClientgeral
        for key in (clients):
            present = False
            
            mac = clients[key] #mac is the MAC address of the client
            dia = mac['fts'][1:11]
            saida = mac['lts'][1:]
            power = mac['power'][1:]
            entrada = mac['fts'][12:]
            saida = mac['lts'][12:]
            if mac['probe'][0]=='':
                mac['probe']=['null']
            
            aux = 0
            redes = mac['probe']
            # redes = mac['probe']
            rede_atual = mac['bssid']
            if rede_atual =='(notassociated)':
                rede_atual = 'null'
                
            mac = mac['station']
            #print mac
            
            essid = self.findESSID(rede_atual,AP)
            first_seen=str(dia)+"T"+str(entrada);
            last_seen = str(dia)+"T"+str(saida);

            if(dictClientgeral.has_key(mac) == True):

                n_saida = dictClientgeral[mac]["lastSeen"]
                id_mongo = dictClientgeral[mac]["_id"]
                present = True

                # print "do mac ", mac, " a saida ant: ", n_saida ," a saida ag: ", saida


                if self.diffTime(saida,n_saida[11:19]):
                    v = db.device.find({"_id":ObjectId(id_mongo)})
                    v = v[0]
                    # print 'update', id_mongo
                    # print "mac: ", v["stationMac"], " atualiza ", v["lastSeen"], " para: ", saida

                    db.device.update({'_id' : ObjectId(id_mongo)},{"$set" : {'lastSeen' : last_seen}},upsert=False,multi=True)
                    db.device.update({'_id' : ObjectId(id_mongo)},{"$set" : {'power' : power}},upsert=False,multi=True)
                    
                    vet = v["probedSSID"]
                    
                    for net in redes:
                        if (not(str(net) in v["probedSSID"])):
                            if vet =="null":
                                vet = [net]
                            else:
                                vet = vet + [str(net)]

                    db.device.update({'stationMac' : mac},{'$set' : {'probedSSID' : vet}},False,True)
                else:
                    present= False
                    del dictClientgeral[mac]
            else:
                present = False
                
            
            if present == False:
                #print "inseriu: ", mac
                manufacturer = dict_manu.get(mac[:2]+mac[3:5]+mac[6:8])
                if manufacturer is None:
                    manufacturer="UNKNOWN"
                        
                ret = db.device.insert({'stationMac':mac,'firstSeen':first_seen,'lastSeen':last_seen,'power':power,'probedSSID':redes,'currentApBSSID':rede_atual,'currentApESSID':essid, 'riotId':'1','manufacturer':manufacturer})
                
                dictClientgeral[mac] = {"mac":mac, "lastSeen":last_seen, "_id": str(ret)}

                # print "inseriu: ", mac

            
        return dictClientgeral
    
def openMonitorMode():

    lineMonitorMode = "airmon-ng start wlan0"
    monitorMode = subprocess.Popen(lineMonitorMode, stdout = subprocess.PIPE, shell = True)

def runAirodumpAndKill():
    airoCommandLine = "airodump-ng wlan0mon --write tt.csv --output-format csv --write-interval 2"
    airodump = subprocess.Popen("exec " + airoCommandLine,stdout=subprocess.PIPE,shell=True)

    time.sleep(30)

    airodump.terminate()
    airodump.kill()


if __name__ == "__main__":

    banco_riot = "wifiCesar"
    
    inputfile = open("oui.txt","r")
    data = inputfile.read()

    entries = data.split("\n\n")[1:-1]
    dict_manu = {}
    for entry in entries:
        parts = entry.split("\n")[1].split("\t")
        company_id = parts[0].split()[0]
        company_name = parts[-1]
        dict_manu[company_id] = company_name

    openMonitorMode()
    dic = {}
    dictClientgeral = {}
    
    ip = raw_input("Digite o ip ou localhost para local: ")

    if(ip == "localhost"):
       connection_riot = MongoClient()
    
    else:
        connection_riot = MongoClient(ip, 8125)
        
    riotdb = connection_riot[banco_riot]
    device = riotdb['device']
    
    removeCommandLine = "rm tt.csv-01.csv"
    remove = subprocess.Popen(removeCommandLine,stdout=subprocess.PIPE,shell=True)
    # usuarioNome = "riotdb"
    # connection = MongoClient()
    # db = connection.riotdb
    p = airDumpParse()
    # p.parser("tt.csv-01.csv",riotdb)
    
    while(True):

        runAirodumpAndKill()

        p = airDumpParse()
        dic = p.parser("tt.csv-01.csv",riotdb,dict_manu,dictClientgeral)
        dictClientgeral = dic

        removeCommandLine = "rm tt.csv-01.csv"
        remove = subprocess.Popen(removeCommandLine,stdout=subprocess.PIPE,shell=True)
        # # print "cabou"
        # raw_input()
