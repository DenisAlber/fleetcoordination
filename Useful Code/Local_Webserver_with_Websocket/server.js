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

var trafficControlDb = TAFFY([
    {zumiId : "1", nextCrossing : "", direction : ""},
    {zumiId : "2", nextCrossing : "", direction : ""}
])

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
    db({name : req.body.id}).update({isTarget : false});
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
        // keep alive ping for heroku application
        // the heroku app goes off after 10 min when no receives any data
        if(message == " ") {
            ws.send("pong")
            return;
        }
        let body = JSON.parse(message)
        if(body.hasOwnProperty('node1') && body.hasOwnProperty('node2')){
            SetLock(ws, body.node1, body.node2);
        }
        else if(body.hasOwnProperty('target')){
            SetTarget(ws, body.target);
        }
        else if(body.hasOwnProperty('zumiId')  
                && body.hasOwnProperty('nextCrossing')
                && body.hasOwnProperty('direction')){

            trafficControlDb({zumiId : body.zumiId})
                .update({nextCrossing : body.nextCrossing, direction : body.direction});
        }
        else if(body.hasOwnProperty('zumiId')
                && !body.hasOwnProperty('nextCrossing')
                && !body.hasOwnProperty('direction')){
            
            ws.send(CanDrive(body).toString());


            // var other = trafficControlDb({zumiId : {"!is" : body.zumiId}}).stringify()

            // console.log("other Zumi: " + other)
        }
    });
  });

function CanDrive(body){
    if(trafficControlDb({zumiId : body.zumiId}).nextCrossing == "" 
        || trafficControlDb({zumiId : {"!is" : body.zumiId}}).nextCrossing == "") return true;

    if(trafficControlDb({zumiId : body.zumiId}).nextCrossing 
        != trafficControlDb({zumiId : {"!is" : body.zumiId}}).nextCrossing) return true;

    return crossingRules(trafficControlDb({zumiId : body.zumiId}).direction, trafficControlDb({zumiId : {"!is" : body.zumiId}}).direction);
}

function crossingRules(thisDirection, otherDirection){
    // cars are on the opposite sides
    if(thisDirection == "North" && otherDirection == "South") return true;
    if(thisDirection == "South" && otherDirection == "North") return false;
    if(thisDirection == "West" && otherDirection == "East") return true;
    if(thisDirection == "East" && otherDirection == "West") return false;
    
    // car is on the right side from the other one
    if(thisDirection == "North" && otherDirection != "West") return true;
    if(thisDirection == "South" && otherDirection != "East") return true;
    if(thisDirection == "West" && otherDirection != "South") return true;
    if(thisDirection == "East" && otherDirection != "North") return true;

    return false;
}

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