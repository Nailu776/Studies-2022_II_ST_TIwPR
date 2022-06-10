// Init connection on load
// init();
window.addEventListener("load", init, false);
function reload(){
  // Reload app info
  if((window.sessionStorage.getItem('gameOn'))){
    storage_gameOn = window.sessionStorage.getItem('gameOn');
    if(storage_gameOn == 1){
      application.gameOn = true;
    }else{
      application.gameOn = false;
    }
    if(application.gameOn){
      // Reload game id
      application.gameId = parseInt(window.sessionStorage.getItem('gameId'));
      // Reload whoami
      // whoami = JSON.parse(window.sessionStorage.getItem("whoami"));
      storage_whoami = window.sessionStorage.getItem('whoami');
      if(storage_whoami == 1){
        whoami = true;
      }else{
        whoami = false;
      }
      // Send resume msg
      resume_msg(application.gameId);
      // Reload game      
      autoreload();
      // Move listener
      document.addEventListener("keydown", direction_control);
      // Start my main loop
      main_loop();
      document.getElementById("myGameStatus").innerHTML = "Game status: Refreshed game. Good Luck!";
    }
  }
}
// Application params
var application = {
  connected: false,
  gameId: null,
  gameOn: false
}
// Init WebSocket connection
function init() {
  websocket = new WebSocket("ws://localhost:8888/ws");
  websocket.binaryType = 'arraybuffer';
  websocket.onopen = function(e) { onOpen(e) };
  websocket.onclose = function(e) { onClose(e) };
  websocket.onerror = function(e) { onError(e) };
  websocket.onmessage = function(e) { onMessage(e) };
}
// On WebSocket open
function onOpen(e) {
  console.log("Connected to server.");
  // Try to reload data from session
  reload();
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
// Code action sending to server 
function code_my_action(str_action){
  switch (str_action){
    case "move":
      // Sending my move means sending 3
      return 3
    case "new":
      // Start new game means sending 0
      return 0 
    case "join":
      // Join existing game means sending 1
      return 1
    case "resume":
      // Sending resume action means sending 2
      return 2
    case "end":
      // Sending ending game msg (give up or lost)
      return 4;
  }
}
// Decode action
function decode_my_action(coded_action){
  switch (coded_action){
    case 0:
      return "wait"
    case 1:
      return "start"
    case 2:
      return "op_move"
    case 3:
      return "food_move"
    case 4: 
      return "end"
    case 5: 
      return "err"
  }
}
// Decode eventual data
function decode_eventual_data(coded_action, data_view){
  switch (coded_action){
    case 0:
      // Decode id of your game if you wait
      return data_view.getInt8(1)
    case 1:
      // Decode player a or player b
      return data_view.getUint8(1)
    case 2:
      // Decode index of opp move
      return data_view.getInt16(1)
    case 3:
      // Decode index of food
      return data_view.getInt16(1)
    case 4: 
      // Decode that enemy lost or gave up game
      return null
    case 5:
      // Decode error
      return null
  }
}
// On WebSocket message
function onMessage(e) {
  // Get data from binary data
  var data_view = new DataView(e.data,0);
  var coded_action = data_view.getInt8(0)
  var action = decode_my_action(coded_action);
  var data = decode_eventual_data(coded_action, data_view);
  // Log recived message
  console.log("Received action:\t\'" + action + "\'.");
  console.log("Received data:\t\'" + data + "\'.");
  onServerMessage(action, data);
}
// Use server message
function onServerMessage(action, data){
  switch (action) {
    case "wait":
      document.getElementById("game_id").value = data
      application.gameId = data
      document.getElementById("myGameStatus").innerHTML = "Game status: Waiting for opponent...";
      console.log("Waiting for opponent... Game id: '" + data + "'.");
      break;
    case "start":
      // Move listener
      document.addEventListener("keydown", direction_control);
      document.getElementById("myGameStatus").innerHTML = "Game status: Starting game. Good Luck!";
      application.gameOn = true;
      if(application.gameId == null){
        application.gameId = document.getElementById("game_id").value;
      }
      // data == True means player A
      // NOTE:
      // NOTE: Session storage solve 2 players 1 browser
      window.sessionStorage.setItem('gameOn', 1);
      window.sessionStorage.setItem('gameId', application.gameId);
      if(data == true){
        console.log("Start Game as player A.");
        init_player_a();
        resume_msg(application.gameId);
      } else {
        console.log("Start Game as player B.");
        init_player_b();
        resume_msg(application.gameId);
      }
      break;
    case "op_move":
      console.log("Opponent moved to board index: '" + data + "'.");
      recived_op_move(data);
      break;
    case "food_move":
      console.log("Food moved to board index: '" + data + "'.");
      receive_food(data);
      break;
    case "end":
      winning_action();
      application.gameOn = false;
      console.log("Enemy lost.");
      document.getElementById("myGameStatus").innerHTML = "Game status: Nice. You win!";
      websocket.close();
      window.localStorage.clear();
      window.sessionStorage.clear();
  }
}
// Start new game
function start_game(){
  var buffer = new ArrayBuffer(1);
  var data_view = new DataView(buffer);
  data_view.setInt8(0,0);
  websocket.send(buffer);
  console.log("Sent: 'new'.");
}
// Joing game
function join_game(gameId){
  var buffer = new ArrayBuffer(3);
  var data_view = new DataView(buffer);
  data_view.setInt8(0,code_my_action("join"));
  data_view.setInt16(1,gameId);
  websocket.send(buffer);
  console.log("Sent: 'join'.");
}
// MOVE send
function move_on_board(board_index){
  var buffer = new ArrayBuffer(3);
  var data_view = new DataView(buffer);
  data_view.setInt8(0,code_my_action("move"));
  data_view.setInt16(1,board_index);
  websocket.send(buffer);
  console.log("Sent: 'move'.");
}
// END send 
function send_ending_msg(){
  var buffer = new ArrayBuffer(1);
  var data_view = new DataView(buffer);
  data_view.setInt8(0,code_my_action("end"));
  websocket.send(buffer);
  console.log("Sent: 'end'.");
  document.getElementById("myGameStatus").innerHTML = "Game status: You lose.";
  websocket.close();
  window.localStorage.clear();
  window.sessionStorage.clear();
}
// Resume send
function resume_msg(gameId){
  var buffer = new ArrayBuffer(3);
  var data_view = new DataView(buffer);
  data_view.setInt8(0,code_my_action("resume"));
  data_view.setInt8(1,gameId);
  data_view.setInt8(2,whoami);
  websocket.send(buffer);
  console.log("Sent: 'resume'.");
}
// Click submit button
document.getElementById("submit_btn").addEventListener("click", submit_fun);
function submit_fun(){
  if(application.gameOn){
    // abort
    end_game();
  }
  else{
    // Check if connected
    if(!application.connected){
      init();
    }
    // Get game id from input
    var gameId = 
      document.getElementById("game_id").value;
    if(gameId){
      // If there is id try to join game
      document.getElementById("myGameStatus").innerHTML = "Game status: Trying to join game";
      join_game(gameId);
    }
    else{
      // Else start new one
      document.getElementById("myGameStatus").innerHTML = "Game status: Trying to start a new game";
      start_game();
    }
  }
}