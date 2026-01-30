import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, data):
        self.data = data
        self.original_shape = data.shape if data is not None else None
        self.cleaning_history = []
    
    def remove_nulls(self, columns=None, threshold=None):
        """
        Remove rows with null values
        
        Args:
            columns: List of columns to check for nulls (None = all columns)
            threshold: Minimum number of non-null values required (None = all must be non-null)
        """
        before = len(self.data)
        if columns:
            if threshold:
                self.data = self.data.dropna(subset=columns, thresh=threshold)
            else:
                self.data = self.data.dropna(subset=columns)
        else:
            if threshold:
                self.data = self.data.dropna(thresh=threshold)
            else:
                self.data = self.data.dropna()
        
        after = len(self.data)
        self.cleaning_history.append(f"Removed {before - after} rows with null values")
        return self.data
    
    def fill_nulls(self, value=0, columns=None, method=None):
        """
        Fill null values with specified value or method
        
        Args:
            value: Value to fill nulls with
            columns: List of columns to fill (None = all columns)
            method: 'mean', 'median', 'mode', 'forward', 'backward', or None
        """
        if method:
            if columns:
                for col in columns:
                    if col in self.data.columns:
                        if method == 'mean':
                            self.data[col].fillna(self.data[col].mean(), inplace=True)
                        elif method == 'median':
                            self.data[col].fillna(self.data[col].median(), inplace=True)
                        elif method == 'mode':
                            self.data[col].fillna(self.data[col].mode()[0] if not self.data[col].mode().empty else value, inplace=True)
                        elif method == 'forward':
                            self.data[col].fillna(method='ffill', inplace=True)
                        elif method == 'backward':
                            self.data[col].fillna(method='bfill', inplace=True)
            else:
                if method == 'forward':
                    self.data.fillna(method='ffill', inplace=True)
                elif method == 'backward':
                    self.data.fillna(method='bfill', inplace=True)
        else:
            if columns:
                self.data[columns] = self.data[columns].fillna(value)
            else:
                self.data = self.data.fillna(value)
        
        self.cleaning_history.append(f"Filled null values using {method if method else value}")
        return self.data
    
    def remove_duplicates(self, subset=None, keep='first'):
        """
        Remove duplicate rows
        
        Args:
            subset: List of columns to consider for duplicates (None = all columns)
            keep: 'first', 'last', or False (remove all duplicates)
        """
        before = len(self.data)
        self.data = self.data.drop_duplicates(subset=subset, keep=keep)
        after = len(self.data)
        self.cleaning_history.append(f"Removed {before - after} duplicate rows")
        return self.data
    
    def fix_column_types(self, column_type_map):
        """Convert columns to specified types"""
        for column, new_type in column_type_map.items():
            if column in self.data.columns:
                try:
                    self.data[column] = self.data[column].astype(new_type)
                    self.cleaning_history.append(f"Changed {column} type to {new_type}")
                except Exception as e:
                    print(f"Warning: Could not convert {column} to {new_type}: {e}")
        return self.data
    
    def rename_columns(self, column_map):
        """Rename columns"""
        self.data = self.data.rename(columns=column_map)
        self.cleaning_history.append(f"Renamed {len(column_map)} columns")
        return self.data
    
    def remove_outliers(self, columns=None, method='iqr', threshold=1.5):
        """
        Remove outliers using IQR or Z-score method
        
        Args:
            columns: List of numeric columns to check (None = all numeric)
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier (default 1.5) or Z-score threshold (default 3)
        """
        before = len(self.data)
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in columns:
            if col in self.data.columns and pd.api.types.is_numeric_dtype(self.data[col]):
                if method == 'iqr':
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]
                elif method == 'zscore':
                    z_scores = np.abs((self.data[col] - self.data[col].mean()) / self.data[col].std())
                    self.data = self.data[z_scores < threshold]
        
        after = len(self.data)
        self.cleaning_history.append(f"Removed {before - after} outlier rows using {method} method")
        return self.data
    
    def drop_columns(self, columns):
        """Drop specified columns"""
        columns_to_drop = [col for col in columns if col in self.data.columns]
        self.data = self.data.drop(columns=columns_to_drop)
        self.cleaning_history.append(f"Dropped {len(columns_to_drop)} columns")
        return self.data
    
    def infer_dtypes(self):
        """Automatically infer and convert data types"""
        for col in self.data.columns:
            # Try to convert to datetime
            if self.data[col].dtype == 'object':
                try:
                    self.data[col] = pd.to_datetime(self.data[col])
                    self.cleaning_history.append(f"Converted {col} to datetime")
                    continue
                except:
                    pass
                
                # Try to convert to numeric
                try:
                    self.data[col] = pd.to_numeric(self.data[col])
                    self.cleaning_history.append(f"Converted {col} to numeric")
                except:
                    pass
        
        return self.data
    
    def clean_text_columns(self, columns=None, lowercase=True, remove_special=True):
        """
        Clean text columns by removing special characters and converting to lowercase
        
        Args:
            columns: List of text columns to clean (None = all object columns)
            lowercase: Convert to lowercase
            remove_special: Remove special characters
        """
        if columns is None:
            columns = self.data.select_dtypes(include=['object']).columns.tolist()
        
        for col in columns:
            if col in self.data.columns:
                if lowercase:
                    self.data[col] = self.data[col].astype(str).str.lower()
                if remove_special:
                    self.data[col] = self.data[col].astype(str).str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                self.data[col] = self.data[col].str.strip()
        
        self.cleaning_history.append(f"Cleaned {len(columns)} text columns")
        return self.data
    
    def standardize_column_names(self):
        """Standardize column names: lowercase, replace spaces with underscores"""
        new_columns = {}
        for col in self.data.columns:
            new_name = col.lower().strip().replace(' ', '_').replace('-', '_')
            new_name = re.sub(r'[^a-z0-9_]', '', new_name)
            new_columns[col] = new_name
        
        self.data = self.data.rename(columns=new_columns)
        self.cleaning_history.append("Standardized column names")
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
                'cols_removed': cols_removed,
                'cleaning_history': self.cleaning_history
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
    @staticmethod
    def dash_ready_data():
        # 1️⃣ Load raw data
        df = pd.read_csv("data/raw/ford_go_bike.csv")

        # 2️⃣ Rename columns (standardize)
        df = df.rename(columns={
        "duration_sec": "duration_sec",
        "start_time": "start_time",
        "start_station_name": "start_station_name",
        "start_station_latitude": "start_station_latitude",
        "start_station_longitude": "start_station_longitude",
        "user_type": "user_type",
        "member_gender": "member_gender",
        "member_birth_year": "birth_year"
        })

        # 3️⃣ Drop rows with critical missing values
        df = df.dropna(subset=[
        "start_time",
        "duration_sec",
        "start_station_name",
        "start_station_latitude",
        "start_station_longitude"
        ])

        # 4️⃣ Convert start_time to datetime
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")

        # 5️⃣ Remove invalid durations
        df = df[df["duration_sec"] > 0]

        # 6️⃣ Fix gender column
        df["member_gender"] = df["member_gender"].fillna("Other")

        # 7️⃣ Calculate age
        CURRENT_YEAR = 2019
        df["birth_year"] = pd.to_numeric(df["birth_year"], errors="coerce")
        df["age"] = CURRENT_YEAR - df["birth_year"]

        # Remove unrealistic ages
        df = df[(df["age"] >= 18) & (df["age"] <= 80)]

        # 8️⃣ Create age groups
        df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 29, 50, 200],
        labels=["Young", "Adult", "Senior"]
        )

        # 9️⃣ Day of week & month (USED IN DASH)
        df["day_of_week"] = df["start_time"].dt.day_name()
        df["month"] = df["start_time"].dt.strftime("%b")

        # 🔟 Trip ID
        df = df.reset_index(drop=True)
        df["trip_id"] = df.index + 1

        # 1️⃣1️⃣ Keep only required columns
        df = df[
        [
        "trip_id",
        "start_time",
        "duration_sec",
        "start_station_name",
        "start_station_latitude",
        "start_station_longitude",
        "user_type",
        "member_gender",
        "age",
        "age_group",
        "day_of_week",
        "month"
        ]
        ]

        # 1️⃣2️⃣ Save cleaned data
        df.to_csv("cleaned_fordgobike.csv", index=False)

        print("✅ Data cleaning finished. File saved as cleaned_fordgobike.csv")
