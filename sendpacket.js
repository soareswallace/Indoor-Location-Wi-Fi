const net = require('net');
const client = net.createConnection({port: 8125}, () => {
  //'connect' listener
  console.log('Conectado ao servidor.');
  console.log('AP1 mandando mensagem: "HEY"!');
  client.write('HEY!\r\n');
});
client.on('data', (data) => {
  console.log(data.toString());
  client.end();
});
client.on('end', () => {
  console.log('Desconectado do servidor.');
});