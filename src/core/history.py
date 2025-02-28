from typing import List, Optional

class Command:
    """Base class for undoable commands"""
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")
        
    def undo(self):
        raise NotImplementedError("Subclasses must implement undo()")

class History:
    """Manages undo/redo history stack"""
    def __init__(self):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        
    def push(self, command: Command):
        """Record a new command"""
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        """Undo last command"""
        if self._undo_stack:
            command = self._undo_stack.pop()
            command.undo()
            self._redo_stack.append(command)

    def redo(self):
        """Redo last undone command"""
        if self._redo_stack:
            command = self._redo_stack.pop()
            command.execute()
            self._undo_stack.append(command)

    def clear(self):
        """Reset history"""
        self._undo_stack.clear()
        self._redo_stack.clear()

class AddTetrahedronCommand(Command):
    """Command for adding a tetrahedron"""
    def __init__(self, scene_manager, position):
        self.scene_manager = scene_manager
        self.position = position
        self.added_tetra = None
        self.added_index = -1

    def execute(self):
        name = f"Tetrahedron_{len(self.scene_manager.tetrahedra) + 1}"
        self.added_tetra = Tetrahedron(self.position, name)
        self.scene_manager.tetrahedra.append(self.added_tetra)
        self.added_index = len(self.scene_manager.tetrahedra) - 1
        self.scene_manager.selected_index = self.added_index
        self.scene_manager.update_selection()
        self.scene_manager._notify_observers()

    def undo(self):
        if self.added_index != -1:
            self.scene_manager.tetrahedra.pop(self.added_index)
            if self.scene_manager.selected_index >= len(self.scene_manager.tetrahedra):
                self.scene_manager.selected_index = len(self.scene_manager.tetrahedra) - 1
            self.scene_manager.update_selection()
            self.scene_manager._notify_observers()

class MoveTetrahedronCommand(Command):
    """Command for moving a tetrahedron"""
    def __init__(self, scene_manager, dx, dy, dz):
        self.scene_manager = scene_manager
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.old_position = None
        self.tetra = None

    def execute(self):
        if tetra := self.scene_manager.get_selected_tetrahedron():
            self.tetra = tetra
            self.old_position = tetra.get_position()
            pos = self.old_position
            tetra.set_position(
                pos[0] + self.dx * self.scene_manager.grid_size,
                pos[1] + self.dy * self.scene_manager.grid_size,
                pos[2] + self.dz * self.scene_manager.grid_size
            )
            self.scene_manager._notify_observers()

    def undo(self):
        if self.tetra and self.old_position:
            self.tetra.set_position(*self.old_position)
            self.scene_manager._notify_observers()

class RotateTetrahedronCommand(Command):
    """Command for rotating a tetrahedron"""
    def __init__(self, scene_manager, axis, angle):
        self.scene_manager = scene_manager
        self.axis = axis
        self.angle = angle
        self.old_rotation = None
        self.tetra = None

    def execute(self):
        if tetra := self.scene_manager.get_selected_tetrahedron():
            self.tetra = tetra
            self.old_rotation = tetra.get_rotation()
            rot = list(self.old_rotation)
            rot[self.axis] = (rot[self.axis] + self.angle) % 360
            tetra.set_rotation(*rot)
            self.scene_manager._notify_observers()

    def undo(self):
        if self.tetra and self.old_rotation:
            self.tetra.set_rotation(*self.old_rotation)
            self.scene_manager._notify_observers()
