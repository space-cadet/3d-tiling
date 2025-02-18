import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QMessageBox
from src.gui.main_window import MainWindow

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    app = QApplication(sys.argv)
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error("An error occurred during application startup", exc_info=True)
        QMessageBox.critical(None, "Critical Error", f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()