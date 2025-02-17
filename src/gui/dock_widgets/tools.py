from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel, QGroupBox
from PySide6.QtCore import Qt

class ToolsDock(QDockWidget):
    def __init__(self, scene_manager, parent=None):
        super().__init__("Tools", parent)
        self.scene_manager = scene_manager
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Create Tools
        self.create_tetrahedron_tools()
        self.create_rotation_settings()
        
        # Add stretch to push everything to the top
        self.main_layout.addStretch()
        
        # Set the main widget
        self.setWidget(self.main_widget)
        
    def create_tetrahedron_tools(self):
        # Tetrahedron Operations Group
        operations_group = QGroupBox("Tetrahedron Operations")
        operations_layout = QVBoxLayout()
        
        # Create New Button
        new_button = QPushButton("New Tetrahedron")
        new_button.clicked.connect(lambda: self.scene_manager.add_tetrahedron())
        operations_layout.addWidget(new_button)
        
        # Delete Button
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected)
        operations_layout.addWidget(delete_button)
        
        operations_group.setLayout(operations_layout)
        self.main_layout.addWidget(operations_group)
        
    def create_rotation_settings(self):
        # Rotation Settings Group
        settings_group = QGroupBox("Rotation Settings")
        settings_layout = QVBoxLayout()
        
        # Rotation Increment
        increment_label = QLabel("Rotation Increment:")
        self.rotation_increment = QSpinBox()
        self.rotation_increment.setRange(1, 90)
        self.rotation_increment.setValue(90)  # Default value
        self.rotation_increment.setSingleStep(1)
        self.rotation_increment.setSuffix("°")
        
        settings_layout.addWidget(increment_label)
        settings_layout.addWidget(self.rotation_increment)
        
        settings_group.setLayout(settings_layout)
        self.main_layout.addWidget(settings_group)
        
    def delete_selected(self):
        """Delete the currently selected tetrahedron"""
        if self.scene_manager.selected_index >= 0:
            self.scene_manager.remove_tetrahedron(self.scene_manager.selected_index)
            
    def get_rotation_increment(self):
        """Get the current rotation increment value"""
        return self.rotation_increment.value()