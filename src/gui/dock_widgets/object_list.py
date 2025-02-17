from PySide6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, 
                               QListWidget, QListWidgetItem, QMenu)
from PySide6.QtCore import Qt
from src.core.scene_manager import SceneManager

class ObjectListDock(QDockWidget):
    """A dock widget that displays a list of tetrahedra in the scene"""
    
    def __init__(self, scene_manager: SceneManager, parent=None):
        super().__init__("Object List", parent)
        self.scene_manager = scene_manager
        self.scene_manager.add_observer(self)
        
        # Create widget and layout
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        
        # Create list widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.list_widget)
        self.setWidget(self.widget)
        
        # Initialize list
        self.update_list()
    
    def update_list(self):
        """Update the list widget with current tetrahedra"""
        self.list_widget.clear()
        for i, tetra in enumerate(self.scene_manager.tetrahedra):
            item = QListWidgetItem(tetra.name)
            if tetra.selected:
                item.setSelected(True)
            self.list_widget.addItem(item)
    
    def on_item_clicked(self, item):
        """Handle selection of an item in the list"""
        index = self.list_widget.row(item)
        self.scene_manager.select_tetrahedron(index)
    
    def show_context_menu(self, pos):
        """Show context menu for list items"""
        item = self.list_widget.itemAt(pos)
        if not item:
            return
            
        index = self.list_widget.row(item)
        
        menu = QMenu()
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.list_widget.mapToGlobal(pos))
        
        if action == rename_action:
            # TODO: Implement rename functionality
            pass
        elif action == delete_action:
            self.scene_manager.remove_tetrahedron(index)
    
    def scene_updated(self):
        """Called when the scene changes"""
        self.update_list()