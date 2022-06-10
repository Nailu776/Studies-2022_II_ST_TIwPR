//* Snake Game  */
// TODO: usage Score 
let score = 0;    
let op_score = 0;
let still_playing = true;
// Get canvas board element
var board = document.getElementById('mySnakeCanvas');
// Get context
var context = board.getContext('2d');
// Set global alpha - to notice when snake is folding 
context.globalAlpha = 0.7;
// Food index on board (outside board init)
var food_index = 400;
// My snake body - init 2 elems (element = index on board)
var my_snake_body = [];
// Opponent snake body 
var op_snake_body = [];
// Constant values
const GAME_TICK = 1000; //in ms
const IM_PA = true;
const IM_PB = false;
const PA_INIT_INDEX = 43;
const PB_INIT_INDEX = 336;
const NO_INDEXES_IN1D = 20;
// Point size
const PSIZE = (board.width / NO_INDEXES_IN1D);
// Black background color
const BLACK_COLOR = {
  color: 'black',
  border: 'black'
};
// My snake color
const MY_SNAKE_COLOR = {
  color: 'blue',
  border: 'black'
};
// Opponent's snake color
const OP_SNAKE_COLOR = {
  color: 'yellow',
  border: 'black'
};
// Food color
const FOOD_COLOR = {
  color: 'red',
  border: 'black'
};
// Max board index
const MAX_INDEX = 399;
// Next index
const NEXT_INDEX = 1;
// Direction arrow key codes
// https://css-tricks.com/snippets/javascript/javascript-keycodes/
const LEFT_KEY = 37;
const RIGHT_KEY = 39;
const UP_KEY = 38;
const DOWN_KEY = 40;
// Possible directions
// Snake movement variables (direction)
const DIRECTION_RIGHT = NEXT_INDEX;
const DIRECTION_LEFT = -NEXT_INDEX;
const DIRECTION_UP = -NO_INDEXES_IN1D;
const DIRECTION_DOWN = NO_INDEXES_IN1D;
// My actual direction
var actual_direction = DIRECTION_RIGHT;
// Init position - index on board
var my_init_pos = PA_INIT_INDEX;
var op_init_pos = PB_INIT_INDEX;
// Calculate index on board with given xy coordinates
function calculateBoardIndex(x,y){
  return (calculate_index_xy(x) + (calculate_index_xy(y) * NO_INDEXES_IN1D));
}
// Calculate basic index by coordinates
function calculate_index_xy(coordinates){
  return ((coordinates / PSIZE) - 1);
}
// Calculate coordinates from given index
function calculateCoordinatesXY(index){
  return (index * PSIZE);
}
// Calculate x index from board index
function calculate_xIndex(board_index){
  return board_index % (board.width / PSIZE);
}
// Calculate y index from board index
function calculate_yIndex(board_index){
  return Math.floor(board_index / (board.height / PSIZE));
}
// Player A is true, player B is false
var whoami = IM_PA;
// Init snake body
function init_my_snake_body(){
  if(whoami){
    my_snake_body = [
      // Snake head
      my_init_pos,
      // Secound element of snake body
      my_init_pos + DIRECTION_LEFT
    ];
  }else{
    my_snake_body = [
      // Snake head
      my_init_pos,
      // Secound element of snake body
      my_init_pos + DIRECTION_RIGHT
    ];
  }
}
// Init opponent snake body
function init_op_snake_body(){
  if(!whoami){
    op_snake_body = [
      // Snake head
      op_init_pos,
      // Secound element of snake body
      op_init_pos + DIRECTION_LEFT
    ];
  }else{
    op_snake_body = [
      // Snake head
      op_init_pos,
      // Secound element of snake body
      op_init_pos + DIRECTION_RIGHT
    ];
  }
}
// Init first player A
function init_player_a(){
  // I am player A
  whoami = IM_PA;
  // My init index on board is 5
  my_init_pos = PA_INIT_INDEX;
  // My init direction is going right
  actual_direction = DIRECTION_RIGHT;
  // Init of my snake
  init_my_snake_body();
  // Init of my opponent
  init_op_player();
  // Start my main loop
  main_loop();
}
// Init Secound player B
function init_player_b(){
  // I am player B
  whoami = IM_PB;
  // My init index on board is 336
  my_init_pos = PB_INIT_INDEX;
  // My init direction is going left
  actual_direction = DIRECTION_LEFT;
  // Init of my snake
  init_my_snake_body();
  // Init of my opponent
  init_op_player();
  // Start my main loop
  main_loop();
}
// Init opponent player
function init_op_player(){
  if(whoami){
    op_init_pos = PB_INIT_INDEX;
  }else{
    op_init_pos = PA_INIT_INDEX;
  }
  init_op_snake_body();
}
// Draw single point
function drawPoint(index_on_board, point_color){
  const x = calculateCoordinatesXY(calculate_xIndex(index_on_board));
  const y = calculateCoordinatesXY(calculate_yIndex(index_on_board));
  context.fillStyle = point_color.color;
  context.strokestyle = point_color.border;
  // The x-axis coordinate of the rectangle's starting point.
  // The y-axis coordinate of the rectangle's starting point.
  context.fillRect(x, y, PSIZE, PSIZE);
  context.strokeRect(x, y, PSIZE, PSIZE);
}
// Draw entire snake
function drawSnake(snake_body, snake_color){
  // Make head more visible - adding black background
  drawPoint(snake_body[0],BLACK_COLOR);
  drawPoint(snake_body[0],BLACK_COLOR); // TODO: change alpha on canvas
  // Draw every point (including head again)
  snake_body.forEach(point => drawPoint(point, snake_color));
}
// Clear whole canvas
function clearCanvas(){
  context.clearRect(0,0,board.width,board.height);
}
// Refresh board - clear Canvas and draw everything 
function refresh_board(){
  // Clear whole canvas
  clearCanvas();
  // Draw cleared food
  drawPoint(food_index, FOOD_COLOR);
  // Draw new snake
  drawSnake(my_snake_body,MY_SNAKE_COLOR);
  // Draw enemy snake
  drawSnake(op_snake_body,OP_SNAKE_COLOR);
}
// Move snake
function move() 
{ 
  // New snake head - in new postition
  // Automatically wraped horizontally (index on board logic)
  var head = my_snake_body[0] + actual_direction;
  // Wrap head index vertically
  if(head > MAX_INDEX){
    head -= MAX_INDEX; 
  }else{
    if(head < 0){
      head += NO_INDEXES_IN1D * NO_INDEXES_IN1D - 1; 
    }
  }
  // Add head to the beginning
  my_snake_body.unshift(head);
  // Check if snake is eating food rn (in new position)
  const is_eating =  my_snake_body[0] === food_index;
  if (is_eating) {
        // TODO: remmember to add score usage Increase score 
        score += 1;
  } else {
    // Pop tail point - last part of my snake body
    my_snake_body.pop();
  }
  // Send head move
  move_on_board(my_snake_body[0]);
  // Refresh board with new move
  refresh_board();
}
// Opponent move
function recived_op_move(board_index){
  // New snake head - in new postition
  var head = board_index;
  // Add head to the beginning
  op_snake_body.unshift(head);
  // Check if snake is eating food rn (in new position)
  const is_eating =  op_snake_body[0] === food_index;
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
  food_index = board_index;
  // Refresh board with new move
  refresh_board();
}
// Check game is lost
function is_lost(){
  const isLost = op_snake_body.find( (point) => point === my_snake_body[0] );
  return isLost;
}
function game_over(){
  console.log("Game is over!");
}
// Send info that you lost
function end_game(){
  still_playing = false;
  document.removeEventListener("keydown", direction_control); 
  document.addEventListener("keydown", game_over);
  // TODO: Send info about losing game
}
// Make one tick of game
function game_tick(){
  // Move snake on key down press
  move();
  // Check if it is end of the game
  if (is_lost()) end_game();
}
// Control direction after keydown event
function direction_control(event) 
{ 
  // Snake actual movement booleans 
  var goingLeft = actual_direction === DIRECTION_LEFT;
  var goingRight = actual_direction === DIRECTION_RIGHT;  
  var goingUp = actual_direction === DIRECTION_UP;
  var goingDown = actual_direction === DIRECTION_DOWN;
  // Get key code
  switch (event.keyCode){
    // If snake wants to go left 
    case LEFT_KEY:
      // If snake isn't going right 
      if(!goingRight){
        // Snake is going left 
        actual_direction = DIRECTION_LEFT;
      }
      break;
    // If snake wants to go right 
    case RIGHT_KEY:
      // If snake isn't going left 
      if(!goingLeft){
        // Snake is going right 
        actual_direction = DIRECTION_RIGHT;
      }
      break;
    // If snake wants to go up 
    case UP_KEY:
      // If snake isn't going down 
      if(!goingDown){
        // Snake is going up 
        actual_direction = DIRECTION_UP;  
      }
      break;
    // If snake wants to go down 
    case DOWN_KEY:
      // If snake isn't going up 
      if(!goingUp){
        // Snake is going up 
        actual_direction = DIRECTION_DOWN;  
      }
      break;
  }
  game_tick();
}
// Main loop
function main_loop() {
  // Tick every 100 ms
  setTimeout(function onTick() {
    game_tick();
    if(!still_playing)
      // End main loop
      return;
    main_loop();
  }, GAME_TICK)
}
// NOTE: To make it single player before starting game
// But to do this remmember about reseting game.
// Move listener
// document.addEventListener("keydown", direction_control);
// Start main loop
// main_loop();
// Generate first food
// gen_food();