from PySide6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QLabel,
                               QGridLayout, QDoubleSpinBox, QGroupBox)
from PySide6.QtCore import Qt

class PropertiesDock(QDockWidget):
    def __init__(self, scene_manager, parent=None):
        super().__init__("Properties", parent)
        self.scene_manager = scene_manager
        self.scene_manager.add_observer(self)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Position controls
        self.position_group = QGroupBox("Position")
        position_layout = QGridLayout()
        
        self.pos_spinboxes = []
        for i, axis in enumerate(['X', 'Y', 'Z']):
            label = QLabel(axis)
            spinbox = QDoubleSpinBox()
            spinbox.setRange(-100, 100)
            spinbox.setSingleStep(0.1)
            spinbox.setDecimals(2)
            spinbox.valueChanged.connect(
                lambda v, i=i: self.position_changed(i, v))
            position_layout.addWidget(label, 0, i)
            position_layout.addWidget(spinbox, 1, i)
            self.pos_spinboxes.append(spinbox)
            
        self.position_group.setLayout(position_layout)
        
        # Rotation controls
        self.rotation_group = QGroupBox("Rotation")
        rotation_layout = QGridLayout()
        
        self.rot_spinboxes = []
        for i, axis in enumerate(['X', 'Y', 'Z']):
            label = QLabel(axis)
            spinbox = QDoubleSpinBox()
            spinbox.setRange(-360, 360)
            spinbox.setSingleStep(90)
            spinbox.valueChanged.connect(
                lambda v, i=i: self.rotation_changed(i, v))
            rotation_layout.addWidget(label, 0, i)
            rotation_layout.addWidget(spinbox, 1, i)
            self.rot_spinboxes.append(spinbox)
            
        self.rotation_group.setLayout(rotation_layout)
        
        # Add groups to main layout
        self.main_layout.addWidget(self.position_group)
        self.main_layout.addWidget(self.rotation_group)
        self.main_layout.addStretch()
        
        # Set the main widget
        self.setWidget(self.main_widget)
        
        # Update initial state
        self.update_values()
        
    def position_changed(self, axis, value):
        """Handle position spinbox changes"""
        if selected := self.scene_manager.get_selected_tetrahedron():
            pos = list(selected.get_position())
            pos[axis] = value
            selected.set_position(*pos)
            self.scene_manager._notify_observers()
            
    def rotation_changed(self, axis, value):
        """Handle rotation spinbox changes"""
        if selected := self.scene_manager.get_selected_tetrahedron():
            rot = list(selected.get_rotation())
            rot[axis] = value
            selected.set_rotation(*rot)
            self.scene_manager._notify_observers()
            
    def update_values(self):
        """Update spinbox values from selected tetrahedron"""
        selected = self.scene_manager.get_selected_tetrahedron()
        
        # Enable/disable controls based on selection
        enabled = selected is not None
        self.position_group.setEnabled(enabled)
        self.rotation_group.setEnabled(enabled)
        
        if selected:
            # Update position values
            pos = selected.get_position()
            for i, spinbox in enumerate(self.pos_spinboxes):
                spinbox.blockSignals(True)
                spinbox.setValue(pos[i])
                spinbox.blockSignals(False)
                
            # Update rotation values
            rot = selected.get_rotation()
            for i, spinbox in enumerate(self.rot_spinboxes):
                spinbox.blockSignals(True)
                spinbox.setValue(rot[i])
                spinbox.blockSignals(False)
                
    def scene_updated(self):
        """Called when the scene changes"""
        self.update_values()