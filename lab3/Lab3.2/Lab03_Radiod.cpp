#include <gl/gl.h>
#include <gl/glu.h>
#include <gl/glut.h>
#include <fstream>
#include <iostream>
#include <wtypes.h>
#include <math.h>
using namespace std;
#define radian 3.141592654*2/180.0
#define SIZEBOARD 720 // kich thuoc window


typedef GLfloat twodimpoint[2];
float radius = 1; // more than this gets ugl
int limit = 180;
void initGL() {
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f); // Set background color to black and opaque
    glClearDepth(1.0f);                   // Set background depth to farthest
    glEnable(GL_DEPTH_TEST);   // Enable depth testing for z-culling
    glDepthFunc(GL_LEQUAL);    // Set the type of depth-test
    glShadeModel(GL_SMOOTH);   // Enable smooth shading
    gluOrtho2D(-3, 3, -3, 3);
    //GetDesktopResolution();
    //glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);  // Nice perspective corrections
}

void drawCircle(float temp){
    glPushMatrix();
    glBegin(GL_LINE_STRIP);
    for(int i = 0; i <= 180; i++){
        glVertex2f(temp*cos(radian*i), temp*sin(radian*i));
    }
    glEnd();
    glPopMatrix();
}


void display(){
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glColor3f(0.0, 0.0, 0.0);
    twodimpoint arrPoint[limit];
    for(int i = 0; i <limit; i++){
        arrPoint[i][0] = radius*cos(i*radian);
        arrPoint[i][1] = radius*sin(i*radian);
        glPushMatrix();
        glRotated(i*2.0, 0.0, 0.0, 1.0);
        glTranslated(0.0, radius, 0.0);
        drawCircle(sqrt(pow(arrPoint[i][0], 2) + pow(arrPoint[i][1] - radius, 2)));
        glPopMatrix();
    }
    glutSwapBuffers();
}

void keyboard(int key, int x, int y){
    switch(key){
    case GLUT_KEY_DOWN:
        limit--;
        if(limit < 0)
            limit = 0;
        glutPostRedisplay();
        break;
    case GLUT_KEY_UP:
        limit++;
        if(limit > 180)
            limit = 180;
        glutPostRedisplay();
        break;
    }
}

int main(int argc, char** argv){
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
    glutInitWindowSize(SIZEBOARD, SIZEBOARD);
    glutInitWindowPosition(300, 0);

    glutCreateWindow("radiod");
    glutDisplayFunc(display);
    glutSpecialFunc(keyboard);
    initGL();

    glutMainLoop();

}
