import subprocess
import time


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
        power1 = l[2]
        mac = l[0]
        if(mac != ""):
            mac = mac[1:18]                     #Tirando as aspas da entrada
            power1 = power1[1:len(power1)-1]    #Idem

            if(dicionario.has_key(mac) == True):#Se existir o mac, adiciona ao vetor
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

    return dicionario     
        #"34:bb:26:ac:f6:fe",,"-57","Apr 25, 2016 10:06:00.883871000"

if __name__ == "__main__":
    aux = 0
    mac = "34:BB:26:AC:F6:FE"
    while (1):
        mac = "34:BB:26:AC:F6:FE"
        # TsharkCommand = "sudo tshark -S -l -i wlan0mon -Y \"wlan.sa == "+mac+"\" -T fields -e wlan.sa -e wlan_mgt.ssid -e radiotap.dbm_antsignal -e frame.time -E separator=, -E quote=d >> file"+str(aux)+".txt"
        # Tshark = subprocess.Popen("exec " + TsharkCommand,stdout=subprocess.PIPE,shell=True)
        # time.sleep(60)
        # Tshark.terminate()
        # Tshark.kill()
        # print "aux"
        # ++aux
        cleanData = vectorFile('/home/heitor/file01.txt');
        dic = readVector(cleanData)
        print dic
        # print(len(cleanData))
        raw_input()