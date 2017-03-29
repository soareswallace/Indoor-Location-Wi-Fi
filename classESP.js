var method = Esp.prototype;
function Esp (mac, ap, distancia,timeSent, fabricante, temTudo) { //classe dos ESP
    this.mac = mac;
    this.apName = ap;
    if(ap == "ap1"){
        this.distanceFromAp1 = distancia;

    }
    if(ap == "ap2"){
        this.distanceFromAp2 = distancia;
    }
    if(ap == "ap3"){
        this.distanceFromAp3 = distancia;
    }
    this.timeSent = timeSent;
    this.fabricante = fabricante;
    this.hasAllDataForDistance = temTudo;
    this.getMac = function() {
        return this.mac;
    };
    this.getApName = function() {
        return this.apName;
    };
    this.getDistanceFromAp1 = function() {  
        return this.distanceFromAp1;
    };
    this.getDistanceFromAp2 = function() {
        return this.distanceFromAp2;
    };

    this.getDistanceFromAp3 = function() {
        return this.distanceFromAp3;
    };

    this.getFabricante = function() {
        return this.fabricante;
    };

    this.gettimeSent = function() {
        return this.timeSent;
    };

    this.gethasAllDataForDistance = function() {
        return this.hasAllDataForDistance;
    };
////////////////////////////////////////////////////////////////
    this.settimeSent = function(newtimeSent) {
        return this.timeSent;
    };

    this.equalsMac = function(macSended){
    	if(this.mac == macSended){
    		return true;
    	}
    }
    this.showInfo = function(){
    	return 'MAC: ' + this.mac + '\nDistancia para o AP1: ' + this.distanceFromAp1 + '\n' + 'Distancia para o AP2: ' + this.distanceFromAp2 + '\nDistancia para o AP3: ' + this.distanceFromAp3 + '\nTime Sent:' + this.timeSent + '\n' + "Fabricante: " + fabricante + '\n' ;
    }

    this.updateSignal = function(newEsp){
     //   console.log("Debug -> Nome do AP: " + newEsp.getApName());
        //console.log("POTENCIA QUE VEM " + newEsp.getAp3Power());
        //console.log("TIME: " + newEsp.gettimeSent());
        if(newEsp.getApName()=="ap1"){
            //console.log("\n\nVEIO PARA MIM" + newEsp.getAp3Power() + "\n\nPRECISO TROCAR" + this.ap3Power + "\n\n");
            this.distanceFromAp1 = newEsp.getDistanceFromAp1();
            this.timeSent = newEsp.gettimeSent();
            //console.log("POTENCIA " + this.ap3Power);
        }
        else if(newEsp.getApName()=="ap2"){
            //console.log("\n\nVEIO PARA MIM" + newEsp.getAp3Power() + "\n\nPRECISO TROCAR" + this.ap3Power + "\n\n");
            this.distanceFromAp2 = newEsp.getDistanceFromAp2();
            this.timeSent = newEsp.gettimeSent();
            //console.log("POTENCIA " + this.ap3Power);
        }
        else if(newEsp.getApName()=="ap3"){
            //console.log("\n\nVEIO PARA MIM" + newEsp.getAp3Power() + "\n\nPRECISO TROCAR" + this.ap3Power + "\n\n");
            this.distanceFromAp3 = newEsp.getDistanceFromAp3();
            this.timeSent = newEsp.gettimeSent();
            //console.log("POTENCIA " + this.ap3Power);
        }
        else{
            console.log("ERROR UPDATE_SIGNAL: NAO ENCONTREI STRING COMPATIVEL\n\n");
        }
        if(this.distanceFromAp1 != null && this.distanceFromAp2 != null && this.distanceFromAp3 != null){
            this.hasAllDataForDistance = true;
        }
    }
}

module.exports = Esp;