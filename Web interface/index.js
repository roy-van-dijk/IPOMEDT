var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
  console.log(res);
  console.log(req);
});

app.get('/test/', function (req, res){
  console.log("test")
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "test")
})

app.get('/wachtenopbestemming/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "wachtenopbestemming")
})
app.get('/klaaromtestarten/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "klaaromtestarten")
})
app.get('/onderwegnaarkruispunt/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "onderwegnaarkruispunt")
})
app.get('/kruispuntgevonden/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "kruispuntgevonden")
})
app.get('/onderwegnaarbestemming/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "onderwegnaarbestemming")
})
app.get('/bestemmingbereikt/', function (req, res){
  res.sendFile(__dirname + '/index.html');
  io.emit("voortgang", "bestemmingbereikt")
})

http.listen(3000, function(){
  
});