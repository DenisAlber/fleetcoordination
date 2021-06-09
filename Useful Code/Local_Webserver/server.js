const express = require('express');
const app = express();
const port = 3000;
const router = express.Router(); 
var events = require('events');
var eventEmitter = new events.EventEmitter();
var resList = [];
TAFFY = require('taffy');

// Create a new database using a JSON string
var db = TAFFY([
  {name: "A", x: 150, y: 100, r: 50,  "connections" : [
    { connected: "B", blocked: false }, // key blocked : true/false?
    { connected: "D", blocked: false }
] 
},
{
    name: "B", x: 350, y: 100, r: 50, "connections": [
        { connected: "A", blocked: false },
        { connected: "C", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "C", x: 550, y: 100, r: 50, "connections" : [
        { connected: "B", blocked: false },
        { connected: "F", blocked: false }
    ]
},
{
    name: "D", x: 150, y: 300, r: 50, "connections" : [
        { connected: "A", blocked: false },
        { connected: "G", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "E", x: 350, y: 300, r: 50, "connections" : [
        { connected: "D", blocked: false },
        { connected: "F", blocked: false },
        { connected: "B", blocked: false },
    ]
},
{
    name: "F", x: 550, y: 300, r: 50, "connections" : [
        { connected: "C", blocked: false },
        { connected: "I", blocked: false },
        { connected: "E", blocked: false }
    ]
},
{
    name: "G", x: 150, y: 500, r: 50, "connections" : [
        { connected: "D", blocked: false },
        { connected: "H", blocked: false },
    ]
},
{
    name: "H", x: 350, y: 500, r: 50, connections: [
        { connected: "G", blocked: false },
        { connected: "I", blocked: false },
    ]
},
{
    name: "I", x: 550, y: 500, r: 50, connections : [
        { connected: "H", blocked: false },
        { connected: "F", blocked: false },
    ]
}
]);

var myEventHandler = function(street, blocked){
//   console.log("test");
  var jsonResponse = {id : street, isBlocked : blocked};
  resList.forEach(element => {
    element.send(jsonResponse);
  });
  resList = [];
}

eventEmitter.on('tick', myEventHandler);

// console.log(db().stringify());
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

// receive post request
app.post('/Zumi', (req, res) =>{
    var jsonTest = '{"name":"TestServer", "count":14}';
    console.log("Block "+req.body.node1 + " to " + req.body.node2);
    res.send(jsonTest);
    eventEmitter.emit('tick');
});

// receive post request
app.get('/Zumi', (req, res) =>{
    resList.push(res);
    // var jsonTest = '{"name":"TestServer", "count":14}';
    // // console.log("Block "+req.body.node1 + " to " + req.body.node2);
    // res.send(jsonTest);
    // eventEmitter.emit('tick');
});

app.get('/GetMap', (req, res) => {
  let json = `{"nodes" : ${db().stringify()}}`;
  res.send(json);
});

app.get('/traffic', (req, res) => {
  resList.push(res);
});

app.post('/traffic', (req, res) => {
    let firstNode = req.body.node1;
    let secondNode = req.body.node2;

    // check if 
    if(secondNode != "nothing"){
        console.log("locking street...")
        // var nodeConnection = db({name : firstNode}).select("connections");
        // get connections with name
        var nodeConnection = db({name : firstNode}).first().connections;

        nodeConnection.forEach(element => {
            // console.log(element);
            if(element.connected == secondNode){
                if(element.blocked){
                    console.log("street " + firstNode + " -> " + secondNode +  " unlocked!");
                    element.blocked = false;
                    eventEmitter.emit('tick', firstNode + secondNode, element.blocked);
                }
                else{
                    console.log("street " + firstNode + " -> " + secondNode +  " locked!");
                    element.blocked = true;
                    eventEmitter.emit('tick', firstNode + secondNode, element.blocked);
                }
            }
        });
        db({name : firstNode}).update({connections : nodeConnection});
        res.send("success!");   
        // console.log(db().stringify());
    }

    if(secondNode == "nothing"){
        console.log("set target...")
    }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});