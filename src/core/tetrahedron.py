import numpy as np
from OpenGL.GL import *

class Tetrahedron:
    def __init__(self, position=(0, 0, 0), name="Tetrahedron"):
        self.name = name
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

    def set_position(self, x, y, z):
        self.position = np.array([x, y, z], dtype=np.float32)

    def set_rotation(self, x, y, z):
        self.rotation = np.array([x, y, z], dtype=np.float32)

    def get_position(self):
        return tuple(self.position)

    def get_rotation(self):
        return tuple(self.rotation)

    def to_dict(self):
        """Convert tetrahedron data to dictionary for serialization"""
        # Convert numpy arrays to lists for JSON serialization
        return {
            'name': self.name,
            'position': [float(x) for x in self.position],  # Convert numpy array to list of floats
            'rotation': [float(x) for x in self.rotation],  # Convert numpy array to list of floats
            'selected': self.selected
        }

    @classmethod
    def from_dict(cls, data):
        """Create tetrahedron from dictionary data"""
        tetra = cls(position=data['position'], name=data['name'])
        tetra.set_rotation(*data['rotation'])  # Unpack the rotation list
        tetra.selected = data['selected']
        return tetra