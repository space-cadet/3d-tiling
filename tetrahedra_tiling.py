import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables for camera rotation
rot_x = 0.0
rot_y = 0.0
last_x = 0
last_y = 0
ROTATION_SCALE = 0.5

class Tetrahedron:
    def __init__(self, position=(0, 0, 0)):
        # Define vertices of a regular tetrahedron
        self.base_vertices = np.array([
            [1.0, 1.0, 1.0],    # Vertex 0
            [-1.0, -1.0, 1.0],  # Vertex 1
            [-1.0, 1.0, -1.0],  # Vertex 2
            [1.0, -1.0, -1.0]   # Vertex 3
        ], dtype=np.float32)
        
        # Scale the tetrahedron to make it unit size
        scale = 1.0 / np.sqrt(3)
        self.base_vertices *= scale
        
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)
        
        # Define faces (as triangles)
        self.faces = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 3, 2]
        ]
        
        # Colors for faces
        self.colors = [
            [1.0, 0.0, 0.0],  # Red
            [0.0, 1.0, 0.0],  # Green
            [0.0, 0.0, 1.0],  # Blue
            [1.0, 1.0, 0.0]   # Yellow
        ]
        
        self.selected = False

    def get_transformed_vertices(self):
        # Apply transformations to vertices
        vertices = self.base_vertices.copy()
        # Add position offset
        vertices += self.position
        return vertices

    def draw(self):
        glPushMatrix()
        
        # Apply object transformations
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw selection highlight if selected
        if self.selected:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(1.0, 1.0, 1.0)  # White outline
            self._draw_faces()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Draw filled tetrahedron
        self._draw_faces()
        
        glPopMatrix()

    def _draw_faces(self):
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(self.faces):
            if not self.selected:
                glColor3fv(self.colors[i])
            for vertex_id in face:
                glVertex3fv(self.base_vertices[vertex_id])
        glEnd()

class TetrahedraManager:
    def __init__(self):
        self.tetrahedra = []
        self.selected_index = -1
        self.grid_size = 2.0  # Size of grid for snapping

    def add_tetrahedron(self, position=(0, 0, 0)):
        self.tetrahedra.append(Tetrahedron(position))
        self.selected_index = len(self.tetrahedra) - 1
        self.update_selection()

    def draw_all(self):
        for tetra in self.tetrahedra:
            tetra.draw()

    def select_next(self):
        if not self.tetrahedra:
            return
        self.selected_index = (self.selected_index + 1) % len(self.tetrahedra)
        self.update_selection()

    def select_previous(self):
        if not self.tetrahedra:
            return
        self.selected_index = (self.selected_index - 1) % len(self.tetrahedra)
        self.update_selection()

    def update_selection(self):
        for i, tetra in enumerate(self.tetrahedra):
            tetra.selected = (i == self.selected_index)

    def move_selected(self, dx, dy, dz):
        if self.selected_index >= 0:
            tetra = self.tetrahedra[self.selected_index]
            tetra.position += np.array([dx, dy, dz]) * self.grid_size

    def rotate_selected(self, axis, angle):
        if self.selected_index >= 0:
            tetra = self.tetrahedra[self.selected_index]
            tetra.rotation[axis] += angle

def render_text(x, y, text):
    glDisable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    glOrtho(0, w, 0, h, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1, 1, 1)  # White text
    glRasterPos2i(x, h - y)  # Adjust y coordinate
    for char in str(text):
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_DEPTH_TEST)

def draw_info_overlay():
    # Get info about current state
    total_tetras = len(manager.tetrahedra)
    current_tetra = manager.selected_index + 1 if manager.selected_index >= 0 else 0
    
    # Basic info
    render_text(10, 20, f"Tetrahedra: {current_tetra}/{total_tetras}")
    
    # Selected tetrahedron info
    if manager.selected_index >= 0:
        tetra = manager.tetrahedra[manager.selected_index]
        pos = tetra.position
        rot = tetra.rotation
        render_text(10, 40, f"Position: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})")
        render_text(10, 60, f"Rotation: ({rot[0]:.1f}, {rot[1]:.1f}, {rot[2]:.1f})")
    
    # Controls help
    render_text(10, glutGet(GLUT_WINDOW_HEIGHT) - 20, "N: New  Tab: Next  `: Previous  WASD/QE: Move  XYZ: Rotate")

def draw():
    global rot_x, rot_y
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Position the camera
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
    
    # Apply camera rotations
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    
    # Draw grid (optional)
    draw_grid()
    
    # Draw all tetrahedra
    manager.draw_all()
    
    # Draw UI overlay
    draw_info_overlay()
    
    glutSwapBuffers()

def draw_grid():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(i * 2.0, -10.0, 0)
        glVertex3f(i * 2.0, 10.0, 0)
        glVertex3f(-10.0, i * 2.0, 0)
        glVertex3f(10.0, i * 2.0, 0)
    glEnd()

def mouse_motion(x, y):
    global rot_x, rot_y, last_x, last_y
    
    dx = x - last_x
    dy = y - last_y
    
    rot_y += dx * ROTATION_SCALE
    rot_x += dy * ROTATION_SCALE
    
    last_x = x
    last_y = y
    
    glutPostRedisplay()

def mouse(button, state, x, y):
    global last_x, last_y
    
    last_x = x
    last_y = y

def keyboard(key, x, y):
    if key == b'n':  # Add new tetrahedron
        manager.add_tetrahedron()
    elif key == b'tab':  # Select next tetrahedron
        manager.select_next()
    elif key == b'`':  # Select previous tetrahedron
        manager.select_previous()
    
    # Movement controls for selected tetrahedron
    elif key == b'w':
        manager.move_selected(0, 1, 0)
    elif key == b's':
        manager.move_selected(0, -1, 0)
    elif key == b'a':
        manager.move_selected(-1, 0, 0)
    elif key == b'd':
        manager.move_selected(1, 0, 0)
    elif key == b'q':
        manager.move_selected(0, 0, 1)
    elif key == b'e':
        manager.move_selected(0, 0, -1)
    
    # Rotation controls for selected tetrahedron
    elif key == b'x':
        manager.rotate_selected(0, 90)
    elif key == b'y':
        manager.rotate_selected(1, 90)
    elif key == b'z':
        manager.rotate_selected(2, 90)
    
    glutPostRedisplay()

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Initialize GLUT and create window
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Tetrahedra Tiling")

# Create tetrahedra manager
manager = TetrahedraManager()
manager.add_tetrahedron()  # Add initial tetrahedron

# Register callbacks
glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutMotionFunc(mouse_motion)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)

# Initialize OpenGL settings
init()

print("""
Tetrahedra Tiling Controls:
--------------------------
Mouse drag: Rotate camera view
n: Add new tetrahedron
tab: Select next tetrahedron
`: Select previous tetrahedron

Movement (selected tetrahedron):
w/s: Move up/down
a/d: Move left/right
q/e: Move forward/backward

Rotation (selected tetrahedron):
x: Rotate around X axis
y: Rotate around Y axis
z: Rotate around Z axis
""")

# Start the main loop
glutMainLoop()