# main.py
from data_cleaner import DataCleaner
from data_overview import DataOverview
from data_loader import DataLoader
import pandas as pd
from clean_forbike import dash_ready_data

def display_menu(title, options):
    """Helper function to display menus"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print('='*50)
    for key, value in options.items():
        print(f"{key}. {value}")
    print('='*50)

def main():
    print("📊 DATA ANALYSIS PIPELINE")
    print("="*50)
    
    # Initialize classes
    loader = DataLoader()
    overview = DataOverview()
    cleaner = None
    
    current_data = None
    
    while True:
        # Main menu
        main_menu = {
            '1': 'Load Data',
            '2': 'Data Overview & Analysis',
            '3': 'Data Cleaning',
            '4': 'Save Data',
            '5': 'Final file of data ready to use in dash',
            '6': 'Exit'
        }
        
        display_menu("MAIN MENU", main_menu)
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            # Load Data
            load_menu = {
                '1': 'Load CSV',
                '2': 'Load Excel',
                '3': 'Load JSON',
                '4': 'Back to Main Menu'
            }
            
            display_menu("LOAD DATA", load_menu)
            load_choice = input("Select option (1-4): ").strip()
            
            if load_choice == '1':
                file_path = input("Enter CSV file path: ").strip()
                current_data = loader.load_csv(file_path)
            elif load_choice == '2':
                file_path = input("Enter Excel file path: ").strip()
                current_data = loader.load_excel(file_path)
            elif load_choice == '3':
                file_path = input("Enter JSON file path: ").strip()
                current_data = loader.load_json(file_path)
            elif load_choice == '4':
                continue
            else:
                print("Invalid choice!")
            
            if current_data is not None:
                overview.set_data(current_data)
                cleaner = DataCleaner(current_data.copy())
                print(f"\n✅ Data loaded successfully!")
                print(f"   Shape: {current_data.shape}")
        
        elif choice == '2':
            # Data Overview & Analysis
            if current_data is None:
                print("\n❌ No data loaded! Please load data first.")
                continue
            
            overview_menu = {
                '1': 'Show Data Shape',
                '2': 'Show Sample Data',
                '3': 'Show Overview Table',
                '4': 'Check for Duplicates',
                '5': 'Check for Outliers',
                '6': 'Get Statistics',
                '7': 'Back to Main Menu'
            }
            
            display_menu("DATA OVERVIEW & ANALYSIS", overview_menu)
            overview_choice = input("Select option (1-7): ").strip()
            
            if overview_choice == '1':
                print(f"\n📏 Data Shape: {overview.shape()}")
            elif overview_choice == '2':
                n = input("Number of rows to show (default: 5): ").strip()
                n = int(n) if n.isdigit() else 5
                print("\n📋 Sample Data:")
                print(overview.sample(n=n))
            elif overview_choice == '3':
                print("\n📊 Overview Table:")
                print(overview.overview())
            elif overview_choice == '4':
                print("\n🔍 Duplicates Check:")
                print(overview.duplicates())
            elif overview_choice == '5':
                print("\n⚠️  Outliers Detection:")
                outliers_df = overview.outliers()
                if outliers_df is not None and not outliers_df.empty:
                    print(outliers_df)
                else:
                    print("No numeric columns found or no outliers detected.")
            elif overview_choice == '6':
                print("\n📈 Statistics:")
                print("\n1. Numeric Statistics")
                print("2. Categorical Statistics")
                print("3. Datetime Statistics")
                print("4. All Statistics")
                
                stat_choice = input("\nSelect statistics type (1-4): ").strip()
                
                if stat_choice == '1':
                    print(overview.get_stats(numeric=True, categorical=False, datetime=False))
                elif stat_choice == '2':
                    print(overview.get_stats(numeric=False, categorical=True, datetime=False))
                elif stat_choice == '3':
                    print(overview.get_stats(numeric=False, categorical=False, datetime=True))
                elif stat_choice == '4':
                    print(overview.get_stats(numeric=True, categorical=True, datetime=True))
                else:
                    print("Invalid choice!")
            elif overview_choice == '7':
                continue
        
        elif choice == '3':
            # Data Cleaning
            if current_data is None:
                print("\n❌ No data loaded! Please load data first.")
                continue
            
            cleaning_menu = {
                '1': 'Remove Null Rows',
                '2': 'Fill Null Values',
                '3': 'Remove Duplicates',
                '4': 'Remove Outliers (NEW)',
                '5': 'Fix Column Types',
                '6': 'Rename Columns',
                '7': 'Drop Columns (NEW)',
                '8': 'Infer Data Types (NEW)',
                '9': 'Clean Text Columns (NEW)',
                '10': 'Standardize Column Names (NEW)',
                '11': 'Show Cleaning Report',
                '12': 'Reset to Original',
                '13': 'Back to Main Menu'
            }
            
            display_menu("DATA CLEANING", cleaning_menu)
            clean_choice = input("Select option (1-13): ").strip()
            
            if clean_choice == '1':
                columns = input("Enter columns to check (comma-separated, leave empty for all): ").strip()
                columns = [col.strip() for col in columns.split(',')] if columns else None
                current_data = cleaner.remove_nulls(columns)
                overview.set_data(current_data)
                print("✅ Null rows removed!")
                
            elif clean_choice == '2':
                print("\n📝 Fill Null Values")
                print("Available methods:")
                print("  1. Fill with specific value")
                print("  2. Fill with mean (numeric columns)")
                print("  3. Fill with median (numeric columns)")
                print("  4. Fill with mode (most common value)")
                print("  5. Forward fill")
                print("  6. Backward fill")
                
                method_choice = input("\nSelect method (1-6): ").strip()
                columns = input("Enter columns to fill (comma-separated, leave empty for all): ").strip()
                columns = [col.strip() for col in columns.split(',')] if columns else None
                
                if method_choice == '1':
                    value = input("Enter value to fill (default: 0): ").strip()
                    value = float(value) if '.' in value else (int(value) if value.isdigit() else 0)
                    current_data = cleaner.fill_nulls(value=value, columns=columns)
                elif method_choice == '2':
                    current_data = cleaner.fill_nulls(method='mean', columns=columns)
                elif method_choice == '3':
                    current_data = cleaner.fill_nulls(method='median', columns=columns)
                elif method_choice == '4':
                    current_data = cleaner.fill_nulls(method='mode', columns=columns)
                elif method_choice == '5':
                    current_data = cleaner.fill_nulls(method='forward', columns=columns)
                elif method_choice == '6':
                    current_data = cleaner.fill_nulls(method='backward', columns=columns)
                else:
                    print("Invalid method choice!")
                    continue
                
                overview.set_data(current_data)
                print("✅ Null values filled!")
                
            elif clean_choice == '3':
                current_data = cleaner.remove_duplicates()
                overview.set_data(current_data)
                print("✅ Duplicates removed!")
                
            elif clean_choice == '4':
                print("\n🔍 Remove Outliers")
                print("Available methods:")
                print("  1. IQR (Interquartile Range) - default threshold: 1.5")
                print("  2. Z-score - default threshold: 3")
                
                method_choice = input("\nSelect method (1-2): ").strip()
                columns = input("Enter numeric columns to check (comma-separated, leave empty for all numeric): ").strip()
                columns = [col.strip() for col in columns.split(',')] if columns else None
                
                if method_choice == '1':
                    threshold = input("Enter IQR threshold (default: 1.5): ").strip()
                    threshold = float(threshold) if threshold else 1.5
                    current_data = cleaner.remove_outliers(columns=columns, method='iqr', threshold=threshold)
                elif method_choice == '2':
                    threshold = input("Enter Z-score threshold (default: 3): ").strip()
                    threshold = float(threshold) if threshold else 3
                    current_data = cleaner.remove_outliers(columns=columns, method='zscore', threshold=threshold)
                else:
                    print("Invalid method choice!")
                    continue
                
                overview.set_data(current_data)
                print("✅ Outliers removed!")
                
            elif clean_choice == '5':
                print("\nCurrent columns and types:")
                for col in current_data.columns:
                    print(f"  {col}: {current_data[col].dtype}")
                
                print("\nEnter column type mappings (format: column:type)")
                print("Example: age:int, salary:float, date:datetime64")
                mappings = input("Enter mappings: ").strip()
                
                if mappings:
                    column_type_map = {}
                    for mapping in mappings.split(','):
                        if ':' in mapping:
                            col, typ = mapping.split(':')
                            column_type_map[col.strip()] = typ.strip()
                    
                    current_data = cleaner.fix_column_types(column_type_map)
                    overview.set_data(current_data)
                    print("✅ Column types fixed!")
                else:
                    print("No mappings provided.")
                    
            elif clean_choice == '6':
                print("\nCurrent columns:")
                for col in current_data.columns:
                    print(f"  {col}")
                
                print("\nEnter column renamings (format: old:new)")
                print("Example: old_name:new_name, another_old:another_new")
                renames = input("Enter renamings: ").strip()
                
                if renames:
                    column_map = {}
                    for rename in renames.split(','):
                        if ':' in rename:
                            old, new = rename.split(':')
                            column_map[old.strip()] = new.strip()
                    
                    current_data = cleaner.rename_columns(column_map)
                    overview.set_data(current_data)
                    print("✅ Columns renamed!")
                else:
                    print("No renamings provided.")
                    
            elif clean_choice == '7':
                print("\n🗑️ Drop Columns")
                print("Current columns:")
                for col in current_data.columns:
                    print(f"  {col}")
                
                columns = input("\nEnter columns to drop (comma-separated): ").strip()
                if columns:
                    columns_list = [col.strip() for col in columns.split(',')]
                    current_data = cleaner.drop_columns(columns_list)
                    overview.set_data(current_data)
                    print("✅ Columns dropped!")
                else:
                    print("No columns specified.")
                    
            elif clean_choice == '8':
                print("\n🔄 Infer Data Types")
                print("Automatically detecting and converting data types...")
                current_data = cleaner.infer_dtypes()
                overview.set_data(current_data)
                print("✅ Data types inferred!")
                print("\nNew column types:")
                for col in current_data.columns:
                    print(f"  {col}: {current_data[col].dtype}")
                    
            elif clean_choice == '9':
                print("\n🧹 Clean Text Columns")
                print("Current text columns:")
                text_cols = current_data.select_dtypes(include=['object']).columns.tolist()
                for col in text_cols:
                    print(f"  {col}")
                
                columns = input("\nEnter columns to clean (comma-separated, leave empty for all text columns): ").strip()
                columns = [col.strip() for col in columns.split(',')] if columns else None
                
                lowercase = input("Convert to lowercase? (y/n, default: y): ").strip().lower() != 'n'
                remove_special = input("Remove special characters? (y/n, default: y): ").strip().lower() != 'n'
                
                current_data = cleaner.clean_text_columns(columns=columns, lowercase=lowercase, remove_special=remove_special)
                overview.set_data(current_data)
                print("✅ Text columns cleaned!")
                    
            elif clean_choice == '10':
                print("\n📝 Standardize Column Names")
                print("Current columns:")
                for col in current_data.columns:
                    print(f"  {col}")
                
                confirm = input("\nStandardize all column names? (y/n): ").strip().lower()
                if confirm == 'y':
                    current_data = cleaner.standardize_column_names()
                    overview.set_data(current_data)
                    print("✅ Column names standardized!")
                    print("\nNew column names:")
                    for col in current_data.columns:
                        print(f"  {col}")
                else:
                    print("Operation cancelled.")
                    
            elif clean_choice == '11':
                report = cleaner.get_cleaning_report()
                if report:
                    print("\n📋 Cleaning Report:")
                    print(f"  Original shape: {report['original_shape']}")
                    print(f"  Current shape: {report['current_shape']}")
                    print(f"  Rows removed: {report['rows_removed']}")
                    print(f"  Columns removed: {report['cols_removed']}")
                    
                    if 'cleaning_history' in report and report['cleaning_history']:
                        print("\n  Cleaning History:")
                        for entry in report['cleaning_history']:
                            print(f"    • {entry}")
                else:
                    print("No cleaning report available.")
                    
            elif clean_choice == '12':
                if cleaner.original_shape:
                    cleaner = DataCleaner(pd.read_csv(loader.file_path) if loader.file_path else None)
                    current_data = cleaner.data
                    overview.set_data(current_data)
                    print("✅ Data reset to original!")
                else:
                    print("No original data available.")
                    
            elif clean_choice == '13':
                continue
        
        elif choice == '4':
            # Save Data
            if current_data is None:
                print("\n❌ No data to save! Please load data first.")
                continue
            
            save_menu = {
                '1': 'Save as CSV',
                '2': 'Save as Excel',
                '3': 'Back to Main Menu'
            }
            
            display_menu("SAVE DATA", save_menu)
            save_choice = input("Select option (1-3): ").strip()
            
            if save_choice == '1':
                file_name = input("Enter file name (without .csv): ").strip()
                file_name = file_name if file_name else 'cleaned_data'
                current_data.to_csv(f"{file_name}.csv", index=False)
                print(f"✅ Data saved as {file_name}.csv")
                
            elif save_choice == '2':
                file_name = input("Enter file name (without .xlsx): ").strip()
                file_name = file_name if file_name else 'cleaned_data'
                current_data.to_excel(f"{file_name}.xlsx", index=False)
                print(f"✅ Data saved as {file_name}.xlsx")
                
            elif save_choice == '3':
                continue
        
        elif choice == '5':
            dash_ready_data()
            break
        elif choice == '6':
            print("\n👋 Goodbye!")
            break

        
        else:
            print("\n❌ Invalid choice! Please select 1-6.")

if __name__ == "__main__":
    main()

    