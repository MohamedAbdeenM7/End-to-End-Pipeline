import pandas as pd

class DataCleaner:
    def __init__(self, data):
        self.data = data
        self.original_shape = data.shape if data is not None else None
    
    def remove_nulls(self, columns=None):
        """Remove rows with null values"""
        if columns:
            self.data = self.data.dropna(subset=columns)
        else:
            self.data = self.data.dropna()
        return self.data
    
    def fill_nulls(self, value=0, columns=None):
        """Fill null values with specified value"""
        if columns:
            self.data[columns] = self.data[columns].fillna(value)
        else:
            self.data = self.data.fillna(value)
        return self.data
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        self.data = self.data.drop_duplicates()
        return self.data
    
    def fix_column_types(self, column_type_map):
        """Convert columns to specified types"""
        for column, new_type in column_type_map.items():
            if column in self.data.columns:
                self.data[column] = self.data[column].astype(new_type)
        return self.data
    
    def rename_columns(self, column_map):
        """Rename columns"""
        self.data = self.data.rename(columns=column_map)
        return self.data
    
    def get_cleaning_report(self):
        """Get report of what was cleaned"""
        if self.original_shape:
            current_shape = self.data.shape
            rows_removed = self.original_shape[0] - current_shape[0]
            cols_removed = self.original_shape[1] - current_shape[1]
            
            return {
                'original_shape': self.original_shape,
                'current_shape': current_shape,
                'rows_removed': rows_removed,
                'cols_removed': cols_removed
            }
        return None