import pandas as pd
import numpy as np
from scipy import stats
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
    def all_columns_outlier_percentage(self, method='iqr', z_threshold=3):
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        results = []

        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outliers = (self.data[col] < lower) | (self.data[col] > upper)
            
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.data[col], nan_policy='omit'))
                outliers = z_scores > z_threshold
            
            else:
             raise ValueError("method must be 'iqr' or 'zscore'")
            pct = outliers.sum() / len(self.data) * 100
            results.append((col, pct))
         
        return pd.DataFrame(results, columns=['Column', 'Outlier %']).sort_values(by='Outlier %', ascending=False)
    
    def handle_outliers(self, column, method='iqr', action='cap'):
        """Handle outliers in a column"""
        if method == 'iqr':
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(self.data[column], nan_policy='omit'))
            lower_bound = self.data[column][z_scores <= 3].min()
            upper_bound = self.data[column][z_scores <= 3].max()
        else:
            raise ValueError("method must be 'iqr' or 'zscore'")

        if action == 'remove':
            self.data.drop(self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)].index, inplace=True)
        elif action == 'replace':
            median_val = self.data[column].median()
            self.data[column] = np.where(
                (self.data[column] < lower_bound) | (self.data[column] > upper_bound),
                median_val,
                self.data[column]
            )
        elif action == 'cap':
            self.data[column] = np.clip(self.data[column], lower_bound, upper_bound)
        else:
            raise ValueError("action must be 'remove', 'replace', or 'cap'")
        return self.data