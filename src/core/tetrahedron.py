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
        
        # Define faces (as triangles)
        self.faces = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 3, 2]
        ]
        
        # Calculate face normals
        self.face_normals = self._calculate_face_normals()
        
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array([0, 0, 0], dtype=np.float32)
        
        # Define faces (as triangles)
        self.faces = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 3, 2]
        ]
        
        # Colors for faces (slightly desaturated for better lighting)
        self.colors = [
            [0.8, 0.2, 0.2],  # Softer red
            [0.2, 0.8, 0.2],  # Softer green
            [0.2, 0.2, 0.8],  # Softer blue
            [0.8, 0.8, 0.2]   # Softer yellow
        ]
        
        self.selected = False

    def get_transformed_vertices(self):
        # Apply transformations to vertices
        vertices = self.base_vertices.copy()
        # Add position offset
        vertices += self.position
        return vertices

    def draw(self, color=None):
        glPushMatrix()
        
        # Apply object transformations
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw selection highlight if selected
        if self.selected and color is None:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(1.0, 1.0, 1.0)  # White outline
            self._draw_faces()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Draw filled tetrahedron
        self._draw_faces(color)
        
        glPopMatrix()

    def _calculate_face_normals(self):
        """Calculate face normals using cross product of face edges"""
        normals = []
        for face in self.faces:
            # Get three vertices of the face
            v0 = self.base_vertices[face[0]]
            v1 = self.base_vertices[face[1]]
            v2 = self.base_vertices[face[2]]
            
            # Calculate two edge vectors
            edge1 = v1 - v0
            edge2 = v2 - v0
            
            # Calculate cross product and normalize
            normal = np.cross(edge1, edge2)
            normal /= np.linalg.norm(normal)
            normals.append(normal)
            
        return normals

    def _draw_faces(self, color=None):
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(self.faces):
            # Always use face normal for proper lighting
            glNormal3fv(self.face_normals[i])
            
            if color is None:
                # Set material properties to match face color
                face_color = self.colors[i]
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [c * 0.2 for c in face_color] + [1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, face_color + [1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
                glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)
                glColor3fv(face_color)
            else:
                # For selection highlight or picking, use flat color without lighting effects
                glColor3fv(color)
                
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
