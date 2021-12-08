'''
Author: Szu-Yung Huang, Jyun-Yan Lu
Class: ECE6122 
Last Date Modified: Dec, 7 2021 
 
Description: 
    Developing a breakout game with multi-thread and OpenGL in python

'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import threading
from wall import *
from paddle import *
from ball import *

screen_width, screen_height = 600, 600

cols = 6
rows = 6

# ball position
point_x, point_y = [0, -screen_height // 2 + 30]

# control flag
prolongPaddle = False
accBallSpeed = False
shortenPaddle = False
doubleBall = False
waitTocontinue = True
gamingFlag = False
liveBall = False
oneTimeFlag = True

# game over control
gameOver = 0
gameOver1 = 0
    

class Ball:
    def __init__(self, x, y):
        t = threading.Thread(target=self.reset, args=(x, y))
        t.start()
        # self.reset(x, y)
    
    # ball movement
    def move(self):
        global prolongPaddle, accBallSpeed, shortenPaddle, doubleBall, phitTime, ahitTime, shitTime
        
        # detect the collision distance
        collision_thresh = 10
        
        row_count = 0
        for row in wall.blocks:
            block_count = 0
            for block in row:

                if block[0][0][0] < self.rect[0] and self.rect[0] < block[0][3][0]:
                    # collision from above
                    if abs(self.rect[1] - block[0][1][1]) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                        block[2] = True

                        if block[3] == 1:
                            phitTime = time.time()
                            prolongPaddle = True
                        elif block[3] == 2:
                            shitTime = time.time()
                            shortenPaddle = True
                        elif block[3] == 3:
                            ahitTime = time.time()
                            accBallSpeed = True
                        elif block[3] == 4:
                            doubleBall = True

                    # collision from below
                    if abs(self.rect[1] - block[0][0][1]) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        block[2] = True

                        if block[3] == 1:
                            phitTime = time.time()
                            prolongPaddle = True
                        elif block[3] == 2:
                            shitTime = time.time()
                            shortenPaddle = True
                        elif block[3] == 3:
                            ahitTime = time.time()
                            accBallSpeed = True
                        elif block[3] == 4:
                            doubleBall = True

                if block[0][0][1] < self.rect[1] and self.rect[1] < block[0][1][1]:
                    # collision from left
                    if abs(self.rect[0] - block[0][0][0]) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        block[2] = True
                        if block[3] == 1:
                            phitTime = time.time()
                            prolongPaddle = True
                        elif block[3] == 2:
                            shitTime = time.time()
                            shortenPaddle = True
                        elif block[3] == 3:
                            ahitTime = time.time()
                            accBallSpeed = True
                        elif block[3] == 4:
                            doubleBall = True

                    # collision from right
                    if abs(self.rect[0] - block[0][2][0]) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                        block[2] = True
                        if block[3] == 1:
                            phitTime = time.time()
                            prolongPaddle = True
                        elif block[3] == 2:
                            shitTime = time.time()
                            shortenPaddle = True
                        elif block[3] == 3:
                            ahitTime = time.time()
                            accBallSpeed = True
                        elif block[3] == 4:
                            doubleBall = True
                
                # if collision with block, make it downgraded or diappeared
                if wall.blocks[row_count][block_count][1] > 1 and wall.blocks[row_count][block_count][2]:
                    wall.blocks[row_count][block_count][1] -= 1
                    wall.blocks[row_count][block_count][2] = False
                elif wall.blocks[row_count][block_count][1] == 1 and wall.blocks[row_count][block_count][2]:
                    del wall.blocks[row_count][block_count]
                
                block_count += 1
            row_count += 1
        
        # all blocks are disappeared, win the game
        if wall.blocks == [[]]:
            self.game_over = 1
                    
        # hitting left and right screen 
        if self.rect[0] < -screen_width // 2 or self.rect[0] > screen_width // 2:
            self.speed_x *= -1
        
        # hitting top screen
        if self.rect[1] > screen_height // 2:
            self.speed_y *= -1
        
        # did not catch the ball (screen bottom)
        if self.rect[1] < -screen_height // 2:
            self.game_over = -1

        # collision with paddle
        if player_paddle.rect[0][0] < self.rect[0] and self.rect[0] < player_paddle.rect[1][0]:
            if abs(self.rect[1] - player_paddle.rect[0][1]) < collision_thresh and self.speed_y < 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = - self.speed_max

        self.rect[0] += self.speed_x
        self.rect[1] += self.speed_y

        return self.game_over

    # Draw the ball
    def draw(self):
        # glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(20)
        glEnable(GL_POINT_SMOOTH)
        glBegin(GL_POINTS)
        glVertex2f(self.rect[0], self.rect[1])
        glEnd()
        # glFlush()

    # initialize/reset the ball
    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = [point_x, point_y]
        self.speed_x = 4
        self.speed_y = 4
        self.speed_max = 5
        self.game_over = 0

# show the instruction text on the screen
def drawText(x, y, s):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, screen_width, 0.0, screen_height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # glColor3f(78.0 // 255.0, 81.0 // 255.0, 139.0 // 255.0)
    glColor3f(1.0, 1.0, 139.0 // 255.0)
    glRasterPos2i(x, y)

    font = GLUT_BITMAP_9_BY_15
    for c in s:
        glutBitmapCharacter(font, ord(c))
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()



wall = Wall()
wall.create_wall()

player_paddle = Paddle()

ball = Ball(point_x, point_y)
ball2 = Ball(point_x, point_y)

stopTime = 0.0

# display the screen content
def display():
    # global lastFrame
    # currentFrame = glutGet(GLUT_ELAPSED_TIME)
    # deltaTime = currentFrame - lastFrame
    # lastFrame = currentFrame

    global gameOver, gameOver1, liveBall, doubleBall
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    

    #draw all objects
    wall.draw()
    player_paddle.draw()
    ball.draw()
    
    global oneTimeFlag, prolongPaddle, accBallSpeed, shortenPaddle, gamingFlag, stopTime, waitTocontinue
    if prolongPaddle:
        if int(time.time() - phitTime) < 5:
            if oneTimeFlag:
                player_paddle.rect[0][0] = player_paddle.rect[0][0] - 50
                player_paddle.rect[1][0] = player_paddle.rect[1][0] + 50
                oneTimeFlag = False
        else:
            player_paddle.rect[0][0] = player_paddle.rect[0][0] + 50
            player_paddle.rect[1][0] = player_paddle.rect[1][0] - 50
            oneTimeFlag = True
            prolongPaddle = False
    
    if shortenPaddle:
        if int(time.time() - shitTime) < 5:
            if oneTimeFlag:
                player_paddle.rect[0][0] = player_paddle.rect[0][0] + 20
                player_paddle.rect[1][0] = player_paddle.rect[1][0] - 20
                oneTimeFlag = False
        else:
            player_paddle.rect[0][0] = player_paddle.rect[0][0] - 20
            player_paddle.rect[1][0] = player_paddle.rect[1][0] + 20
            oneTimeFlag = True
            shortenPaddle = False
    
    if accBallSpeed:
        if int(time.time() - ahitTime) < 5:
            if oneTimeFlag:
                ball.speed_x *= 2
                ball.speed_y *= 2
                oneTimeFlag = False
        else:
            ball.speed_x //= 2
            ball.speed_y //= 2
            oneTimeFlag = True
            accBallSpeed = False


    if liveBall:
        player_paddle.move()
        gameOver = ball.move()
        if doubleBall:
            ball2.draw()
            gameOver1 = ball2.move()
            if gameOver != 0 and gameOver1 != 0:
                liveBall = False
        if not doubleBall and gameOver != 0:
            liveBall = False

    if not liveBall:
        if waitTocontinue:
            stopTime = time.time()
            waitTocontinue = False
        if gameOver == 0:
            drawText(215, screen_height // 2 - 100, 'CLICK SPACE TO START')
            gamingFlag = False
        elif gameOver == 1:
            drawText(265, screen_height // 2 - 100, 'YOU WIN')
            if int(time.time() - stopTime) < 3:
                drawText(190, screen_height // 2 - 150, 'WAIT 3 SECONDS FOR RESTART') 
                gamingFlag = True
            else:
                drawText(215, screen_height // 2 - 150, 'CLICK SPACE TO START')
                gamingFlag = False
        elif gameOver == -1:
            drawText(265, screen_height // 2 - 100, 'YOU LOSE')
            if int(time.time() - stopTime) < 3:
                drawText(190, screen_height // 2 - 150, 'WAIT 3 SECONDS FOR RESTART') 
                gamingFlag = True  
            else:
                drawText(215, screen_height // 2 - 150, 'CLICK SPACE TO START')
                gamingFlag = False

    glFlush()
    glutPostRedisplay()
    glutSwapBuffers()

def init():
    # glClearColor(234.0/255.0, 218.0/255.0, 184.0/255.0, 1.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-screen_width/2, screen_width/2, -screen_height/2, screen_height/2)

def keyPressed(key, x, y):
    global liveBall, gamingFlag, doubleBall, waitTocontinue

    # SPACE: start/restart the game
    if key == 32:
        if not gamingFlag:
            liveBall = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            ball2.reset(player_paddle.x + (player_paddle.width // 2),
                    player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
            gamingFlag = True
            doubleBall = False
            waitTocontinue = True


    if key == GLUT_KEY_LEFT:
        player_paddle.pressLeft = True

    if key == GLUT_KEY_RIGHT:
        player_paddle.pressRight = True

    glutPostRedisplay()

def keyReleased(key, x, y):
    # global pressLeft, pressRight
    
    if key == GLUT_KEY_LEFT:
        player_paddle.pressLeft = False

    if key == GLUT_KEY_RIGHT:
        player_paddle.pressRight = False
    glutPostRedisplay()


def main():

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screen_width, screen_height)
    window = glutCreateWindow("Breakout")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(keyPressed)
    glutSpecialUpFunc(keyReleased)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()