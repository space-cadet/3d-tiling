import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QDockWidget,
                             QVBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtOpenGLWidgets import QOpenGLWidget  # Correct import location
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class TetrahedraGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
        
        # Draw a simple triangle for testing
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 1.0, 0.0)
        glEnd()

class TetrahedraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetrahedra Tiling")
        
        # Create OpenGL widget as central widget
        self.gl_widget = TetrahedraGLWidget(self)
        self.setCentralWidget(self.gl_widget)
        
        # Create dock widgets
        self.setup_docks()
        
        # Create menu bar
        self.setup_menu()
        
        # Restore previous layout if exists
        self.restore_layout()
        
        # Set initial window size
        self.resize(1200, 800)

    def setup_docks(self):
        # Scene Info Dock
        self.scene_info_dock = QDockWidget("Scene Info", self)
        scene_info_widget = QWidget()
        scene_info_layout = QVBoxLayout()
        scene_info_layout.addWidget(QLabel("Total Tetrahedra: 0"))
        scene_info_widget.setLayout(scene_info_layout)
        self.scene_info_dock.setWidget(scene_info_widget)
        
        # Object List Dock
        self.object_list_dock = QDockWidget("Objects", self)
        object_list_widget = QWidget()
        object_list_layout = QVBoxLayout()
        object_list_layout.addWidget(QLabel("Object List"))
        object_list_widget.setLayout(object_list_layout)
        self.object_list_dock.setWidget(object_list_widget)
        
        # Properties Dock
        self.properties_dock = QDockWidget("Properties", self)
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()
        properties_layout.addWidget(QLabel("Properties"))
        properties_widget.setLayout(properties_layout)
        self.properties_dock.setWidget(properties_widget)
        
        # Tools Dock
        self.tools_dock = QDockWidget("Tools", self)
        tools_widget = QWidget()
        tools_layout = QVBoxLayout()
        tools_layout.addWidget(QPushButton("New Tetrahedron"))
        tools_widget.setLayout(tools_layout)
        self.tools_dock.setWidget(tools_widget)
        
        # Set dock features
        for dock in [self.scene_info_dock, self.object_list_dock,
                    self.properties_dock, self.tools_dock]:
            dock.setFeatures(QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetMovable |
                           QDockWidget.DockWidgetClosable)
        
        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.scene_info_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.object_list_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.properties_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tools_dock)

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        # Add actions to show/hide docks
        view_menu.addAction(self.scene_info_dock.toggleViewAction())
        view_menu.addAction(self.object_list_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.tools_dock.toggleViewAction())

    def save_layout(self):
        settings = QSettings('Block', 'TetrahedraTiling')
        settings.setValue('windowGeometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        
    def restore_layout(self):
        settings = QSettings('Block', 'TetrahedraTiling')
        if settings.value('windowGeometry'):
            self.restoreGeometry(settings.value('windowGeometry'))
        if settings.value('windowState'):
            self.restoreState(settings.value('windowState'))
            
    def closeEvent(self, event):
        self.save_layout()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = TetrahedraApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()