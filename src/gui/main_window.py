from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QDockWidget)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QKeySequence

from src.core.scene_manager import SceneManager
from src.gui.gl_widget import GLWidget
from src.gui.dock_widgets.properties import PropertiesDock
from src.gui.dock_widgets.scene_info import SceneInfoDock
from src.gui.dock_widgets.tools import ToolsDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetrahedra Tiling")
        
        # Create scene manager
        self.scene_manager = SceneManager()
        
        # Create OpenGL widget
        self.gl_widget = GLWidget(self.scene_manager, self)
        self.setCentralWidget(self.gl_widget)
        
        # Create dock widgets
        self.setup_docks()
        
        # Create menu bar
        self.setup_menu()
        
        # Create shortcuts
        self.setup_shortcuts()
        
        # Restore previous layout if exists
        self.restore_layout()
        
        # Set initial window size
        self.resize(1200, 800)
        
        # Add initial tetrahedron
        self.scene_manager.add_tetrahedron()

    def setup_docks(self):
        # Scene Info Dock
        self.scene_info_dock = SceneInfoDock(self.scene_manager, self)
        
        # Properties Dock
        self.properties_dock = PropertiesDock(self.scene_manager, self)
        
        # Tools Dock
        self.tools_dock = ToolsDock(self.scene_manager, self)
        
        # Set dock features
        for dock in [self.scene_info_dock, self.properties_dock, self.tools_dock]:
            dock.setFeatures(QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetMovable |
                           QDockWidget.DockWidgetClosable)
        
        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.scene_info_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.properties_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tools_dock)

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_scene)
        file_menu.addAction(new_action)
        
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.scene_info_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.tools_dock.toggleViewAction())

    def setup_shortcuts(self):
        # Next tetrahedron
        next_shortcut = QAction("Next Tetrahedron", self)
        next_shortcut.setShortcut(QKeySequence(Qt.Key_Tab))
        next_shortcut.triggered.connect(self.scene_manager.select_next)
        self.addAction(next_shortcut)
        
        # Previous tetrahedron
        prev_shortcut = QAction("Previous Tetrahedron", self)
        prev_shortcut.setShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Tab))
        prev_shortcut.triggered.connect(self.scene_manager.select_previous)
        self.addAction(prev_shortcut)

    def new_scene(self):
        """Create a new scene"""
        self.scene_manager.tetrahedra.clear()
        self.scene_manager.selected_index = -1
        self.scene_manager.add_tetrahedron()
        self.scene_manager._notify_observers()

    def save_layout(self):
        settings = QSettings('Block', 'TetrahedraTiling')
        settings.setValue('windowGeometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        
    def restore_layout(self):
        settings = QSettings('Block', 'TetrahedraTiling')
        if settings.value('windowGeometry'):
            self.restoreGeometry(settings.value('windowGeometry'))
        if settings.value('windowState'):
            self.restoreState(settings.value('windowState'))
            
    def closeEvent(self, event):
        self.save_layout()
        super().closeEvent(event)