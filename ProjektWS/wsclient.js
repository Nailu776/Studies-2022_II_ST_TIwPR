function init() {
  websocket = new WebSocket("ws://localhost:8888/ws");
  websocket.onopen = function(e) { onOpen(e) };
  websocket.onclose = function(e) { onClose(e) };
  websocket.onmessage = function(e) { onMessage(e) };
  websocket.onerror = function(e) { onError(e) };
}

function onOpen(e) {
  console.log(e.type);
  websocket.send("Hello there! ;)");
}

function onMessage(e) {
  console.log('Received message: ' + e.data + '.');
  websocket.close();
}
function onClose(e) {  
  console.log('Connection closed.');
};

window.addEventListener("load", init, false);