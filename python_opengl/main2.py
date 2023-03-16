import OpenGL
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


class ClassThing:
    def __init__(self):
        self.Splash = True

    def TexFromPNG(self, filename):
        img = Image.open(filename)
        img_data = numpy.array(list(img.getdata()), numpy.uint8)

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Texture parameters are part of the texture object, so you need to 
        # specify them only once for a given texture object.
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return texture

    def run(self):
        glutInitDisplayMode(GLUT_RGBA)

        glutInitWindowSize(256,224)
        self.window = glutCreateWindow("GL")
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)

        self.MainTex = glGenTextures(1)
        self.SplashTex = self.TexFromPNG("misc/mars.png")

        glutMainLoop()

    def reshape(self, width, height):
        self.width = width
        self.height = height
        glutPostRedisplay();

    def draw(self):
        glViewport(0, 0, self.width, self.height)

        glClearDepth(1) # just for completeness
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity()

        if self.Splash:
            glBindTexture(GL_TEXTURE_2D, self.SplashTex)
        else:
            glBindTexture(GL_TEXTURE_2D, self.MainTex)

        # it's a good idea to enable state right before you need it
        # there's no such thing like global state intialization in
        # OpenGL
        glEnable(GL_TEXTURE_2D)
        # vertex arrays must be enabled using glEnableClientState
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        Varray = numpy.array([[0,0],[0,1],[1,1],[1,0]],numpy.float64)
        glVertexPointer(2,GL_FLOAT,0,Varray)
        glTexCoordPointer(2,GL_FLOAT,0,Varray)
        indices = [0,1,2,3]
        glDrawElements(GL_QUADS,1,GL_UNSIGNED_SHORT,indices)

        # This implies a glFinish, which includes a glFlush
        glutSwapBuffers() 

# GLUT initialization in program global, so initialize it on
# the process level. It might be 
glutInit(sys.argv)

thing = ClassThing()
thing.run()
