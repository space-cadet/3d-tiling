from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QDockWidget, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QKeySequence
import os

from src.core.scene_manager import SceneManager
from src.core.file_manager import FileManager
from src.gui.gl_widget import GLWidget
from src.gui.dock_widgets.properties import PropertiesDock
from src.gui.dock_widgets.scene_info import SceneInfoDock
from src.gui.dock_widgets.tools import ToolsDock
from src.gui.dock_widgets.object_list import ObjectListDock
from src.gui.dock_widgets.llm_dock import LLMDock  # Import the new LLM dock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetrahedra Tiling")
        
        # Create scene manager
        self.scene_manager = SceneManager()
        
        # Load last session if exists
        self.last_session_path = "scenes/last_session.json"
        self.loaded_session = False
        
        if os.path.exists(self.last_session_path):
            try:
                camera_settings, lighting_settings = self.scene_manager.load_scene(self.last_session_path)
                self.loaded_session = True
                
                # Create OpenGL widget first so we can apply settings to it
                self.gl_widget = GLWidget(self.scene_manager, self)
                
                # Apply camera and lighting settings if they exist
                if camera_settings:
                    self.gl_widget.set_camera_settings(camera_settings)
                if lighting_settings:
                    self.gl_widget.set_lighting_settings(lighting_settings)
                    
            except Exception as e:
                QMessageBox.warning(self, "Warning", 
                    f"Failed to load last session: {str(e)}")
                # Create OpenGL widget if loading failed
                self.gl_widget = GLWidget(self.scene_manager, self)
                self.loaded_session = False
        else:
            # Create OpenGL widget if no last session exists
            self.gl_widget = GLWidget(self.scene_manager, self)
            self.loaded_session = False
        
        # Set the OpenGL widget as the central widget
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
        
        # Add initial tetrahedron only if we didn't load a session
        if not self.loaded_session:
            self.scene_manager.add_tetrahedron()

    def setup_docks(self):
        # Scene Info Dock
        self.scene_info_dock = SceneInfoDock(self.scene_manager, self)
        self.scene_info_dock.setObjectName("SceneInfoDock")
        
        # Properties Dock
        self.properties_dock = PropertiesDock(self.scene_manager, self)
        self.properties_dock.setObjectName("PropertiesDock")
        
        # Tools Dock
        self.tools_dock = ToolsDock(self.scene_manager, self)
        self.tools_dock.setObjectName("ToolsDock")
        
        # Object List Dock
        self.object_list_dock = ObjectListDock(self.scene_manager, self)
        self.object_list_dock.setObjectName("ObjectListDock")
        
        # LLM Dock
        self.llm_dock = LLMDock(self)
        self.llm_dock.setObjectName("LLMDock")
        
        # Set dock features
        for dock in [self.scene_info_dock, self.properties_dock, 
                    self.tools_dock, self.object_list_dock, self.llm_dock]:
            dock.setFeatures(QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetMovable |
                           QDockWidget.DockWidgetClosable)
        
        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.scene_info_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.properties_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tools_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.object_list_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.llm_dock)  # Add the LLM dock

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        # New Scene
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_scene)
        file_menu.addAction(new_action)
        
        # Open Scene
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_scene)
        file_menu.addAction(open_action)
        
        # Save Scene
        save_action = QAction("Save...", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_scene)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Edit submenu
        edit_menu = file_menu.addMenu("Edit")
        
        # Undo
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.scene_manager.history.undo)
        edit_menu.addAction(undo_action)
        
        # Redo
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.scene_manager.history.redo)
        edit_menu.addAction(redo_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.scene_info_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.tools_dock.toggleViewAction())
        view_menu.addAction(self.object_list_dock.toggleViewAction())
        view_menu.addAction(self.llm_dock.toggleViewAction())  # Add the LLM dock toggle

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

        # Undo
        undo_shortcut = QAction("Undo", self)
        undo_shortcut.setShortcut(QKeySequence.Undo)
        undo_shortcut.triggered.connect(self.scene_manager.history.undo)
        self.addAction(undo_shortcut)
        
        # Redo
        redo_shortcut = QAction("Redo", self)
        redo_shortcut.setShortcut(QKeySequence.Redo)
        redo_shortcut.triggered.connect(self.scene_manager.history.redo)
        self.addAction(redo_shortcut)

    def new_scene(self):
        """Create a new scene"""
        self.scene_manager.tetrahedra.clear()
        self.scene_manager.selected_index = -1
        self.scene_manager.add_tetrahedron()
        self.scene_manager._notify_observers()

    def open_scene(self):
        """Open a scene from file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Scene",
            "",
            "Scene Files (*.json);;All Files (*)"
        )
        
        if filepath:
            try:
                data = FileManager.load_scene(filepath)
                
                # Load tetrahedra data
                self.scene_manager.tetrahedra.clear()
                for tetra_data in data['tetrahedra']:
                    tetra = self.scene_manager.add_tetrahedron()
                    tetra.set_position(*tetra_data['position'])
                    tetra.set_rotation(*tetra_data['rotation'])
                    tetra.name = tetra_data['name']
                self.scene_manager.selected_index = data.get('selected_index', -1)
                self.scene_manager.grid_size = data.get('grid_size', 2.0)
                self.scene_manager.update_selection()
                
                # Load camera and lighting settings if they exist
                camera_settings = data.get('camera_settings')
                lighting_settings = data.get('lighting_settings')
                
                if camera_settings:
                    self.gl_widget.set_camera_settings(camera_settings)
                if lighting_settings:
                    self.gl_widget.set_lighting_settings(lighting_settings)
                
                self.scene_manager._notify_observers()
                
                QMessageBox.information(self, "Success", "Scene loaded successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load scene: {str(e)}")

    def save_scene(self):
        """Save the scene to file"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Scene",
            "",
            "Scene Files (*.json);;All Files (*)"
        )
        
        if filepath:
            try:
                # Get camera and lighting settings
                camera_settings = self.gl_widget.get_camera_settings()
                lighting_settings = self.gl_widget.get_lighting_settings()
                
                # Create scene data with all settings
                scene_data = {
                    'tetrahedra': [t.to_dict() for t in self.scene_manager.tetrahedra],
                    'selected_index': self.scene_manager.selected_index,
                    'grid_size': self.scene_manager.grid_size,
                    'camera_settings': camera_settings,
                    'lighting_settings': lighting_settings
                }
                
                if FileManager.save_scene(filepath, scene_data):
                    QMessageBox.information(self, "Success", "Scene saved successfully")
                else:
                    QMessageBox.warning(self, "Warning", "Scene may not have been saved correctly")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save scene: {str(e)}")

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
        # Save current scene before closing
        try:
            os.makedirs("scenes", exist_ok=True)
            
            # Get camera and lighting settings from the GL widget
            camera_settings = self.gl_widget.get_camera_settings()
            lighting_settings = self.gl_widget.get_lighting_settings()
            
            # Save scene with camera and lighting settings
            self.scene_manager.save_scene(
                self.last_session_path,
                camera_settings=camera_settings,
                lighting_settings=lighting_settings
            )
        except Exception as e:
            QMessageBox.warning(self, "Warning", 
                f"Failed to save session: {str(e)}")
        
        self.save_layout()
        super().closeEvent(event)
