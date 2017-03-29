var 	express         =   require("express"),
    	app             =   express();
    	ejs 			= 	require("ejs"),
    	moment			=	require("moment"),
    	mongoose 		= 	require("mongoose");
        Esp             =   require("./classESP.js");

var trilat = require('trilat'); 
var power1;
var power2;
var power3;
var devices = [new Esp()];


var http = require('http').Server(app);
var io = require('socket.io')(http);

// APP CONFIG
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').renderFile);
app.use(express.static(__dirname + "/public"));

moment().locale("pt-BR");
moment().format();

mongoose.Promise = global.Promise;                  // use this line to get rid of deprecated promises

mongoose.connect("mongodb://localhost/riotdb"); 	// loading riotdb

// Schema setup
var deviceSchema = new mongoose.Schema({
    mac: String,
    Distance_para_o_Ap1: { type: Number, default: 0},
    Distance_para_o_Ap2: { type: Number, default: 0},
    Distance_para_o_Ap3: { type: Number, default: 0},
    fabricante: { type: String, default: 'undefined'},
    timeSent: { type: Date, default: Date.now()}
});

var Device = mongoose.model("Device", deviceSchema);



// Packets Server

var espToFind = "18:FE:34:D6:EA:8E";

var esps = new Array();





// ------------- RESTful ROUTES ---------------
app.get("/", function(req, res){
    res.render("index", {pageClass: "home"});
});

app.get("/send", function(req, res){
    res.render("send");
});

app.get("/colaboradores", function(req, res){
    res.render("colaboradores", {pageClass: "colaboradores"});
});

app.get("/mapa", function(req, res){
    res.render("mapa", {pageClass: "mapa"});
});

app.get("/mapa2", function(req, res){
	res.render("mapa2", {trilat: trilat, pageClass: "mapa"});
});

function addDevice(newEsp){
    //console.log("AQUI PORRA " + newEsp.showInfo());
        var novoEsp = new Device({
            
            mac: newEsp.getMac(),
            Distance_para_o_Ap1: newEsp.getDistanceFromAp1(),
            Distance_para_o_Ap2: newEsp.getDistanceFromAp2(),
            Distance_para_o_Ap3: newEsp.getDistanceFromAp3(),
            fabricante: newEsp.getFabricante(),
            timeSent: newEsp.gettimeSent()

        });

        var qual_foi_o_AP = newEsp.getApName();
        var query = {"mac": newEsp.getMac()};


        Device.findOne(query, function(err, data){
            if(err){
                console.log(err);
            }
            if(data){
                console.log("\nTamanho do array : " + devices.length + "\n");
                //console.log("ENTREI" + data);
                if(qual_foi_o_AP == "ap1"){
                    var update = {"Distance_para_o_Ap1": newEsp.getDistanceFromAp1()};
                    Device.update(query, update, function(err, done){
                        if(err){
                            console.log(err);
                        }
                        if(done){
                            console.log("\nBanco atualizado!\n");
                        }
                    });
                }
                if(qual_foi_o_AP == "ap2"){
                    var update = {"Distance_para_o_Ap2": newEsp.getDistanceFromAp2()};
                    Device.update(query, update, function(err, done){
                        if(err){
                            console.log(err);
                        }
                        if(done){
                            console.log("\nBanco atualizado!\n");
                        }
                    });   
                }
                if(qual_foi_o_AP == "ap3"){
                    var update = {"Distance_para_o_Ap3": newEsp.getDistanceFromAp3()};
                    Device.update(query, update, function(err, done){
                        if(err){
                            console.log(err);
                        }
                        if(done){
                            console.log("\nBanco atualizado!\n");
                        }
                    });
                }
            }
            if(!data){
                novoEsp.save(function(err,data){
                    if(err){
                        console.log(err);
                    }
                    else{
                        console.log("Saved: " + data);
                        devices.push(newEsp);
                        console.log("\nTamanho do array : " + devices.length + "\n");
                    }
                });
            }
        });

    }

    function distFromSignalAp1(level) {

        const A = -56; //dBm 1m of distance 
        const n = 1.287; // constante de propagação no meio.
        var rssi = level;
        console.log("level: " + level);
        var aux = (rssi - A) / (-10 * n);
        var dist = Math.pow(10, aux);
        console.log("Distancia: " + dist);
        return dist.toString();

    }

    function distFromSignalAp2(level) {

        const A = -41; //dBm 1m of distance 
        const n = 2.432; // constante de propagação no meio.
        var rssi = level;
        console.log("level: " + level);
        var aux = (rssi - A) / (-10 * n);
        var dist = Math.pow(10, aux);
        console.log("Distancia: " + dist);
        return dist.toString();

    }

    function distFromSignalAp3(level) {

        const A = -40; //dBm 1m of distance 
        const n = 2.003// constante de propagação no meio.
        var rssi = level;

        console.log("level: " + level);
        var aux = (rssi - A) / (-10 * n);
        var dist = Math.pow(10, aux);
        console.log("Distancia: " + dist);
        return dist.toString();

    }

    function distanceBetweenTwoPoints(point1, point2){
        var deltaX = point1[0]-point2[0];
        var deltaY = point1[1]-point2[1];
        var distanciaEntrePontos = Math.pow(deltaX,2) + Math.pow(deltaY, 2);
        distanciaEntrePontos = Math.sqrt(distanciaEntrePontos);
        return distanciaEntrePontos;
    }

    function positionInMap(distance1, distance2, distance3){
        distance1 = distance1*100;
        distance2 = distance2*100;
        distance3 = distance3*100;
        var input = [
                //      X       Y       R 
                    [940.0,     750.0,  distance1],
                    [635.0,     130.0,  distance2],
                    [0.0,      0.0,  distance3]
                ];
        var output = trilat(input);
        return output;
    }


