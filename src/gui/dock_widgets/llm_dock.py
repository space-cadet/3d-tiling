from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Qt

class LLMDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("LLM Interaction", parent)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Create message input area
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your message here...")
        self.main_layout.addWidget(self.message_input)
        
        # Create send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.main_layout.addWidget(self.send_button)
        
        # Create response display area
        self.response_display = QLabel()
        self.response_display.setWordWrap(True)
        self.main_layout.addWidget(self.response_display)
        
        # Set the main widget
        self.setWidget(self.main_widget)
        
    def send_message(self):
        """Send the message to the LLM and display the response"""
        message = self.message_input.toPlainText()
        if message:
            response = self.get_llm_response(message)
            self.response_display.setText(response)
    
    def get_llm_response(self, message):
        """Mock function to get LLM response. Replace with actual LLM API call."""
        # TODO: Implement actual LLM API call here
        return f"Response to: {message}"