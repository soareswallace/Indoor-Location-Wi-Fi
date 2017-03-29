// // ---- Parte 1: transforma string em array
//
// str = "18:FE:34:D6:EA:8E;AP1;23h13min;-57;Roteadores Do Tio";
// var res = str.split(";");   // explode a string em uma array

// var mac = res[0];             // console.log("MAC: "+mac+"\n");
// var ap = res[1];              // console.log("AP: "+ap+"\n");
// var timeSent = res[2];        // console.log("timeSent: "+timeSent+"\n");
// var timeArrived = new Date(); // console.log("timeArrived: "+timeArrived+"\n");
// var power = res[3];           // console.log("power: "+power+"\n");
// var fabricante = res[4];      // console.log("fabricante: "+fabricante+"\n");

// var esps = {
//     [mac] : {
//       'ap1' : power,
//       'ap2' : power,
//       'ap3' : power
//     }
// };

var esps = {
  '18:FE:34:D6:EA:8E' : {
      'ap1' : -18,
      'ap2' : -28,
      'ap3' : -38
  },
  '16:GE:38:F8:AE:6A': {
      'ap1' : -16,
      'ap2' : -26,
      'ap3' : -36
  },
  '12:AF:12:C9:EC:8I': {
      'ap1' : -12,
      'ap2' : -22,
      'ap3' : -32
  },
  '14:FA:18:A8:CE:9I': {
      'ap1' : -14,
      'ap2' : -24,
      'ap3' : -34
  }
};

var i = 0; // Ponteiro

console.log(esps);
console.log("--------");

// Manipulando o valor dos APs
// novoPower = -2;
// esps["18:FE:34:D6:EA:8E"].ap1 = novoPower;
// console.log(esps);

var qtdEsps = Object.keys(esps).length;
// console.log("Quantidade de ESPS na rede: " +qtdEsps);

// var qtdDados = Object.keys(esps[mac]).length;

// Object.keys(esps).forEach(function(key) {
//   //Consertar isso: console.log("Quantidade de dados: " + Object.keys(esps[mac]).length);
//   console.log("HEY");
//   console.log(key, esps[key]);
// });



// console.log(dados);
// console.log(dados[1]);     //dados[x] retorna não os dados mas os metadados


// console.log("Número de ESP: "+qtdEsps+"\n"+"Número de dados em cada ESP: "+qtdDados);

// while (i < qtdEsps) {
//     //console.log("Esp achado: " +esps[mac]);
//     console.log("HEY\n"+esps);
//     i++;
// }