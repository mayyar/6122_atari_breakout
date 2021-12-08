from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import threading

screen_width, screen_height = 600, 600

cols = 6
rows = 6

class Wall:
    def __init__(self):
        '''
        special function: 
        1. prolong, 2. shorten, 3. accelerate, 4. two balls 
        '''
        self.width = screen_width // cols
        self.height = 30
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

        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height

                strength = self.matrix[row][col] // 10
                special = self.matrix[row][col] % 10
                if strength == 0:
                    col += 1
                    continue

                lower_left = [-screen_width // 2 + (5 * (col + 1)) + block_x, screen_height // 2 - self.height - (5 * (row + 1)) - block_y]
                higer_left = [-screen_width // 2 + (5 * (col + 1)) + block_x, screen_height // 2 - (5 * (row + 1)) - block_y]
                higher_right = [-screen_width // 2 + self.width + (5 * (col + 1)) + block_x, screen_height // 2 - (5 * (row + 1)) - block_y]
                lower_right = [-screen_width // 2 + self.width + (5 * (col + 1)) + block_x, screen_height // 2 - self.height - (5 * (row + 1)) - block_y]
                
                rect = [lower_left, higer_left, higher_right, lower_right]
                
                block_individual = [rect, strength, False, special] # x y position, strength, hit or not, special function

                block_row.append(block_individual)

            self.blocks.append(block_row)

    # draw the blocks
    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[3] != 0:
                    glColor3f(1.0, 1.0, 0.0)
                elif block[1] == 3:
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