//const MAX_RSSI = -34; //dBm
//const MIN_RSSI = -76; //dBm
//const RANGE = MAX_RSSI - MIN_RSSI;
// Received signal strength at 1 metre
var comando = '0';
var cont = 0;
io.on('connection', function(socket){
    console.log(socket.handshake.address);
    // socket.on('comando', function(msg){
    //     console.log(msg);
    //     console.log(msg instanceof Object);
    //     var comando = '1';
    //     socket.emit('comando', comando);
    //     cont++;
    //     if(cont==5){
    //         comando = '0';
    //         socket.emit('comando', comando);
    //         cont = 0;
    //     }
    // });
    socket.on('comando', function(msg){
        console.log('Client:', msg);
        var output;

        console.log(msg instanceof Object);
        if(!(msg instanceof Object)){
            var str = msg;
            var res = str.split(";");

            var mac         = res[0];
            var ap          = res[1];
            var power       = res[2];
            var timeSent    = res[3];
            var fabricante  = res[4];  

            
        

            if(res[1] == "ap1"){    
                //console.log("AP1: " + power);
                power1 = res[2];
                var distAp1 = distFromSignalAp1(power1);
                var newEsp = new Esp(res[0], res[1], distAp1, res[3], res[4], false);
                //console.log("Power1: " + power1);
                
            }
            if(res[1] == "ap2"){
                //console.log("AP2: " + power);
                power2 = res[2];
                var distAp2 = distFromSignalAp2(power2);
                var newEsp = new Esp(res[0], res[1], distAp2, res[3], res[4], false);
                //console.log("Power2: " + power2);
                
            }
            if(res[1] == "ap3"){
                //console.log("AP3: " + power);
                power3 = res[2];
                var distAp3 = distFromSignalAp3(power3); 
                var newEsp = new Esp(res[0], res[1], distAp3, res[3], res[4], false);
                //console.log("Power3: " + power3);
                
            }

            addDevice(newEsp);  

            var query = {"mac": "18:FE:34:D6:EA:8E"};


            
            Device.findOne(query, function(err, data){
                if(err){
                    console.log(err);
                }
                else{
                    output = positionInMap(data.Distance_para_o_Ap1,data.Distance_para_o_Ap2,data.Distance_para_o_Ap3);
                    var fakepoint = [];
                    fakepoint.push(340);
                    fakepoint.push(150);
                    console.log("Outpu: " + output);
                    if(output[0] != 0 && output[1] != 0){
                        console.log("\n" + output + "\n");
                        io.emit('chat message', output);
                    }
                    var points = distanceBetweenTwoPoints(fakepoint, output);
                    console.log("Distancia entre 2 pontos: " + distanceBetweenTwoPoints(fakepoint, output));
                    console.log("Comando: " + comando + "\nContador: " + cont);
                    socket.emit('comando', comando);
                    cont++;
                    if(distAp2<1.6){
                        comando = '1';
                        console.log("Comando: " + comando);
                        cont = 0;
                    }
                    if(distAp2>1.6){
                        comando = '0';
                        console.log("Comando: " + comando);
                        cont = 0;
                    }
      
                }
            });
            
            console.log("Mensagem: ");
            console.log(msg);
            
        }
        else{
            socket.emit('comando', comando);
        }
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});




