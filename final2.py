import pygame
from pygame.locals import *
import sys
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

screen_width, screen_height = 600, 600

cols = 6
rows = 6
fps = 60


# Number of the glut window.
window = 0

left = [-screen_width // cols // 2, -300 + 20]
right = [screen_width // cols // 2, -300 + 20]

point_x, point_y = [0, -300 + 30]

def key_callback(window, key, scancode, action, mode):
	if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
		glfw.set_window_should_close(window, GL_TRUE)


class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50
    
    def create_wall(self):
        self.blocks = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                # rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength  = 1

                lower_left = (-200 + (2 * (col + 1)) + block_x, 250 - (2 * (row + 1)) - block_y)
                higer_left = (-200 + (2 * (col + 1)) + block_x, 300 - (2 * (row + 1)) - block_y)
                higher_right = (-300 + (2 * (col + 1)) + block_x, 300 - (2 * (row + 1)) - block_y)
                lower_right = (-300 + (2 * (col + 1)) + block_x, 250 - (2 * (row + 1)) - block_y)
                
                rect = [lower_left, higer_left, higher_right, lower_right]
                
                block_individual = [rect, strength]

                block_row.append(block_individual)

            self.blocks.append(block_row)


    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    # block_col = block_blue
                    glColor3f(69.0/255.0, 177.0/255.0, 232.0/255.0)
                elif block[1] == 2:
                    # block_col = block_green
                    glColor3f(86.0/255.0, 174.0/255.0, 87.0/255.0)
                elif block[1] == 1:
                    # block_col = block_red
                    glColor3f(242.0/255.0, 85.0/255.0, 96.0/255.0)
                rect = block[0]
                glBegin(GL_QUADS)
                glVertex2f(rect[0][0], rect[0][1])
                glVertex2f(rect[1][0], rect[1][1])
                glVertex2f(rect[2][0], rect[2][1])
                glVertex2f(rect[3][0], rect[3][1])
                glEnd()
                glFlush()

class Paddle:
    def __init__(self):
        self.reset()

    # def move(self):
    #     self.direction = 0
    #     key = pygame.key.get_pressed()
        # if key[pygame.K_LEFT] and self.rect[0][0] > 0:
        #     for i in range(4):
        #         self.rect[i][0] -= self.speed
        #     self.direction = -1
        # if key[pygame.K_RIGHT] and self.rect[2][0] < screen_width:
        #     for i in range(4):
        #         self.rect[i][0] += self.speed
        #     self.direction = 1
    
    def draw(self):
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glLineWidth(20)
        glBegin(GL_LINES)
        glVertex2f(self.rect[0][0], self.rect[0][1])
        glVertex2f(self.rect[1][0], self.rect[1][1])
        glEnd()
        glFlush()
    
    def reset(self):
        self.height = 20
        self.width = screen_width // cols
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = (left, right)
        self.direction = 0
    

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def move(self):

    #     collision_thresh = 5

    #     wall_destroyed = 1
    #     row_count = 0
    #     for row in wall.blocks:
    #         block_count = 0
    #         for block in row:

    #             if self.rect.colliderect(block[0]):
    #                 # collision form above
    #                 if abs(self.rect.bottom - block[0].top) < collision_thresh and self.speed_y > 0:
    #                     self.speed_y *= -1
    #                 # collision form below
    #                 if abs(self.rect.top - block[0].bottom) < collision_thresh and self.speed_y < 0:
    #                     self.speed_y *= -1
    #                 # collision form left
    #                 if abs(self.rect.right - block[0].left) < collision_thresh and self.speed_x > 0:
    #                     self.speed_x *= -1
    #                 # collision form right
    #                 if abs(self.rect.left - block[0].right) < collision_thresh and self.speed_x < 0:
    #                     self.speed_x *= -1
                    
    #                 if wall.blocks[row_count][block_count][1] > 1:
    #                     wall.blocks[row_count][block_count][1] -= 1
    #                 else:
    #                     wall.blocks[row_count][block_count][0] = (0, 0, 0, 0)
                
    #             if wall.blocks[row_count][block_count][0] != (0, 0, 0, 0):
    #                 wall_destroyed = 0
    #             block_count += 1
    #         row_count += 1

    #     if wall_destroyed == 1:
    #         self.game_over = 1
                    


        if self.rect[0] < -screen_width // 2 or self.rect[0] > screen_width // 2:
            self.speed_x *= -1
        
        if self.rect[1] < screen_height // 2:
            self.speed_y *= -1
        if self.rect[1] > screen_height:
            self.game_over = -1

    #     if self.rect.colliderect(player_paddle):

    #         if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
    #             self.speed_y *= -1
    #             self.speed_x += player_paddle.direction
    #             if self.speed_x > self.speed_max:
    #                 self.speed_x = self.speed_max
    #             elif self.speed_x < 0 and self.speed_x < -self.speed_max:
    #                 self.speed_x = - self.speed_max
    #         else:
    #             self.speed_x *= -1

        self.rect[0] += self.speed_x
        self.rect[1] += self.speed_y

    #     return self.game_over

    def draw(self):
        # pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        # pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glPointSize(20)
        glEnable(GL_POINT_SMOOTH)
        glBegin(GL_POINTS)
        glVertex2f(self.rect[0], self.rect[1])
        glEnd()
        glFlush()

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        # self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.rect = [point_x, point_y]
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.RESIZABLE, GL_FALSE)


window = glfw.create_window(screen_width, screen_height, "Breakout", None, None)

glfw.make_context_current(window)

glfw.set_key_callback(window, key_callback)

glViewport(0, 0, screen_width, screen_height)

glEnable(GL_CULL_FACE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     wall = Wall()
#     wall.create_wall()
#     wall.draw()

#     player_paddle = Paddle()
#     player_paddle.draw()
#     ball = Ball(point_x, point_y)
#     ball.draw()
#     ball.move()
#     glutPostRedisplay()
#     glutSwapBuffers()

# def init():
#     glClearColor(234.0/255.0, 218.0/255.0, 184.0/255.0, 1.0)
#     gluOrtho2D(-screen_width/2, screen_width/2, -screen_height/2, screen_height/2)

# def keyPressed(key, x, y):
#     global window
# 	# If escape is pressed, kill everything.
#     if key == ESCAPE:
#         sys.exit()
#     global left, right
#     if key == b'a' and left[0] > -screen_width // 2:
#         left[0] -= 10
#         right[0] -= 10
#     if key == b'd' and right[0] < screen_width // 2:
#         left[0] += 10
#         right[0] += 10
#     glutPostRedisplay()

wall = Wall()
wall.create_wall()
wall.draw()

deltaTime = 0.0
lastFrame = 0.0

while not glfw.window_should_close(window):
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame

    glfw.poll_events()

    glClearColor(234.0/255.0, 218.0/255.0, 184.0/255.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glfw.swap_buffers(window)

glfw.terminate()