const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello Zumi!')
})

app.get('/Zumi', (req, res) =>{
    var jsonTest = '{"name":"TestServer", "count":14}';
    res.send(jsonTest);
});


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})