import pandas as pd

class DataLoader:
    def __init__(self):
        self.data = None
        self.file_path = None
    
    def load_csv(self, file_path):
        """Load data from a CSV file"""
        try:
            self.file_path = file_path
            self.data = pd.read_csv(file_path)
            print(f"Successfully loaded CSV: {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def load_excel(self, file_path, sheet_name=0):
        """Load data from an Excel file"""
        try:
            self.file_path = file_path
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Successfully loaded Excel: {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading Excel: {e}")
            return None
    
    def load_json(self, file_path):
        """Load data from a JSON file"""
        try:
            self.file_path = file_path
            self.data = pd.read_json(file_path)
            print(f"Successfully loaded JSON: {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None