import OpenGL
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def cube():
    glColor3f(1.0, 0.0, 3.0) # Set the color to pink
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


#def texture():
rect_prism_surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def gen_rect_prism_vertices(xloc,yloc,zloc,x,y,z):
    x *= 0.5
    y *= 0.5
    z *= 0.5
    vertices = (
        (xloc+x, yloc-y, zloc-z),
        (xloc+x, yloc+y, zloc-z),
        (xloc-x, yloc+y, zloc-z),
        (xloc-x, yloc-y, zloc-z),
        (xloc+x, yloc-y, zloc+z),
        (xloc+x, yloc+y, zloc+z),
        (xloc-x, yloc-y, zloc+z),
        (xloc-x, yloc+y, zloc+z)
        )
    return vertices


def block(xloc,yloc,zloc,x,y,z):
    glEnable(GL_TEXTURE_2D)
    textID = read_texture("mars.png")
    # glBindTexture(GL_TEXTURE_2D,textID)
    vertices = gen_rect_prism_vertices(xloc,yloc,zloc,x,y,z)
    for surface in rect_prism_surfaces:
        n = 0
        glBegin(GL_QUADS)
        for vertex in surface:
            if n == 0:
                xv = 0.0
                yv = 0.0
            if n == 1:
                xv = 1.0
                yv = 0.0
            if n == 2:
                xv = 1.0
                yv = 1.0
            if n == 3:
                xv = 0.0
                yv = 1.0
            glTexCoord2f(xv,yv); glVertex3fv(vertices[vertex])
            n += 1
        glEnd()

def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


def square():
    glColor3f(0.0, 3.0, 0.0) # Set the color to pink
    glBegin(GL_QUADS) # Begin the sketch
    glVertex2f(1, 1) # Coordinates for the bottom left point
    glVertex2f(2, 1) # Coordinates for the bottom right point
    glVertex2f(2, 2) # Coordinates for the top right point
    glVertex2f(1, 2) # Coordinates for the top left point
    glEnd() # Mark the end of drawing


# Add this function before Section 2 of the code above i.e. the showScreen function
def iterate():
    glViewport(100, 100, 300, 300)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 3, 0.0, 3, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
    glLoadIdentity() # Reset all graphic/shape's position
    # We have to declare the points in this sequence: bottom left, bottom right, top right, top left
    iterate()
    cube()
    square()
    block(1,1,1,1,2,3)
    glutSwapBuffers()


def main():
    glutInit() # Initialize a glut instance which will allow us to customize our window
    glutInitDisplayMode(GLUT_RGBA) # Set the display mode to be colored
    glutInitWindowSize(500, 500)   # Set the width and height of your window
    glutInitWindowPosition(0, 0)   # Set the position of the window
    wind = glutCreateWindow("Python OpenGL Example") # Give your window a title
    glutDisplayFunc(display)  # Tell OpenGL to call the showScreen method continuously
    glutIdleFunc(display)     # Draw any graphics or shapes in the showScreen function at all times
    glutMainLoop()  # Keeps the window created above displaying/running in a loop

if __name__ == '__main__':
    main()
