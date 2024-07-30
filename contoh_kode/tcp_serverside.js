'use strict';
const net = require('net');
const fs = require('fs');
var moment = require('moment');
//const server = net.createServer({port: 5833, host: '192.168.3.137'});

var STX = [0x02];
var ENQ = [0x05]; //ENQUIRY
var ACK = [0x06]; //ACKNOWLEDGE
var EOT = [0x04]; //END OF TEXT
var LF = [ 0x0A]; //LINE FEED
var ETX = [0x03];
var FS = [0x1C];

server.listen(6033, function () {
     console.log('server is listening');
 });

server.on('connection', socket => {
  console.log('new client arrived');
  socket.on("data", data => {
    console.log(data);
    for (var i = 0; i < data.length; i++){ 
         if (data[i] === 0x05) {
                console.log(data)
                socket.write(Buffer.from(String.fromCharCode(0x06)));
         }
         if (data[i] === 0x04) {
                console.log(data)
                socket.write(Buffer.from(String.fromCharCode(0x05)));
        }
        if (data[i] === 0x06) {
                console.log(data)
                socket.write(Buffer.from(String.fromCharCode(0x04)));
        }
        if (data[i] === 0x0A) {
                console.log(data)
                socket.write(Buffer.from(String.fromCharCode(0x06)));
        }
    }
    })
  server.on('close', () => {
      console.log('close, client disconnected')
  });

  server.on('end', () => {
      console.log('end')
  });

  server.on('error', () => {
      console.log('error, disconnected')
});
});
