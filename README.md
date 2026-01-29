# 🚀 End-to-End Data Science Pipeline

A comprehensive, production-ready data science pipeline for loading, analyzing, cleaning, and visualizing data with multiple interfaces (CLI, GUI, and Web Dashboard).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-green.svg)
![Dash](https://img.shields.io/badge/Dash-2.9+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔧 Core Capabilities
- **Multi-format Data Loading**: Support for CSV, Excel, and JSON files
- **Automated Data Quality Analysis**: Comprehensive quality scoring and reporting
- **Advanced Data Cleaning**: 
  - Remove/fill null values with multiple strategies (mean, median, mode, forward/backward fill)
  - Duplicate detection and removal
  - Outlier detection and removal (IQR and Z-score methods)
  - Automatic data type inference
  - Text cleaning and standardization
  - Column name standardization
- **Statistical Analysis**: Detailed statistics for numeric, categorical, and datetime columns
- **Data Visualization**: Interactive charts and dashboards

### 🖥️ Multiple Interfaces
1. **Command-Line Interface (CLI)** - `main.py`
2. **Graphical User Interface (GUI)** - `gui.py` (Tkinter-based)
3. **Web Dashboard** - `enhanced_dashboard.py` (Modern, interactive Plotly Dash)
4. **Pipeline Orchestrator** - `pipeline_orchestrator.py` (Automated workflow)

## 📁 Project Structure

```
End-to-End-Pipeline/
├── data_loader.py              # Data loading module (CSV, Excel, JSON)
├── data_overview.py            # Data analysis and statistics
├── data_cleaner.py             # Data cleaning and transformation
├── pipeline_orchestrator.py    # Automated pipeline workflow
├── main.py                     # CLI interface
├── gui.py                      # GUI interface (Tkinter)
├── final_dash.py              # Basic Dash dashboard
├── enhanced_dashboard.py       # Advanced Dash dashboard (NEW!)
├── requierments.txt           # Python dependencies
├── README.md                   # This file
├── cleaned_fordgobike.csv     # Sample dataset
└── Digram/                    # Project diagrams
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd End-to-End-Pipeline
```

2. **Install dependencies**
```bash
pip install -r requierments.txt
```

### Usage

#### Option 1: Command-Line Interface (CLI)
```bash
python main.py
```
Interactive menu for:
- Loading data from various sources
- Viewing data overview and statistics
- Cleaning data with multiple options
- Saving processed data

#### Option 2: Graphical User Interface (GUI)
```bash
python gui.py
```
Features:
- Drag-and-drop file loading
- Visual data preview
- Interactive cleaning options
- Statistical visualizations
- Export functionality

#### Option 3: Enhanced Web Dashboard
```bash
python enhanced_dashboard.py
```
Access at: `http://127.0.0.1:8050/`

Features:
- 🎨 Modern dark mode design
- 📊 Real-time interactive charts
- 🔍 Advanced filtering (date range, user type, gender, age group)
- 📈 KPI cards with key metrics
- 🗺️ Interactive map visualizations
- 📉 Multiple chart types (line, bar, pie, box plots, histograms)

#### Option 4: Automated Pipeline
```python
from pipeline_orchestrator import DataPipeline

# Create pipeline
pipeline = DataPipeline(verbose=True)

# Run full pipeline
result = pipeline.run_full_pipeline(
    input_path="your_data.csv",
    output_path="cleaned_data.csv",
    clean_config={
        'remove_duplicates': True,
        'handle_nulls': 'fill_mean',
        'remove_outliers': False,
        'standardize_columns': True
    }
)
```

## 📊 Module Documentation

### 1. DataLoader (`data_loader.py`)
Handles loading data from multiple file formats.

**Methods:**
- `load_csv(file_path)` - Load CSV files
- `load_excel(file_path, sheet_name=0)` - Load Excel files
- `load_json(file_path)` - Load JSON files

### 2. DataOverview (`data_overview.py`)
Provides comprehensive data analysis and statistics.

**Methods:**
- `shape(data)` - Get dataset dimensions
- `sample(data, n=5)` - View first n rows
- `duplicates(data)` - Detect duplicate rows
- `outliers(data)` - Identify outliers using IQR method
- `get_stats(data, numeric, categorical, datetime)` - Get detailed statistics
- `overview(data)` - Comprehensive column-wise overview

### 3. DataCleaner (`data_cleaner.py`)
Advanced data cleaning and transformation capabilities.

**Methods:**
- `remove_nulls(columns, threshold)` - Remove rows with null values
- `fill_nulls(value, columns, method)` - Fill nulls with value or statistical method
- `remove_duplicates(subset, keep)` - Remove duplicate rows
- `fix_column_types(column_type_map)` - Convert column data types
- `rename_columns(column_map)` - Rename columns
- `remove_outliers(columns, method, threshold)` - Remove statistical outliers
- `drop_columns(columns)` - Drop specified columns
- `infer_dtypes()` - Automatically infer and convert data types
- `clean_text_columns(columns, lowercase, remove_special)` - Clean text data
- `standardize_column_names()` - Standardize column naming
- `get_cleaning_report()` - Get detailed cleaning report

### 4. DataPipeline (`pipeline_orchestrator.py`)
Orchestrates the complete data processing workflow.

**Methods:**
- `load_data(file_path, file_type)` - Load data with auto-detection
- `analyze_data_quality()` - Comprehensive quality analysis
- `auto_clean(config)` - Automated cleaning with best practices
- `generate_report(output_path)` - Generate detailed text report
- `export_data(output_path, file_type)` - Export processed data
- `run_full_pipeline(input_path, output_path, clean_config)` - Complete workflow

## 🎯 Use Cases

### 1. Quick Data Exploration
```python
from data_loader import DataLoader
from data_overview import DataOverview

loader = DataLoader()
data = loader.load_csv("your_data.csv")

overview = DataOverview()
overview.set_data(data)

print(overview.overview())
print(overview.get_stats(numeric=True))
```

### 2. Data Cleaning Workflow
```python
from data_cleaner import DataCleaner

cleaner = DataCleaner(data)
cleaner.standardize_column_names()
cleaner.remove_duplicates()
cleaner.fill_nulls(method='mean')
cleaner.remove_outliers(method='iqr')

cleaned_data = cleaner.data
report = cleaner.get_cleaning_report()
```

### 3. Automated Pipeline
```python
from pipeline_orchestrator import DataPipeline

pipeline = DataPipeline()
result = pipeline.run_full_pipeline(
    input_path="raw_data.csv",
    output_path="cleaned_data.csv"
)
```

## 📈 Dashboard Features

The **Enhanced Dashboard** (`enhanced_dashboard.py`) provides:

### Visualizations
1. **KPI Cards**: Total trips, average duration, active users, popular station
2. **Trips by Day of Week**: Line chart with area fill
3. **Trips by Hour**: Colorful bar chart showing hourly patterns
4. **Age Distribution**: Histogram of user ages
5. **Gender Distribution**: Pie chart with donut style
6. **Trip Duration by User Type**: Box plots comparing subscribers vs customers
7. **User Type Trends**: Line chart showing trends over time
8. **Station Activity Map**: Interactive map with bubble sizes
9. **Top 10 Start Stations**: Horizontal bar chart

### Filters
- Date range picker
- User type multi-select
- Gender multi-select
- Age group checkboxes
- Reset filters button

## 🛠️ Advanced Configuration

### Cleaning Configuration Options
```python
clean_config = {
    'remove_duplicates': True,           # Remove duplicate rows
    'handle_nulls': 'fill_mean',        # 'drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_zero'
    'remove_outliers': True,            # Remove statistical outliers
    'standardize_columns': True         # Standardize column names
}
```

### Null Handling Strategies
- `'drop'` - Remove rows with null values
- `'fill_mean'` - Fill with column mean (numeric only)
- `'fill_median'` - Fill with column median (numeric only)
- `'fill_mode'` - Fill with most common value
- `'fill_zero'` - Fill with zero

### Outlier Detection Methods
- `'iqr'` - Interquartile Range method (default threshold: 1.5)
- `'zscore'` - Z-score method (default threshold: 3)

## 📝 Sample Data

The project includes a sample Ford GoBike dataset (`cleaned_fordgobike.csv`) with:
- Trip information (ID, duration, timestamps)
- Station data (names, coordinates)
- User demographics (type, gender, age)
- Temporal features (day of week, month, hour)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

 Team - Final Project



