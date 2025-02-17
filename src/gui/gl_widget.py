from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class GLWidget(QOpenGLWidget):
    def __init__(self, scene_manager, parent=None):
        super().__init__(parent)
        self.scene_manager = scene_manager
        self.last_pos = None
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.zoom = -10.0
        
        # Register as scene observer
        self.scene_manager.add_observer(self)
        
    def minimumSizeHint(self):
        return QSize(400, 400)

    def sizeHint(self):
        return QSize(800, 600)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply camera transformations
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_z, 0, 0, 1)
        
        # Draw grid
        self.draw_grid()
        
        # Draw scene objects
        self.scene_manager.draw_all()

    def draw_grid(self):
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINES)
        for i in range(-5, 6):
            glVertex3f(i * 2.0, -10.0, 0)
            glVertex3f(i * 2.0, 10.0, 0)
            glVertex3f(-10.0, i * 2.0, 0)
            glVertex3f(10.0, i * 2.0, 0)
        glEnd()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            self.last_pos = event.pos()
            return
            
        dx = event.pos().x() - self.last_pos.x()
        dy = event.pos().y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rot_y += dx * 0.5
            self.rot_x += dy * 0.5
            self.update()
        elif event.buttons() & Qt.RightButton:
            self.zoom += dy * 0.1
            self.update()
            
        self.last_pos = event.pos()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.01
        self.update()

    def scene_updated(self):
        """Called when the scene changes"""
        self.update()

    def get_scene_manager(self):
        return self.scene_manager