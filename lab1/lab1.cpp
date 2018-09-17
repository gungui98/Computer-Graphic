#include <GL/glut.h>

#include <math.h>

/**
* make: g++ main.cpp -o string -lglut -lGLU -lGL
 * */

void displayMe(void)
{
    // Lệnh xóa nền
    glBegin(GL_POLYGON);		    
        glVertex3f(0.25, 0.25, 0.0);
        glVertex3f(0.75, 0.25, 0.0);
        glVertex3f(0.75, 0.75, 0.0);
        glVertex3f(0.25, 0.75, 0.0);
    glEnd();
    glFlush();			
    glutSwapBuffers();

}
 
int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(400, 300);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Hello world!");
    glutDisplayFunc(displayMe);
    glutMainLoop();
    return 0;
}