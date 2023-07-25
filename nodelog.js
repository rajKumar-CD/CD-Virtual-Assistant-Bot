const express = require('express')
const app = express()
var bodyParser = require('body-parser')
const fs = require('fs');
const { connect } = require('http2');
var cors = require('cors')

app.use(cors())

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

app.get('/readFile', function (req, res) {
  res.send(readFile())
})

app.post('/updateFile', (req,res) => {
    var body = req.body
    var content = body.content;
    writeFile(content);
    res.send({
        "data":"Process successful!"
    })
})

function writeFile(content){
    var date =getCurrentDate();
    if(`${date}.txt`){
        fs.appendFile(`${date}.txt`, content, function (err) { 
            if (err) throw err; 
            console.log('The "data to append" was appended to file!'); 
          }); 
    }
    else{
        fs.writeFileSync(`${date}.txt`,content, function (err) {
            if (err) throw err;
            console.log('Saved!')});
    }
}
    
function readFile(){
    var date = getCurrentDate()
    return fs.readFileSync(`./${date}.txt`,{ encoding: 'utf8', flag: 'r' })
}

function getCurrentDate(){
    var today = new Date();
    var date = today.getFullYear()+'_'+(today.getMonth()+1)+'_'+today.getDate();
    return date
}
app.listen(3001)