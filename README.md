# Atari Breakout

### Georgia Tech ECE6122 Final Project 
* Developing a breakout game with multi-thread and OpenGL in python

    * OpenGL: create 2D graphic for Atari Breakout game
    * Multi-thread: each ball is running on an unique thread. For special function, only that ball would be triggered.

## Statement of Work
### Movement
Elastic collision
* The ball bounce inside the wall and follow the law of reflection: when it hit the wall or the paddle, it will change the movement direction.

Inertia
* If paddle's moving direction is contrary to the x-axis of moving ball, slow down the ball's speed a little bit. Otherwise, accelerate the ball speed.

### Blocks with different strength
* Red: crash after 1 collision
* Green: crash after 2 collision
* Blue: crash after 3 collision
* Yellow: special function for acceleration, double balls, extended paddle, shorten paddle

    * If a brick is hit, its strength will be degraded and the color will be changed. For example, if a green brick is hit, its strength will turn to 1, which means that it will crash after only one time collision. 

### Different level
* Randomize game difficulty by assigning different strength of the bricks.

### Interactive interface
* User could control the paddle's movement by mouse.
* Use the keyboard "Space" to start the game. 

