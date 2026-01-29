"""
Data Pipeline Orchestrator
Coordinates the entire data processing workflow from loading to visualization

This module provides a high-level API to:
1. Load data from various sources
2. Perform automated data quality checks
3. Clean and transform data
4. Generate comprehensive reports
5. Export processed data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

from data_loader import DataLoader
from data_overview import DataOverview
from data_cleaner import DataCleaner


class DataPipeline:
    """
    Orchestrates the complete data processing pipeline
    """
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.loader = DataLoader()
        self.overview = DataOverview()
        self.cleaner = None
        self.data = None
        self.pipeline_log = []
        
    def log(self, message, level="INFO"):
        """Log pipeline activities"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.pipeline_log.append(log_entry)
        if self.verbose:
            print(log_entry)
    
    def load_data(self, file_path, file_type='auto'):
        """
        Load data from file
        
        Args:
            file_path: Path to data file
            file_type: 'csv', 'excel', 'json', or 'auto' (detect from extension)
        
        Returns:
            DataFrame or None
        """
        self.log(f"Loading data from: {file_path}")
        
        if file_type == 'auto':
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.csv':
                file_type = 'csv'
            elif ext in ['.xlsx', '.xls']:
                file_type = 'excel'
            elif ext == '.json':
                file_type = 'json'
            else:
                self.log(f"Unknown file extension: {ext}", "ERROR")
                return None
        
        try:
            if file_type == 'csv':
                self.data = self.loader.load_csv(file_path)
            elif file_type == 'excel':
                self.data = self.loader.load_excel(file_path)
            elif file_type == 'json':
                self.data = self.loader.load_json(file_path)
            
            if self.data is not None:
                self.overview.set_data(self.data)
                self.cleaner = DataCleaner(self.data.copy())
                self.log(f"✓ Data loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
                return self.data
            else:
                self.log("✗ Failed to load data", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"✗ Error loading data: {str(e)}", "ERROR")
            return None
    
    def analyze_data_quality(self):
        """
        Perform comprehensive data quality analysis
        
        Returns:
            Dictionary with quality metrics
        """
        if self.data is None:
            self.log("No data loaded", "WARNING")
            return None
        
        self.log("Analyzing data quality...")
        
        quality_report = {
            'shape': self.overview.shape(),
            'duplicates': self.overview.duplicates(),
            'outliers': self.overview.outliers(),
            'overview': self.overview.overview(),
            'numeric_stats': self.overview.get_stats(numeric=True, categorical=False, datetime=False),
            'categorical_stats': self.overview.get_stats(numeric=False, categorical=True, datetime=False),
        }
        
        # Calculate quality score
        total_rows = self.data.shape[0]
        total_cols = self.data.shape[1]
        
        # Null percentage
        null_pct = (self.data.isnull().sum().sum() / (total_rows * total_cols)) * 100
        
        # Duplicate percentage
        dup_count = self.data.duplicated().sum()
        dup_pct = (dup_count / total_rows) * 100 if total_rows > 0 else 0
        
        # Quality score (0-100)
        quality_score = 100 - (null_pct * 0.5) - (dup_pct * 0.5)
        quality_score = max(0, min(100, quality_score))
        
        quality_report['quality_score'] = round(quality_score, 2)
        quality_report['null_percentage'] = round(null_pct, 2)
        quality_report['duplicate_percentage'] = round(dup_pct, 2)
        
        self.log(f"✓ Quality Score: {quality_score:.2f}/100")
        self.log(f"  - Null values: {null_pct:.2f}%")
        self.log(f"  - Duplicates: {dup_pct:.2f}%")
        
        return quality_report
    
    def auto_clean(self, remove_duplicates=True, handle_nulls='drop', 
                   remove_outliers=False, standardize_columns=True):
        """
        Automatically clean data based on best practices
        
        Args:
            remove_duplicates: Remove duplicate rows
            handle_nulls: 'drop', 'fill_mean', 'fill_median', 'fill_mode', or 'fill_zero'
            remove_outliers: Remove statistical outliers
            standardize_columns: Standardize column names
        
        Returns:
            Cleaned DataFrame
        """
        if self.cleaner is None:
            self.log("No data loaded for cleaning", "WARNING")
            return None
        
        self.log("Starting automatic data cleaning...")
        
        original_shape = self.cleaner.data.shape
        
        # Standardize column names
        if standardize_columns:
            self.cleaner.standardize_column_names()
            self.log("✓ Standardized column names")
        
        # Remove duplicates
        if remove_duplicates:
            self.cleaner.remove_duplicates()
            self.log("✓ Removed duplicate rows")
        
        # Handle null values
        if handle_nulls == 'drop':
            self.cleaner.remove_nulls()
            self.log("✓ Removed rows with null values")
        elif handle_nulls == 'fill_mean':
            numeric_cols = self.cleaner.data.select_dtypes(include=[np.number]).columns.tolist()
            self.cleaner.fill_nulls(method='mean', columns=numeric_cols)
            self.log("✓ Filled nulls with mean values")
        elif handle_nulls == 'fill_median':
            numeric_cols = self.cleaner.data.select_dtypes(include=[np.number]).columns.tolist()
            self.cleaner.fill_nulls(method='median', columns=numeric_cols)
            self.log("✓ Filled nulls with median values")
        elif handle_nulls == 'fill_mode':
            self.cleaner.fill_nulls(method='mode')
            self.log("✓ Filled nulls with mode values")
        elif handle_nulls == 'fill_zero':
            self.cleaner.fill_nulls(value=0)
            self.log("✓ Filled nulls with zeros")
        
        # Remove outliers
        if remove_outliers:
            self.cleaner.remove_outliers(method='iqr', threshold=1.5)
            self.log("✓ Removed outliers using IQR method")
        
        # Infer data types
        self.cleaner.infer_dtypes()
        self.log("✓ Inferred and converted data types")
        
        # Update main data reference
        self.data = self.cleaner.data
        self.overview.set_data(self.data)
        
        new_shape = self.data.shape
        self.log(f"✓ Cleaning complete: {original_shape} → {new_shape}")
        self.log(f"  Removed {original_shape[0] - new_shape[0]} rows, {original_shape[1] - new_shape[1]} columns")
        
        return self.data
    
    def generate_report(self, output_path='data_quality_report.txt'):
        """
        Generate comprehensive text report
        
        Args:
            output_path: Path to save the report
        
        Returns:
            Report string
        """
        if self.data is None:
            self.log("No data available for report", "WARNING")
            return None
        
        self.log(f"Generating report: {output_path}")
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DATA QUALITY REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Dataset Shape: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
        report_lines.append("")
        
        # Overview
        report_lines.append("-" * 80)
        report_lines.append("COLUMN OVERVIEW")
        report_lines.append("-" * 80)
        overview_df = self.overview.overview()
        if overview_df is not None:
            report_lines.append(overview_df.to_string())
        report_lines.append("")
        
        # Duplicates
        report_lines.append("-" * 80)
        report_lines.append("DUPLICATES")
        report_lines.append("-" * 80)
        dup_df = self.overview.duplicates()
        if dup_df is not None:
            report_lines.append(dup_df.to_string())
        report_lines.append("")
        
        # Statistics
        report_lines.append("-" * 80)
        report_lines.append("NUMERIC STATISTICS")
        report_lines.append("-" * 80)
        stats_df = self.overview.get_stats(numeric=True, categorical=False, datetime=False)
        if stats_df is not None and not stats_df.empty:
            report_lines.append(stats_df.to_string())
        else:
            report_lines.append("No numeric columns found")
        report_lines.append("")
        
        # Cleaning history
        if self.cleaner and self.cleaner.cleaning_history:
            report_lines.append("-" * 80)
            report_lines.append("CLEANING HISTORY")
            report_lines.append("-" * 80)
            for entry in self.cleaner.cleaning_history:
                report_lines.append(f"  • {entry}")
            report_lines.append("")
        
        # Pipeline log
        report_lines.append("-" * 80)
        report_lines.append("PIPELINE LOG")
        report_lines.append("-" * 80)
        for log_entry in self.pipeline_log:
            report_lines.append(log_entry)
        
        report_lines.append("=" * 80)
        
        report_text = "\n".join(report_lines)
        
        # Save to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            self.log(f"✓ Report saved to: {output_path}")
        except Exception as e:
            self.log(f"✗ Error saving report: {str(e)}", "ERROR")
        
        return report_text
    
    def export_data(self, output_path, file_type='csv'):
        """
        Export processed data
        
        Args:
            output_path: Path to save the file
            file_type: 'csv', 'excel', or 'json'
        
        Returns:
            True if successful, False otherwise
        """
        if self.data is None:
            self.log("No data to export", "WARNING")
            return False
        
        self.log(f"Exporting data to: {output_path}")
        
        try:
            if file_type == 'csv':
                self.data.to_csv(output_path, index=False)
            elif file_type == 'excel':
                self.data.to_excel(output_path, index=False)
            elif file_type == 'json':
                self.data.to_json(output_path, orient='records', indent=2)
            else:
                self.log(f"Unknown file type: {file_type}", "ERROR")
                return False
            
            self.log(f"✓ Data exported successfully")
            return True
            
        except Exception as e:
            self.log(f"✗ Error exporting data: {str(e)}", "ERROR")
            return False
    
    def run_full_pipeline(self, input_path, output_path=None, 
                         clean_config=None, generate_report_file=True):
        """
        Run the complete pipeline from start to finish
        
        Args:
            input_path: Path to input data file
            output_path: Path to save cleaned data (None = auto-generate)
            clean_config: Dictionary with cleaning configuration
            generate_report_file: Whether to generate a report file
        
        Returns:
            Dictionary with pipeline results
        """
        self.log("=" * 80)
        self.log("STARTING FULL DATA PIPELINE")
        self.log("=" * 80)
        
        # Default cleaning configuration
        if clean_config is None:
            clean_config = {
                'remove_duplicates': True,
                'handle_nulls': 'drop',
                'remove_outliers': False,
                'standardize_columns': True
            }
        
        # Auto-generate output path if not provided
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"cleaned_{base_name}.csv"
        
        # Step 1: Load data
        if self.load_data(input_path) is None:
            return {'success': False, 'error': 'Failed to load data'}
        
        # Step 2: Analyze quality
        quality_report = self.analyze_data_quality()
        
        # Step 3: Clean data
        self.auto_clean(**clean_config)
        
        # Step 4: Generate report
        if generate_report_file:
            report_path = output_path.replace('.csv', '_report.txt')
            self.generate_report(report_path)
        
        # Step 5: Export cleaned data
        self.export_data(output_path)
        
        self.log("=" * 80)
        self.log("PIPELINE COMPLETED SUCCESSFULLY")
        self.log("=" * 80)
        
        return {
            'success': True,
            'input_path': input_path,
            'output_path': output_path,
            'original_shape': quality_report['shape'] if quality_report else None,
            'final_shape': self.data.shape,
            'quality_score': quality_report['quality_score'] if quality_report else None,
            'cleaning_history': self.cleaner.cleaning_history if self.cleaner else []
        }


# Example usage
if __name__ == "__main__":
    # Create pipeline instance
    pipeline = DataPipeline(verbose=True)
    
    # Example 1: Run full pipeline
    print("\n" + "="*80)
    print("EXAMPLE: Running Full Pipeline")
    print("="*80 + "\n")
    
    # Check if sample data exists
    if os.path.exists("fordgobike-tripdataFor201902.csv"):
        result = pipeline.run_full_pipeline(
            input_path="fordgobike-tripdataFor201902.csv",
            output_path="processed_fordgobike.csv",
            clean_config={
                'remove_duplicates': True,
                'handle_nulls': 'fill_mean',
                'remove_outliers': False,
                'standardize_columns': True
            }
        )
        
        print("\n" + "="*80)
        print("PIPELINE RESULTS")
        print("="*80)
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("Sample data file not found. Please provide a data file to process.")
        print("\nYou can use the pipeline like this:")
        print("""
pipeline = DataPipeline()
result = pipeline.run_full_pipeline(
    input_path="your_data.csv",
    output_path="cleaned_data.csv"
)
        """)
