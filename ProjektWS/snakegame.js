//* Snake Game  */
// TODO: usage Score 
let score = 0;    
let op_score = 0;
// Get canvas board element
var board = document.getElementById('mySnakeCanvas');
// Get context
var context = board.getContext('2d');
// Set global alpha - to notice when snake is folding 
context.globalAlpha = 0.7;
// Move listener
// NOTE: to make it single player before starting game:
// document.addEventListener("keydown", direction_control);
// Food params
let food = {
  x: 0,
  y: 0
};
// Init position
var my_init_pos = 200;
var op_init_pos = 600;
// My snake body - init 2 elems
var my_snake_body = [];
// Opponent snake body 
var op_snake_body = [];
// Constant values
// Delta between points
const delta = 40;
// Point width and height
const point_w = delta;
const point_h = delta;
// My snake color
const my_snake_color = {
  color: 'blue',
  border: 'black'
};
// Opponent's snake color
const op_snake_color = {
  color: 'yellow',
  border: 'black'
};
// Food color
const food_color = {
  color: 'red',
  border: 'black'
};
// My actual direction
var actual_direction = {
  dx: delta,
  dy: 0
};
// Calculate index on board with given xy coordinates
function calculateBoardIndex(x,y){
  return (calculate_index_xy(x) + (calculate_index_xy(y) * 20));
}
// Calculate basic index by coordinates
function calculate_index_xy(coordinates){
  return ((coordinates / 40) - 1);
}
// Calculate coordinates from given index
function calculateCoordinatesXY(index){
  return ((index + 1) * 40);
}
// Calculate x index from board index
function calculate_xIndex(board_index){
  return board_index % (board.width / delta);
}
// Calculate y index from board index
function calculate_yIndex(board_index){
  return Math.floor(board_index / (board.height / delta));
}
// Player A is true, player B is false
var whoami = true;
// Init snake body
function init_snake_body(){
  my_snake_body = [
    // Snake head
    { 
      x: my_init_pos, 
      y: my_init_pos
    },
    // Secound element of snake body
    { 
      x: my_init_pos - delta, 
      y: my_init_pos
    }
  ];
}
// Init opponent snake body
function init_op_snake_body(){
  op_snake_body = [
    // Snake head
    { 
      x: op_init_pos, 
      y: op_init_pos
    },
    // Secound element of snake body
    { 
      x: op_init_pos - delta, 
      y: op_init_pos
    }
  ];
}
// Init first player A
function init_player_a(){
  whoami = true;
  my_init_pos = 120;
  actual_direction = {
    dx: delta,
    dy: 0
  };
  init_snake_body();
  // Start main loop
  main_loop();
  // gen_food();
}
// Init Secound player B
function init_player_b(){
  whoami = false;
  my_init_pos = 640;
  actual_direction = {
    dx: -delta,
    dy: 0
  };
  init_snake_body();
  // Start main loop
  main_loop();
  // gen_food();
}
// Init opponent player
function init_op_player(){
  if(whoami){
    op_init_pos = 640;
  }else{
    op_init_pos = 120;
  }
  init_op_snake_body();
}
// Draw single point
function drawPoint(point, point_color){
  context.fillStyle = point_color.color;
  context.strokestyle = point_color.border;
  context.fillRect(point.x, point.y, point_w, point_h);
  context.strokeRect( point.x, point.y, point_w, point_h);
}
// Draw entire snake
function drawSnake(){
  // Make head more visible - adding black background
  drawPoint(my_snake_body[0],{color:'black', border:'black'});
  drawPoint(my_snake_body[0],{color:'black', border:'black'}); // TODO: change alpha on canvas
  // Draw every point (including head again)
  my_snake_body.forEach(point => drawPoint(point, my_snake_color));
}
// Draw opponent's snake
function drawOpSnake(){
  // Make head more visible - adding black background
  drawPoint(op_snake_body[0],{color:'black', border:'black'});
  drawPoint(op_snake_body[0],{color:'black', border:'black'});
  // Draw every point (including head again)
  op_snake_body.forEach(point => drawPoint(point, op_snake_color));
}
// Clear whole canvas
function clearCanvas(){
  context.clearRect(0,0,board.width,board.height);
}
// Refresh board
function refresh_board(){
  // Clear whole canvas
  clearCanvas();
  // Draw cleared food
  drawFood();
  // Draw new snake
  drawSnake();
  // Draw enemy snake
  drawOpSnake();
}
// Move snake
function move() 
{ 
  // New snake head - in new postition
  head = {
    x: my_snake_body[0].x + actual_direction.dx, 
    y: my_snake_body[0].y + actual_direction.dy
  };
  // Add head to the beginning
  my_snake_body.unshift(head);
  // Check if snake is eating food rn (in new position)
  const is_eating = 
    my_snake_body[0].x === food.x && 
    my_snake_body[0].y === food.y;
  if (is_eating) {
        // TODO: remmember to add score usage Increase score 
        score += 1;
        // Generate food
        // gen_food();
  } else {
    // Pop tail point - last part of my snake body
    my_snake_body.pop();
  }
  move_on_board(
    calculateBoardIndex(
        my_snake_body[0].x,
        my_snake_body[0].y
      )
    );
  // Refresh board with new move
  refresh_board();
}
// Opponent move
function recived_op_move(board_index){
  // New head coordinates
  var h_x = calculateCoordinatesXY(calculate_xIndex(board_index));
  var h_y = calculateCoordinatesXY(calculate_yIndex(board_index));
  // New snake head - in new postition
  head = {
    x: h_x, 
    y: h_y
  };
  // Add head to the beginning
  op_snake_body.unshift(head);
  // Check if snake is eating food rn (in new position)
  const is_eating = 
    op_snake_body[0].x === food.x && 
    op_snake_body[0].y === food.y;
  if (is_eating) {
        // TODO: remmember to add score usage Increase score 
        op_score += 1;
  } else {
    // Pop tail point - last part of my snake body
    op_snake_body.pop();
  }
  // Refresh board with new move
  refresh_board();
}
// Receive food
function receive_food(board_index){
  // New food coordinates
  food = {
    x: calculateCoordinatesXY(calculate_xIndex(board_index)),
    y: calculateCoordinatesXY(calculate_yIndex(board_index))
  }
  // Refresh board with new move
  refresh_board();
}
// Direction arrow key codes
// https://css-tricks.com/snippets/javascript/javascript-keycodes/
var LEFT_KEY = 37;
var RIGHT_KEY = 39;
var UP_KEY = 38;
var DOWN_KEY = 40;
// Snake movement variables (direction)
// Going left - x coordinates decrease
var LEFT_DIRECTION = {
  dx: -delta,
  dy: 0
};
// Going right - x coordinates increase
var RIGHT_DIRECTION = {
  dx: delta,
  dy: 0
};
// Going up - y coordinates decrease
var UP_DIRECTION = {
  dx: 0,
  dy: -delta
};
// Going down - y coordinates increase
var DOWN_DIRECTION = {
  dx: 0,
  dy: delta
};
// Control direction after keydown event
function direction_control(event) 
{ 
  // Snake movement booleans 
  var goingLeft = actual_direction.dx === -delta;
  var goingRight = actual_direction.dx === delta;  
  var goingUp = actual_direction.dy === -delta;
  var goingDown = actual_direction.dy === delta;
  // Get key code
  switch (event.keyCode){
    // If snake wants to go left 
    case LEFT_KEY:
      // If snake isn't going right 
      if(!goingRight){
        // Snake is going left 
        actual_direction = LEFT_DIRECTION;
      }
      break;
    // If snake wants to go right 
    case RIGHT_KEY:
      // If snake isn't going left 
      if(!goingLeft){
        // Snake is going right 
        actual_direction = RIGHT_DIRECTION;
      }
      break;
    // If snake wants to go up 
    case UP_KEY:
      // If snake isn't going down 
      if(!goingDown){
        // Snake is going up 
        actual_direction = UP_DIRECTION;  
      }
      break;
    // If snake wants to go down 
    case DOWN_KEY:
      // If snake isn't going up 
      if(!goingUp){
        // Snake is going up 
        actual_direction = DOWN_DIRECTION;  
      }
      break;
  }
  // Move snake on key down press
  move();
  // TODO:
  // Check if it is end of the game
  // if (is_end()) return;
}
// // TODO: Serwer sending end of game after hitting player
// function is_end()
// { 
//   return false;
// }
// // TODO: server stuff Randomize food location -- 
// function random_food(min, max)
// {  
//    return Math.round((Math.random() * (max-min) + min) / delta) * delta;
// }
// Draw food
function drawFood(){
  drawPoint({x:food.x, y:food.y,}, food_color);
}
// Main loop
function main_loop() {
  // Check if it is end of the game
  if (is_end()) return;
  // Tick every 100 ms
  setTimeout(function onTick() {
    // Move snake 
    move();
    main_loop();
  }, 1000)
}
// NOTE: To make it single player before game starts
// Start main loop
//main_loop();
// Generate first food
// gen_food();