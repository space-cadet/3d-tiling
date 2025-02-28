from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel, QGroupBox, QDoubleSpinBox
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
        self.create_lighting_settings()
        
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
        self.rotation_increment.setValue(15)  # Default value
        self.rotation_increment.setSingleStep(1)
        self.rotation_increment.setSuffix("°")
        self.rotation_increment.setToolTip("Rotation increment angle (degrees)")
        
        settings_layout.addWidget(increment_label)
        settings_layout.addWidget(self.rotation_increment)
        
        settings_group.setLayout(settings_layout)
        self.main_layout.addWidget(settings_group)
        
    def create_lighting_settings(self):
        """Create lighting position controls"""
        lighting_group = QGroupBox("Lighting Position")
        lighting_layout = QVBoxLayout()
        
        # X Position
        x_label = QLabel("X:")
        self.light_x = QDoubleSpinBox()
        self.light_x.setRange(-10.0, 10.0)
        self.light_x.setValue(4.0)
        self.light_x.setSingleStep(0.5)
        self.light_x.valueChanged.connect(self.update_light_position)
        lighting_layout.addWidget(x_label)
        lighting_layout.addWidget(self.light_x)
        
        # Y Position
        y_label = QLabel("Y:")
        self.light_y = QDoubleSpinBox()
        self.light_y.setRange(-10.0, 10.0)
        self.light_y.setValue(4.0)
        self.light_y.setSingleStep(0.5)
        self.light_y.valueChanged.connect(self.update_light_position)
        lighting_layout.addWidget(y_label)
        lighting_layout.addWidget(self.light_y)
        
        # Z Position
        z_label = QLabel("Z:")
        self.light_z = QDoubleSpinBox()
        self.light_z.setRange(-10.0, 10.0)
        self.light_z.setValue(4.0)
        self.light_z.setSingleStep(0.5)
        self.light_z.valueChanged.connect(self.update_light_position)
        lighting_layout.addWidget(z_label)
        lighting_layout.addWidget(self.light_z)
        
        lighting_group.setLayout(lighting_layout)
        self.main_layout.addWidget(lighting_group)

    def delete_selected(self):
        """Delete the currently selected tetrahedron"""
        if self.scene_manager.selected_index >= 0:
            self.scene_manager.remove_tetrahedron(self.scene_manager.selected_index)
            
    def get_rotation_increment(self):
        """Get the current rotation increment value"""
        return self.rotation_increment.value()
        
    def update_light_position(self):
        """Update light position when controls change"""
        if hasattr(self.parent(), 'gl_widget'):
            self.parent().gl_widget.light_pos = [
                self.light_x.value(),
                self.light_y.value(),
                self.light_z.value(),
                1.0
            ]
            self.parent().gl_widget.update()
