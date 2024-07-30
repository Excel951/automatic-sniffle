'use strict'; 
var fs = require('fs'); 
const net = require('net');
var dataReceive = [];
var logFile = '';
var axios = require('axios');
var stringify = require('json-stringify');
var moment = require('moment');
var STX = [0x02];
var ENQ = [0x05]; //ENQUIRY
var ACK = [0x06]; //ACKNOWLEDGE
var EOT = [0x04]; //END OF TEXT
var LF = [0x0A]; //LINE FEED
var ETX = [0x03];
var FS = [0x1C];
const { defineLocale } = require('moment');
const client = net.createConnection({ port: 3030, host: '192.168.100.30' });  
client.on('connect',  () => {
    console.log('CLIENT is listening');
    logFile += 'client is listening \n';
});
    client.on('data', (data) => { 
        console.log(data)
            for (var i = 0; i < data.length; i++){ 
               dataReceive.push(data[i]);
                if (data[i] === ENQ[0]) {
                          console.log('RX ENQ')
                            client.write(Buffer.from(String.fromCharCode(0x06)));
                }
                if (data[i] === EOT[0]) {
                          console.log('RX EOT')
                            client.write(Buffer.from(String.fromCharCode(0x05)));
                }
                if (data[i] === ACK[0]) {
                          console.log('RX ACK')
                            client.write(Buffer.from(String.fromCharCode(0x04)));
                } 
                if (data[i] === LF[0]) {
                          console.log('RX LF')
                           client.write(Buffer.from(String.fromCharCode(0x06)));
                                }
    }
    client.on('close', () => {
        console.log('close, socket disconnected')
    });

    client.on('end', () => {
        console.log('end')
    });

    client.on('error', () => {
        console.log('error, disconnected')
    });
});
