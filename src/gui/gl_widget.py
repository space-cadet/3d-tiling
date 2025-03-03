from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, QSize
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class GLWidget(QOpenGLWidget):
    def __init__(self, scene_manager, parent=None):
        super().__init__(parent)
        self.scene_manager = scene_manager
        self.last_pos = None
        
        # Camera transformations
        self.camera_rot_x = 0.0
        self.camera_rot_y = 0.0
        self.camera_rot_z = 0.0
        self.camera_pan_x = 0.0
        self.camera_pan_y = 0.0
        self.zoom = -10.0

        # Initialize light positions with default values
        self.light0_pos = [15.0, 15.0, 15.0, 1.0]
        self.light1_pos = [-15.0, -15.0, 15.0, 1.0]
        self.light2_pos = [0.0, 0.0, 20.0, 1.0]
        
        # Object transformations
        self.object_rot_x = 0.0
        self.object_rot_y = 0.0
        self.object_rot_z = 0.0
        
        # Register as scene observer
        self.scene_manager.add_observer(self)
        
        # Set focus policy to accept keyboard input
        self.setFocusPolicy(Qt.StrongFocus)
        
    def minimumSizeHint(self):
        return QSize(400, 400)

    def sizeHint(self):
        return QSize(800, 600)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.3, 0.3, 0.35, 1.0)  # Brighter neutral background
        
        # Configure lights
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.4, 0.4, 0.4, 1.0])  # Increased ambient light
        
        # Configure main light (light0)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light0_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
        # Configure secondary light (light1)
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, self.light1_pos)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])  # Brighter secondary light
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.6, 0.6, 0.6, 1.0])
        
        # Configure third light (light2)
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, self.light2_pos)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.4, 0.4, 0.4, 1.0])
        glLightfv(GL_LIGHT2, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
        
        # Set up material properties
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Increased specular
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)  # Higher shininess for sharper highlights
        
        # Enable fog for depth perception
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, [0.3, 0.3, 0.35, 1.0])  # Match background color
        glFogf(GL_FOG_START, 15.0)
        glFogf(GL_FOG_END, 25.0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Update light positions
        glLightfv(GL_LIGHT0, GL_POSITION, self.light0_pos)
        glLightfv(GL_LIGHT1, GL_POSITION, self.light1_pos)
        
        # Apply camera transformations
        glTranslatef(self.camera_pan_x, self.camera_pan_y, self.zoom)
        glRotatef(self.camera_rot_x, 1, 0, 0)
        glRotatef(self.camera_rot_y, 0, 1, 0)
        glRotatef(self.camera_rot_z, 0, 0, 1)
        
        # Draw grid
        self.draw_grid()
        
        # Draw scene objects
        self.scene_manager.draw_all()

    def draw_grid(self):
        # Draw main grid lines with higher contrast
        glColor3f(0.4, 0.4, 0.4)  # Brighter grid color
        glLineWidth(1.5)
        glBegin(GL_LINES)
        for i in range(-5, 6):
            # X-axis lines
            glVertex3f(i * 2.0, -10.0, 0)
            glVertex3f(i * 2.0, 10.0, 0)
            # Y-axis lines
            glVertex3f(-10.0, i * 2.0, 0)
            glVertex3f(10.0, i * 2.0, 0)
        glEnd()
        
        # Draw thicker center axes
        glColor3f(0.6, 0.6, 0.6)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        # X-axis
        glVertex3f(-10.0, 0.0, 0)
        glVertex3f(10.0, 0.0, 0)
        # Y-axis
        glVertex3f(0.0, -10.0, 0)
        glVertex3f(0.0, 10.0, 0)
        glEnd()

    def mousePressEvent(self, event):
        self.last_pos = event.position()
        self.setFocus()  # Set focus when clicking on GL widget
        
        # Only perform picking when not panning (not holding Option key)
        if event.button() == Qt.LeftButton and not (event.modifiers() & Qt.AltModifier):
            self.pick_object(event.position().x(), event.position().y())

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            self.last_pos = event.position()
            return
            
        dx = event.position().x() - self.last_pos.x()
        dy = event.position().y() - self.last_pos.y()
        
        modifiers = event.modifiers()
        
        if event.buttons() & Qt.LeftButton:
            if modifiers & Qt.AltModifier:
                # Pan camera when Option (Alt) key is pressed
                self.camera_pan_x += dx * 0.01
                self.camera_pan_y -= dy * 0.01
            elif modifiers & Qt.ShiftModifier and self.scene_manager.get_selected_tetrahedron():
                # Rotate selected object
                selected = self.scene_manager.get_selected_tetrahedron()
                current_rot = list(selected.get_rotation())
                current_rot[1] += dx * 0.5  # Y-axis rotation
                current_rot[0] += dy * 0.5  # X-axis rotation
                selected.set_rotation(*current_rot)
                self.scene_manager._notify_observers()
            else:
                # Rotate camera view
                self.camera_rot_y += dx * 0.5
                self.camera_rot_x += dy * 0.5
            self.update()
        elif event.buttons() & Qt.RightButton:
            if modifiers & Qt.ShiftModifier and self.scene_manager.get_selected_tetrahedron():
                # Move selected object in XY plane
                dx_world = dx * 0.01 * self.scene_manager.grid_size
                dy_world = -dy * 0.01 * self.scene_manager.grid_size
                self.scene_manager.move_selected(dx_world, dy_world, 0)
            else:
                # Zoom camera
                self.zoom += dy * 0.1
            self.update()
        elif event.buttons() & Qt.MiddleButton and modifiers & Qt.ShiftModifier:
            if self.scene_manager.get_selected_tetrahedron():
                # Move selected object in Z axis
                dz_world = -dy * 0.01 * self.scene_manager.grid_size
                self.scene_manager.move_selected(0, 0, dz_world)
                self.update()
            
        self.last_pos = event.position()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier and self.scene_manager.get_selected_tetrahedron():
            # Rotate selected object around Z axis
            selected = self.scene_manager.get_selected_tetrahedron()
            current_rot = list(selected.get_rotation())
            current_rot[2] += event.angleDelta().y() * 0.1
            selected.set_rotation(*current_rot)
            self.scene_manager._notify_observers()
        else:
            # Zoom camera
            self.zoom += event.angleDelta().y() * 0.01
        self.update()

    def keyPressEvent(self, event):
        """Handle keyboard input for tetrahedron manipulation"""
        key = event.key()
        
        # Movement keys
        if key == Qt.Key_W:
            self.scene_manager.move_selected(0, 1, 0)
        elif key == Qt.Key_S:
            self.scene_manager.move_selected(0, -1, 0)
        elif key == Qt.Key_A:
            self.scene_manager.move_selected(-1, 0, 0)
        elif key == Qt.Key_D:
            self.scene_manager.move_selected(1, 0, 0)
        elif key == Qt.Key_Q:
            self.scene_manager.move_selected(0, 0, 1)
        elif key == Qt.Key_E:
            self.scene_manager.move_selected(0, 0, -1)
            
        # Rotation keys
        elif key == Qt.Key_X:
            increment = self.parent().tools_dock.get_rotation_increment()
            self.scene_manager.rotate_selected(0, increment)
        elif key == Qt.Key_Y:
            increment = self.parent().tools_dock.get_rotation_increment()
            self.scene_manager.rotate_selected(1, increment)
        elif key == Qt.Key_Z:
            increment = self.parent().tools_dock.get_rotation_increment()
            self.scene_manager.rotate_selected(2, increment)
            
        # Add new tetrahedron
        elif key == Qt.Key_N:
            self.scene_manager.add_tetrahedron()
        
        event.accept()

    def scene_updated(self):
        """Called when the scene changes"""
        self.update()

    def get_scene_manager(self):
        return self.scene_manager
        
    def get_camera_settings(self):
        """Return the current camera settings as a dictionary"""
        return {
            'camera_rot_x': self.camera_rot_x,
            'camera_rot_y': self.camera_rot_y,
            'camera_rot_z': self.camera_rot_z,
            'camera_pan_x': self.camera_pan_x,
            'camera_pan_y': self.camera_pan_y,
            'zoom': self.zoom
        }
        
    def set_camera_settings(self, settings):
        """Set camera settings from a dictionary"""
        if not settings:
            return
            
        self.camera_rot_x = settings.get('camera_rot_x', self.camera_rot_x)
        self.camera_rot_y = settings.get('camera_rot_y', self.camera_rot_y)
        self.camera_rot_z = settings.get('camera_rot_z', self.camera_rot_z)
        self.camera_pan_x = settings.get('camera_pan_x', self.camera_pan_x)
        self.camera_pan_y = settings.get('camera_pan_y', self.camera_pan_y)
        self.zoom = settings.get('zoom', self.zoom)
        self.update()
        
    def get_lighting_settings(self):
        """Return the current lighting settings as a dictionary"""
        # Convert numpy arrays to lists for JSON serialization
        return {
            'light0_pos': self.light0_pos if isinstance(self.light0_pos, list) else self.light0_pos.tolist(),
            'light1_pos': self.light1_pos if isinstance(self.light1_pos, list) else self.light1_pos.tolist(),
            'light2_pos': self.light2_pos if isinstance(self.light2_pos, list) else self.light2_pos.tolist()
        }
        
    def set_lighting_settings(self, settings):
        """Set lighting settings from a dictionary"""
        if not settings:
            return
            
        self.light0_pos = settings.get('light0_pos', self.light0_pos)
        self.light1_pos = settings.get('light1_pos', self.light1_pos)
        self.light2_pos = settings.get('light2_pos', self.light2_pos)
        self.update()

    def pick_object(self, x, y):
        """Pick an object based on mouse click coordinates"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply camera transformations
        glTranslatef(self.camera_pan_x, self.camera_pan_y, self.zoom)
        glRotatef(self.camera_rot_x, 1, 0, 0)
        glRotatef(self.camera_rot_y, 0, 1, 0)
        glRotatef(self.camera_rot_z, 0, 0, 1)
        
        # Render each object with a unique color
        for i, tetra in enumerate(self.scene_manager.tetrahedra):
            color_id = i + 1
            color = (
                (color_id & 0xFF) / 255.0,
                ((color_id >> 8) & 0xFF) / 255.0,
                ((color_id >> 16) & 0xFF) / 255.0
            )
            glColor3f(*color)
            tetra.draw()
        
        glFlush()
        
        # Read the pixel color under the mouse cursor
        pixel = glReadPixels(x, self.height() - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        pixel = np.frombuffer(pixel, dtype=np.uint8).reshape(1, 1, 3)
        color_id = pixel[0, 0, 0] + (pixel[0, 0, 1] << 8) + (pixel[0, 0, 2] << 16)
        
        print(f"Picked color ID: {color_id}")  # Debug print
        
        # Select the object based on the color ID
        if color_id > 0 and color_id <= len(self.scene_manager.tetrahedra):
            self.scene_manager.select_tetrahedron(color_id - 1)
            print(f"Selected tetrahedron index: {color_id - 1}")  # Debug print
        else:
            print("No object selected")  # Debug print
