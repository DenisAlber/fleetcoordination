const express = require('express');
const app = express();
const port = 3000;
const router = express.Router(); 

// For rendering html, boostrap, css
app.use(express.static('public'));

// parse application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: false }))

// parse application/json
app.use(express.json())

router.get('/', (req, res) => {
  // res.send('Hello Zumi!')
  res.render('public/index.html', {root: __dirname});
});

app.post('/Zumi', (req, res) =>{
    var jsonTest = '{"name":"TestServer", "count":14}';
    console.log("Block "+req.body.node1 + " to " + req.body.node2);
    res.send(jsonTest);
});


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
})