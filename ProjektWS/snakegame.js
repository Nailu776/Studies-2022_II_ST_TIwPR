//* Snake Game  */
// TODO: usage Score 
let score = 0;    
// Get canvas board element
var board = document.getElementById('mySnakeCanvas');
// Get context
var context = board.getContext('2d');
// Set global alpha - to notice when snake is folding 
context.globalAlpha = 0.7;
// Move listener
// TODO: delete
// document.addEventListener("keydown", direction_control);
// Food params
let food = {
  x: 0,
  y: 0
};
// Init position
var my_init_pos = 200;
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
// Enemy snake color
const enemy_snake_color = {
  color: 'yellow',
  border: 'black'
};
// Food color
const food_color = {
  color: 'red',
  border: 'black'
};
// Actual direction
var actual_direction = {
  dx: delta,
  dy: 0
};
// Snake init body - 2 elems
var snake_body = [
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
// Init first player A
function init_player_a(){
  my_init_pos = 120;
  actual_direction = {
    dx: delta,
    dy: 0
  };
  init_snake_body();
  // Start main loop
  main_loop();
}
// Init Secound player B
function init_player_b(){
  my_init_pos = 640;
  actual_direction = {
    dx: -delta,
    dy: 0
  };
  init_snake_body();
  // Start main loop
  main_loop();
}
// Init snake body
function init_snake_body(){
  snake_body = [
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
  drawPoint(snake_body[0],{color:'black', border:'black'});
  // Draw every point (including head again)
  snake_body.forEach(point => drawPoint(point, my_snake_color));
}
// Clear whole canvas
function clearCanvas(){
  context.clearRect(0,0,board.width,board.height);
}
// Move snake
function move() 
{ 
  // New snake head - in new postition
  head = {
    x: snake_body[0].x + actual_direction.dx, 
    y: snake_body[0].y + actual_direction.dy
  };
  // Add head to the beginning
  snake_body.unshift(head);
  // Check if snake is eating food rn (in new position)
  const is_eating = 
    snake_body[0].x === food.x && 
    snake_body[0].y === food.y;
  if (is_eating) {
        // TODO: remmember to add score usage Increase score 
        score += 1;
        // Generate food
        gen_food();
  } else {
    // Pop tail point - last part of my snake body
    snake_body.pop();
  }
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
  // Clear whole canvas
  clearCanvas();
  // Draw cleared food
  drawFood();
  // Draw new snake
  drawSnake();
  // Check if it is end of the game
  // if (is_end()) return;
}
// TODO: Serwer sending end of game after hitting player
function is_end()
{ 
  return false;
}
// TODO: server stuff Randomize food location -- 
function random_food(min, max)
{  
   return Math.round((Math.random() * (max-min) + min) / delta) * delta;
}
// TODO: server stuff generate food 
function gen_food() 
{  
   food.x = random_food(0, board.width - delta);
   food.y = random_food(0, board.height - delta);
   // Check every point of snake body - if it is covering food
   snake_body.forEach(function is_covering_snake(part) {
        const covers = part.x == food.x && part.y == food.y;
        // If randomized food is covering snake - generate new.
        if (covers) gen_food();
      });
}
// Draw food
function drawFood(){
  drawPoint({x:food.x, y:food.y,}, food_color);
}
// Main loop
function main_loop() {
  console.log(snake_body[0].x)
  // Check if it is end of the game
  if (is_end()) return;
  // Tick every 100 ms
  setTimeout(function onTick() {
    // Clear whole canvas
    clearCanvas();
    // Draw cleared food
    drawFood();
    // Move snake 
    move();
    // Draw new snake
    drawSnake();
    // Call main again
    main_loop();
  }, 1000)
}
// TODO: delete starting main loop
// Start main loop
//main_loop();
// Generate first food
gen_food();