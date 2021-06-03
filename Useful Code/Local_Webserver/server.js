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
    { connected: "B" },
    { connected: "D" }
] 
},
{
    name: "B", x: 350, y: 100, r: 50, "connections": [
        { connected: "A" },
        { connected: "C" },
        { connected: "E" }
    ]
},
{
    name: "C", x: 550, y: 100, r: 50, "connections" : [
        { connected: "B" },
        { connected: "F" }
    ]
},
{
    name: "D", x: 150, y: 300, r: 50, "connections" : [
        { connected: "A" },
        { connected: "G" },
        { connected: "E" }
    ]
},
{
    name: "E", x: 350, y: 300, r: 50, "connections" : [
        { connected: "D" },
        { connected: "F" },
        { connected: "B" },
    ]
},
{
    name: "F", x: 550, y: 300, r: 50, "connections" : [
        { connected: "C" },
        { connected: "I" },
        { connected: "E" }
    ]
},
{
    name: "G", x: 150, y: 500, r: 50, "connections" : [
        { connected: "D" },
        { connected: "H" },
    ]
},
{
    name: "H", x: 350, y: 500, r: 50, connections: [
        { connected: "G" },
        { connected: "I" },
    ]
},
{
    name: "I", x: 550, y: 500, r: 50, connections : [
        { connected: "H" },
        { connected: "F" },
    ]
}
]);

var myEventHandler = function(){
  console.log("Moin");
  resList.forEach(element => {
    element.send("jamoin");
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

app.get('/GetMap', (req, res) => {
  let json = `{"nodes" : ${db().stringify()}}`;
  res.send(json);
});

app.get('/traffic', (req, res) => {
  resList.push(res);
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});