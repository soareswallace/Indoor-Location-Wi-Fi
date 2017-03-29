# README #

## Projeto de trackeamento! ##

Necessário o aircrak:
**Instalando:**
  1. sudo apt-get install build-essential
  2. sudo apt-get install libssl-dev 
  3. sudo apt-get install libnl-3-dev libnl-genl-3-dev 
  4. wget http://download.aircrack-ng.org/aircrack-ng-1.2-rc4.tar.gz
  5. tar -zxvf aircrack-ng-1.2-rc4.tar.gz
  6. cd aircrack-ng-1.2-rc4
  7. sudo make
  8. sudo make install

**Testando**
  Executa antes: 1.sudo service network-manager stop
  2.Sudo airmon-ng start wlan0 
  3.sudo airodump-ng wlan0mon

**para parar:**
  1.Sudo airmon-ng stop wlan0mon

Se a interface wifi sumir, executa: sudo service network-manager start