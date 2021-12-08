from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

screen_width, screen_height = 600, 600

cols = 6
rows = 6

class Paddle:
    def __init__(self):
        self.reset()

    # paddle movement
    def move(self):
        self.direction = 0
        if self.pressLeft:
            if self.rect[0][0] > -screen_width // 2:
                self.rect[0][0] -= self.speed
                self.rect[1][0] -= self.speed
                self.direction = -1
        if self.pressRight:
            if self.rect[1][0] < screen_width // 2:
                self.rect[0][0] += self.speed
                self.rect[1][0] += self.speed
                self.direction = 1

    # draw the paddle
    def draw(self):
        # glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(20)
        glBegin(GL_LINES)
        glVertex2f(self.rect[0][0], self.rect[0][1])
        glVertex2f(self.rect[1][0], self.rect[1][1])
        glEnd()
    
    # def special(self):
    #     self.rect = [[-self.x - 100, -self.y], [self.x + 100, -self.y]]

    # initialize/reset the paddle
    def reset(self):
        self.pressLeft = False
        self.pressRight = False
        self.height = 20
        self.width = screen_width // cols
        self.x = self.width // 2
        self.y = screen_height // 2 - self.height
        self.speed = 10
        self.rect = [[-self.x, -self.y], [self.x, -self.y]]
        self.direction = 0