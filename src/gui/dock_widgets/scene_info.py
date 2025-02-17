from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class SceneInfoDock(QDockWidget):
    def __init__(self, scene_manager, parent=None):
        super().__init__("Scene Info", parent)
        self.scene_manager = scene_manager
        self.scene_manager.add_observer(self)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Create count label
        self.count_label = QLabel()
        self.main_layout.addWidget(self.count_label)
        
        # Add stretch to push everything to the top
        self.main_layout.addStretch()
        
        # Set the main widget
        self.setWidget(self.main_widget)
        
        # Update initial state
        self.update_info()
        
    def update_info(self):
        """Update the displayed information"""
        total = len(self.scene_manager.tetrahedra)
        current = self.scene_manager.selected_index + 1 if self.scene_manager.selected_index >= 0 else 0
        self.count_label.setText(f"Total Tetrahedra: {total}\nSelected: {current}/{total}")
        
    def scene_updated(self):
        """Called when the scene changes"""
        self.update_info()