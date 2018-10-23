import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# IMPORT OBJECT LOADER
from OBJ import *

filename = sys.argv[1]
pygame.init()
viewport = (800, 600)
hx = viewport[0] / 2
hy = viewport[1] / 2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
obj = OBJ(filename, True)
# obj = OBJ("mean_face.obj", True)

glNormal3f(0.0, 0.0, 1.0)
glEnable(GL_NORMALIZE)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width / float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
rotate = move = False

project = glGetFloat(GL_PROJECTION_MATRIX)
viewport = glGetInteger(GL_VIEWPORT)


def GetOGLPos(x, y):
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    winX = x
    winY = viewport[3] - y
    winZ = glReadPixels(x, int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

    posX, posY, posZ = gluUnProject(winX, winY, winZ, modelview, projection, viewport)

    glBegin(GL_POINTS)
    glVertex3f(posX, posY, posZ)
    glEnd()

    print posX, posY, posZ
    return posX, posY, posZ


def draw_point(x, y, z):
    glPointSize(10)
    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_POINTS)
    glVertex3f(x,y,z)
    glEnd()

while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos = max(1, zpos - 1)
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True

        elif e.type == KEYDOWN and e.key == K_c:
            winx, winy = pygame.mouse.get_pos()
            x, y, z = GetOGLPos(winx, winy)
            winz = glReadPixels(winx, winy, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            index = search_index(x,y,z)
            # draw_point(x, y, z)

        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)

    pygame.display.flip()
