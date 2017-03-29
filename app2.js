var net = require('net');
var server = net.createServer((c) => {
    // 'connection' listener
    //console.log('client connected');
    c.on('data', (data) => {
        console.log(data.toString()); //mongo
    });
    c.on('end', () => {
//        console.log('client disconnected');
    });

    
    //c.pipe(c);

});
    

server.on('error', (err) => {
  throw err;
});

server.listen(8125, () => {
  console.log('Server connected and running...');
});