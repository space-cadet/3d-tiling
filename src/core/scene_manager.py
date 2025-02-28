from typing import List, Optional
import json
from .tetrahedron import Tetrahedron
from .history import History

class SceneManager:
    def __init__(self):
        self.tetrahedra: List[Tetrahedron] = []
        self.selected_index: int = -1
        self.grid_size: float = 2.0
        self._observers = []
        self.history = History()

    def add_observer(self, observer):
        """Add an observer that will be notified of scene changes"""
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer"""
        self._observers.remove(observer)

    def _notify_observers(self):
        """Notify all observers of a scene change"""
        for observer in self._observers:
            observer.scene_updated()

    def add_tetrahedron(self, position=(0, 0, 0)) -> Tetrahedron:
        """Add a new tetrahedron to the scene"""
        from .history import AddTetrahedronCommand
        command = AddTetrahedronCommand(self, position)
        command.execute()
        self.history.push(command)
        return self.tetrahedra[-1]

    def remove_tetrahedron(self, index: int):
        """Remove a tetrahedron from the scene"""
        if 0 <= index < len(self.tetrahedra):
            self.tetrahedra.pop(index)
            if self.selected_index >= len(self.tetrahedra):
                self.selected_index = len(self.tetrahedra) - 1
            self.update_selection()
            self._notify_observers()

    def get_selected_tetrahedron(self) -> Optional[Tetrahedron]:
        """Get the currently selected tetrahedron"""
        if 0 <= self.selected_index < len(self.tetrahedra):
            return self.tetrahedra[self.selected_index]
        return None

    def select_tetrahedron(self, index: int):
        """Select a specific tetrahedron"""
        if 0 <= index < len(self.tetrahedra):
            self.selected_index = index
            self.update_selection()
            self._notify_observers()

    def select_next(self):
        """Select the next tetrahedron in the list"""
        if self.tetrahedra:
            self.selected_index = (self.selected_index + 1) % len(self.tetrahedra)
            self.update_selection()
            self._notify_observers()

    def select_previous(self):
        """Select the previous tetrahedron in the list"""
        if self.tetrahedra:
            self.selected_index = (self.selected_index - 1) % len(self.tetrahedra)
            self.update_selection()
            self._notify_observers()

    def update_selection(self):
        """Update the selection state of all tetrahedra"""
        for i, tetra in enumerate(self.tetrahedra):
            tetra.selected = (i == self.selected_index)

    def move_selected(self, dx: float, dy: float, dz: float):
        """Move the selected tetrahedron"""
        from .history import MoveTetrahedronCommand
        command = MoveTetrahedronCommand(self, dx, dy, dz)
        command.execute()
        self.history.push(command)

    def rotate_selected(self, axis: int, angle: float):
        """Rotate the selected tetrahedron"""
        from .history import RotateTetrahedronCommand
        command = RotateTetrahedronCommand(self, axis, angle)
        command.execute()
        self.history.push(command)

    def draw_all(self):
        """Draw all tetrahedra in the scene"""
        for tetra in self.tetrahedra:
            tetra.draw()

    def save_scene(self, filename: str, camera_settings=None, lighting_settings=None):
        """Save the scene to a file"""
        data = {
            'tetrahedra': [t.to_dict() for t in self.tetrahedra],
            'selected_index': self.selected_index,
            'grid_size': self.grid_size
        }
        
        # Add camera and lighting settings if provided
        if camera_settings:
            data['camera_settings'] = camera_settings
        if lighting_settings:
            data['lighting_settings'] = lighting_settings
            
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_scene(self, filename: str):
        """Load the scene from a file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.tetrahedra = [Tetrahedron.from_dict(t) for t in data['tetrahedra']]
        self.selected_index = data['selected_index']
        self.grid_size = data['grid_size']
        self.update_selection()
        self._notify_observers()
        
        # Return camera and lighting settings if they exist in the file
        camera_settings = data.get('camera_settings')
        lighting_settings = data.get('lighting_settings')
        
        return camera_settings, lighting_settings
