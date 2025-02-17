import json
import os
from typing import List, Dict, Any

class FileManager:
    """Handles saving and loading of scene data"""
    
    @staticmethod
    def save_scene(filepath: str, scene_data: Dict[str, Any]) -> bool:
        """
        Save scene data to a JSON file
        
        Args:
            filepath: Path to save the file
            scene_data: Dictionary containing scene data
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Ensure the file has .json extension
            if not filepath.endswith('.json'):
                filepath += '.json'
                
            with open(filepath, 'w') as f:
                json.dump(scene_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving scene: {e}")
            return False
    
    @staticmethod
    def load_scene(filepath: str) -> Dict[str, Any]:
        """
        Load scene data from a JSON file
        
        Args:
            filepath: Path to the file to load
            
        Returns:
            dict: Dictionary containing scene data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file is not valid JSON
        """
        with open(filepath, 'r') as f:
            return json.load(f)