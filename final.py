
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

screen_width, screen_height = 600, 600

cols = 6
rows = 6

# ball position
point_x, point_y = [0, -screen_height // 2 + 30]

pressLeft, pressRight = False, False
liveBall = False
gameOver = 0

class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50
        self.matrix = []
        with open('level.txt') as f:
            lines = f.readlines()
            for line in lines:
                line_row = []
                for c in line.split(' '):
                    line_row.append(int(c))
                self.matrix.append(line_row)
    
    # create blocks of the breakout game
    def create_wall(self):
        self.blocks = []
        block_individual = []
        row_count = 0
        for row in range(rows):
            block_row = []
            block_count = 0
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height

                # if row < 2:
                #     strength = 3
                # elif row < 4:
                #     strength = 2
                # elif row < 6:
                #     strength  = 1

                strength = self.matrix[row_count][block_count]
                if strength == 0:
                    block_count += 1
                    continue

                lower_left = [-screen_width // 2 + (2 * (col + 1)) + block_x, screen_height // 2 - self.height - (2 * (row + 1)) - block_y]
                higer_left = [-screen_width // 2 + (2 * (col + 1)) + block_x, screen_height // 2 - (2 * (row + 1)) - block_y]
                higher_right = [-screen_width // 2 + self.width + (2 * (col + 1)) + block_x, screen_height // 2 - (2 * (row + 1)) - block_y]
                lower_right = [-screen_width // 2 + self.width + (2 * (col + 1)) + block_x, screen_height // 2 - self.height - (2 * (row + 1)) - block_y]
                
                rect = [lower_left, higer_left, higher_right, lower_right]
                
                block_individual = [rect, strength, False]

                block_row.append(block_individual)
                block_count += 1

            self.blocks.append(block_row)
            row_count += 1

    # draw the blocks
    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    # block_blue
                    glColor3f(69.0/255.0, 177.0/255.0, 232.0/255.0)
                elif block[1] == 2:
                    # block_green
                    glColor3f(86.0/255.0, 174.0/255.0, 87.0/255.0)
                elif block[1] == 1:
                    # block_red
                    glColor3f(242.0/255.0, 85.0/255.0, 96.0/255.0)
                rect = block[0]
                glBegin(GL_QUADS)
                glVertex2f(rect[0][0], rect[0][1])
                glVertex2f(rect[1][0], rect[1][1])
                glVertex2f(rect[2][0], rect[2][1])
                glVertex2f(rect[3][0], rect[3][1])
                glEnd()
                # glFlush()

class Paddle:
    def __init__(self):
        self.reset()

    # paddle movement
    def move(self):
        self.direction = 0
        if pressLeft:
            if self.rect[0][0] > -screen_width // 2:
                self.rect[0][0] -= self.speed
                self.rect[1][0] -= self.speed
                self.direction = -1
        if pressRight:
            if self.rect[1][0] < screen_width // 2:
                self.rect[0][0] += self.speed
                self.rect[1][0] += self.speed
                self.direction = 1

    # draw the paddle
    def draw(self):
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glLineWidth(20)
        glBegin(GL_LINES)
        glVertex2f(self.rect[0][0], self.rect[0][1])
        glVertex2f(self.rect[1][0], self.rect[1][1])
        glEnd()
    
    # initialize/reset the paddle
    def reset(self):
        self.height = 20
        self.width = screen_width // cols
        self.x = self.width // 2
        self.y = screen_height // 2 - self.height
        self.speed = 10
        self.rect = [[-self.x, -self.y], [self.x, -self.y]]
        self.direction = 0
    

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    # ball movement
    def move(self):

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
                        
                    # collision from below
                    if abs(self.rect[1] - block[0][0][1]) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        block[2] = True

                if block[0][0][1] < self.rect[1] and self.rect[1] < block[0][1][1]:
                    # collision from left
                    if abs(self.rect[0] - block[0][0][0]) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        block[2] = True
                    # collision from right
                    if abs(self.rect[0] - block[0][2][0]) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                        block[2] = True

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
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
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
    glColor3f(78.0 // 255.0, 81.0 // 255.0, 139.0 // 255.0)
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

# display the screen content
def display():
    global gameOver, liveBall
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #draw all objects
    wall.draw()
    player_paddle.draw()
    ball.draw()

    if liveBall:
        player_paddle.move()
        gameOver = ball.move()
        if gameOver != 0:
            liveBall = False

    if not liveBall:
        if gameOver == 0:
            drawText(215, screen_height // 2 - 100, 'CLICK SPACE TO START')
        elif gameOver == 1:
            drawText(265, screen_height // 2 - 100, 'YOU WIN')
            drawText(215, screen_height // 2 - 150, 'CLICK SPACE TO START')
        elif gameOver == -1:
            drawText(265, screen_height // 2 - 100, 'YOU LOSE')
            drawText(215, screen_height // 2 - 150, 'CLICK SPACE TO START')

    glFlush()
    glutPostRedisplay()
    glutSwapBuffers()

def init():
    glClearColor(234.0/255.0, 218.0/255.0, 184.0/255.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-screen_width/2, screen_width/2, -screen_height/2, screen_height/2)

def keyPressed(key, x, y):
    global pressLeft, pressRight, liveBall

    # SPACE: start/restart the game
    if key == 32:
        liveBall = True
        ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
        player_paddle.reset()
        wall.create_wall()

    if key == GLUT_KEY_LEFT:
        pressLeft = True

    if key == GLUT_KEY_RIGHT:
        pressRight = True

    glutPostRedisplay()

def keyReleased(key, x, y):
    global pressLeft, pressRight
    
    if key == GLUT_KEY_LEFT:
        pressLeft = False

    if key == GLUT_KEY_RIGHT:
        pressRight = False
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