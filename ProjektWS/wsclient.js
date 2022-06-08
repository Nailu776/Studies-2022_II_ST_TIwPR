// init();
// Init connection on load
window.addEventListener("load", init, false);
// Application params
var application = {
  connected: false,
  gameId: null,
  gameOn: false
}
// Init WebSocket connection
function init() {
  websocket = new WebSocket("ws://localhost:8888/ws");
  websocket.onopen = function(e) { onOpen(e) };
  websocket.onclose = function(e) { onClose(e) };
  websocket.onerror = function(e) { onError(e) };
  websocket.onmessage = function(e) { onMessage(e) };
}
// On WebSocket open
function onOpen(e) {
  console.log("Connected to server.");
  application.connected = true;
}
// On WebSocket close
function onClose(e) {  
  console.log('Connection closed.');
  application.connected = false;
}
// On WebSocket error
function onError(e) {  
  console.log('Connection error.');
}
// On WebSocket message
function onMessage(e) {
  // Get data from binary data TODO:
  var payload = JSON.parse(e.data);
  var action = payload.action;
  var data = payload.data;
  // Log recived message
  console.log('Received message: ' + e.data + '.');
  onServerMessage(action, data);
}
// Use server message
function onServerMessage(action, data){
  switch (action) {
    case "start_player_a":
      application.gameOn = true;
      console.log("Start Game as player A.");
      my_init_pos = 120;
      actual_direction = {
        dx: delta,
        dy: 0
      };
      init_snake_body();
      // Start main loop
      main_loop();
      // Move listener
      document.addEventListener("keydown", direction_control);
      break;
    case "start_player_b":
      application.gameOn = true;
      console.log("Start Game as player B.");
      my_init_pos = 640;
      actual_direction = {
        dx: -delta,
        dy: 0
      };
      init_snake_body();
      // Start main loop
      main_loop();
      // Move listener
      document.addEventListener("keydown", direction_control);
      break;
  }
}
// Start new game
function start_game(){
  var data = {
    action: "new"
  };
  websocket.send(JSON.stringify(data));
  console.log(data);
}
// Joing game
function join_game(gameId){
  var data = {
    action: "join",
    game_id: gameId
  };
  websocket.send(JSON.stringify(data));
  console.log(data);
}
// Click submit button
document.getElementById("submit_btn").addEventListener("click", submit_fun);
function submit_fun(){
  if(application.gameOn){
    // abort
  }
  else{
    // Check if connected
    if(!application.connected){
      init();
    }
    var gameId = document.getElementById("game_id").value;
    if(gameId){
      join_game(gameId);
    }
    else{
      start_game();
    }
  }
}