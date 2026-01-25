import pandas as pd
import numpy as np

class DataOverview:
    def __init__(self):
        """Initialize the DataOverview class"""
        self.data = None
    
    def set_data(self, data):
        """Set data for analysis"""
        self.data = data
    
    # 1. SHAPE FUNCTION
    def shape(self, data=None):
        """Get shape (rows, columns) of data"""
        if data is None:
            data = self.data
        
        if data is not None:
            return data.shape
        return None
    
    # 2. SAMPLE FUNCTION  
    def sample(self, data=None, n=5):
        """Get first n rows as DataFrame"""
        if data is None:
            data = self.data
        
        if data is not None:
            return data.head(n)
        return None
    
    # 3. DUPLICATES FUNCTION
    def duplicates(self, data=None):
        """Get duplicates info as DataFrame"""
        if data is None:
            data = self.data
        
        if data is None:
            return None
        
        # Count duplicate rows
        duplicate_count = data.duplicated().sum()
        total_rows = len(data)
        duplicate_percent = (duplicate_count / total_rows * 100) if total_rows > 0 else 0
        
        # Create DataFrame
        dup = pd.DataFrame({
            'Metric': ['Duplicate Rows', 'Duplicate Percentage'],
            'Value': [duplicate_count, f"{duplicate_percent:.2f}%"]
        })
        
        return dup
    
    # 4. OUTLIERS FUNCTION (IQR method)
    def outliers(self, data=None):
        """Get outliers info per numeric column using IQR method"""
        if data is None:
            data = self.data
        
        if data is None:
            return None
        
        outliers_data = []
        
        for column in data.select_dtypes(include=[np.number]).columns:
            col_data = data[column].dropna()
            
            if len(col_data) > 0:
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Count outliers
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_count = len(outliers)
                outlier_percent = (outlier_count / len(col_data) * 100) if len(col_data) > 0 else 0
                
                outliers_data.append({
                    'Column': column,
                    'Outliers #': outlier_count,
                    'Outliers %': f"{outlier_percent:.2f}%"
                })
        
        if outliers_data:
            return pd.DataFrame(outliers_data)
        else:
            return pd.DataFrame(columns=['Column', 'Outliers #', 'Outliers %'])
    
    
    # 5. STATS FUNCTION
    def get_stats(self, data=None, numeric=True, categorical= False, datetime=False):
        """Get statistics for selected column types"""
        if data is None:
            data = self.data
        
        if data is None:
            return None
        
        stats_data = []
        
        for column in data.columns:
            col_data = data[column].dropna()
            
            # Skip if no data
            if len(col_data) == 0:
                continue
            
            # NUMERIC columns
            if numeric and pd.api.types.is_numeric_dtype(data[column]):
                stats_data.append({
                    'Column': column,
                    'Type': 'numeric',
                    'Count': len(col_data),
                    'Mean': f"{col_data.mean():.2f}",
                    'Std': f"{col_data.std():.2f}",
                    'Min': f"{col_data.min():.2f}",
                    'Max': f"{col_data.max():.2f}"
                })
            
            # DATETIME columns  
            elif datetime and pd.api.types.is_datetime64_any_dtype(data[column]):
                stats_data.append({
                    'Column': column,
                    'Type': 'datetime',
                    'Count': len(col_data),
                    'Start': col_data.min(),
                    'End': col_data.max(),
                    'Days Range': (col_data.max() - col_data.min()).days
                })
            
            # CATEGORICAL/TEXT columns
            elif categorical and (pd.api.types.is_string_dtype(data[column]) or 
                                pd.api.types.is_object_dtype(data[column]) or
                                pd.api.types.is_categorical_dtype(data[column])):
                stats_data.append({
                    'Column': column,
                    'Type': 'categorical',
                    'Count': len(col_data),
                    'Unique': col_data.nunique(),
                    'Most Common': col_data.mode().iloc[0] if not col_data.mode().empty else 'N/A'
                })
        
        if stats_data:
            return pd.DataFrame(stats_data)
        else:
            return pd.DataFrame(columns=['No columns match the selected types'])

    # 5. MAIN OVERVIEW TABLE
    def overview(self, data=None):
        """Get main overview table as DataFrame"""
        if data is None:
            data = self.data
        
        if data is None:
            return None
        
        overview_data = []
        total_rows = len(data)
        
        for column in data.columns:
            # Type
            dtype = str(data[column].dtype)
            
            # Nulls %
            null_count = data[column].isnull().sum()
            null_percent = (null_count / total_rows * 100) if total_rows > 0 else 0
            
            # Uniques
            unique_count = data[column].nunique()
            
            # Outliers for numeric columns
            if data[column].dtype in [np.int64, np.float64]:
                col_data = data[column].dropna()
                if len(col_data) > 0:
                    Q1 = col_data.quantile(0.25)
                    Q3 = col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                    outlier_count = len(outliers)
                    outlier_percent = (outlier_count / len(col_data) * 100) if len(col_data) > 0 else 0
                else:
                    outlier_count = 0
                    outlier_percent = 0
            else:
                outlier_count = None
                outlier_percent = None
            
            overview_data.append({
                'Column': column,
                'Type': dtype,
                'Nulls #': null_count,
                'Nulls %': f"{null_percent:.2f}%",
                'Uniques': unique_count,
                'Outliers #': outlier_count,
                'Outliers %': f"{outlier_percent:.2f}%" if outlier_percent is not None else None
            })
        
        return pd.DataFrame(overview_data)