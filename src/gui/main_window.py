from PySide6.QtWidgets import QMainWindow, QDockWidget, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QSettings

from src.core.scene_manager import SceneManager
from src.gui.gl_widget import GLWidget
from src.gui.dock_widgets.properties import PropertiesDock

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetrahedra Tiling")
        
        # Create scene manager
        self.scene_manager = SceneManager()
        
        # Create OpenGL widget
        self.gl_widget = GLWidget(self.scene_manager)
        self.setCentralWidget(self.gl_widget)
        
        # Create dock widgets
        self.setup_docks()
        
        # Create menu bar
        self.setup_menu()
        
        # Restore previous layout if exists
        self.restore_layout()
        
        # Set initial window size
        self.resize(1200, 800)
        
        # Add initial tetrahedron
        self.scene_manager.add_tetrahedron()

    def setup_docks(self):
        # Scene Info Dock
        self.scene_info_dock = QDockWidget("Scene Info", self)
        scene_info_widget = QWidget()
        scene_info_layout = QVBoxLayout()
        scene_info_layout.addWidget(QLabel("Total Tetrahedra: 0"))
        scene_info_widget.setLayout(scene_info_layout)
        self.scene_info_dock.setWidget(scene_info_widget)
        
        # Properties Dock
        self.properties_dock = PropertiesDock(self.scene_manager, self)
        
        # Set dock features
        for dock in [self.scene_info_dock, self.properties_dock]:
            dock.setFeatures(QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetMovable |
                           QDockWidget.DockWidgetClosable)
        
        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.scene_info_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.properties_dock)

    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.scene_info_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())

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