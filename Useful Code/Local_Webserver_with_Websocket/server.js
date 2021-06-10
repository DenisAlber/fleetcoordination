const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const router = express.Router(); 
const WebSocket = require('ws');
TAFFY = require('taffy');

// Create a new database using a JSON string
var db = TAFFY([
  {name: "A", x: 150, y: 100, r: 50, isTarget : false,"connections" : [
    { connected: "B", blocked: false }, // key blocked : true/false?
    { connected: "D", blocked: false }
] 
},
{
    name: "B", x: 350, y: 100, r: 50, isTarget : false, "connections": [
        { connected: "A", blocked: false },
        { connected: "C", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "C", x: 550, y: 100, r: 50,  isTarget : false, "connections" : [
        { connected: "B", blocked: false },
        { connected: "F", blocked: false }
    ]
},
{
    name: "D", x: 150, y: 300, r: 50, isTarget : false, "connections" : [
        { connected: "A", blocked: false },
        { connected: "G", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "E", x: 350, y: 300, r: 50,  isTarget : false, "connections" : [
        { connected: "D", blocked: false },
        { connected: "F", blocked: false },
        { connected: "B", blocked: false },
    ]
},
{
    name: "F", x: 550, y: 300, r: 50,  isTarget : false, "connections" : [
        { connected: "C", blocked: false },
        { connected: "I", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "G", x: 150, y: 500, r: 50,  isTarget : false, "connections" : [
        { connected: "D", blocked: false },
        { connected: "H", blocked: false },
    ]
},
{
    name: "H", x: 350, y: 500, r: 50,  isTarget : false, connections: [
        { connected: "G", blocked: false },
        { connected: "I", blocked: false },
    ]
},
{
    name: "I", x: 550, y: 500, r: 50,  isTarget : false, connections : [
        { connected: "H", blocked: false },
        { connected: "F", blocked: false },
    ]
}
]);

// For rendering html, boostrap, css
app.use(express.static('public'));

// parse application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: false }))

// parse application/json
app.use(express.json())

// render and send main page
router.get('/', (req, res) => {
  res.render('public/index.html', {root: __dirname});
});

// For resetting target
// JSON String should be {id: 'A'}
app.post('/zumi', (req, res) =>{
    db({name : req.body.id}).update()
});

app.get('/GetMap', (req, res) => {
  let json = `{"nodes" : ${db().stringify()}}`;
  res.send(json);
});

// WebSocket
const wsServer = new WebSocket.Server({ noServer: true });
wsServer.on('connection', ws => {

    ws.send("connected to server ...");
  
    ws.on('message', message => 
    {
        if(message == " ") {
            ws.send("pong")
            return;
        }
        let body = JSON.parse(message)
        if(body.node2 != "")
        {
            SetLock(ws, body.node1, body.node2);
        }
        else{
            SetTarget(ws, body.node1);
        }
    });
  });

function SetLock(ws, firstNode, secondNode){
    console.log("locking street...")
    var nodeConnection = db({name : firstNode}).first().connections;
    nodeConnection.forEach(element => {
        if(element.connected == secondNode){
            if(element.blocked){
                console.log("street " + firstNode + " -> " + secondNode +  " unlocked!");
                element.blocked = false;
               var jsonResponse = {id : firstNode + secondNode, isBlocked : element.blocked};
                wsServer.clients.forEach(function each(client) {
                  if (client.readyState === WebSocket.OPEN) {
                  client.send(JSON.stringify(jsonResponse))
                  }
                })
            }
            else{
                console.log("street " + firstNode + " -> " + secondNode +  " locked!");
                element.blocked = true;
                
                var jsonResponse = {id : firstNode + secondNode, isBlocked : element.blocked};
                wsServer.clients.forEach(function each(client) {
                  if (client.readyState === WebSocket.OPEN) {
                  client.send(JSON.stringify(jsonResponse))
                  }
                })
            }
        }
    });

    db({name : firstNode}).update({connections : nodeConnection});
}

function SetTarget(ws, node){
    let targets = db({isTarget : true}).get();
    if(Object.keys(targets).length != 0){
        ws.send("Another target is already set!");
        return;
    } 
    console.log("set target ...");
    db({name : node}).update({isTarget : true});

    var jsonResponse = {id : node, isTarget : true};
    wsServer.clients.forEach(function each(client){
        client.send(JSON.stringify(jsonResponse));
    })
}

const server = app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

server.on('upgrade', (request, socket, head) => {
    wsServer.handleUpgrade(request, socket, head, socket => {
      wsServer.emit('connection', socket, request);
    });
  });