"""
Quick Start Script for Data Science Pipeline
This script helps you get started with the pipeline quickly
"""

import os
import sys

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🚀 Data Science Pipeline - Quick Start 🚀             ║
    ║                                                              ║
    ║     End-to-End Data Processing, Analysis & Visualization    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'dash': 'dash',
        'dash_bootstrap_components': 'dash-bootstrap-components',
        'matplotlib': 'matplotlib'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print(f"\n💡 Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        print(f"\n   OR")
        print(f"   pip install -r requierments.txt")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        return True

def show_menu():
    """Display main menu"""
    menu = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                      CHOOSE YOUR INTERFACE                   ║
    ╚══════════════════════════════════════════════════════════════╝
    
    1. 🖥️  Command-Line Interface (CLI)
       Interactive text-based menu for data processing
       → Best for: Quick tasks, automation, scripting
    
    2. 🎨 Graphical User Interface (GUI)
       Desktop application with visual controls
       → Best for: Visual data exploration, drag-and-drop
    
    3. 🌐 Enhanced Web Dashboard
       Modern, interactive web-based analytics dashboard
       → Best for: Data visualization, presentations, sharing
    
    4. 🔧 Pipeline Orchestrator (Code)
       Automated workflow for batch processing
       → Best for: Production pipelines, automation
    
    5. 📚 View Documentation
       Open README and examples
    
    6. ❌ Exit
    
    """
    print(menu)

def run_cli():
    """Run command-line interface"""
    print("\n🖥️  Starting Command-Line Interface...")
    print("=" * 60)
    os.system("python main.py")

def run_gui():
    """Run graphical user interface"""
    print("\n🎨 Starting Graphical User Interface...")
    print("=" * 60)
    try:
        os.system("python gui.py")
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure tkinter is installed (usually comes with Python)")

def run_dashboard():
    """Run enhanced web dashboard"""
    print("\n🌐 Starting Enhanced Web Dashboard...")
    print("=" * 60)
    print("\n📊 Dashboard will open at: http://127.0.0.1:8050/")
    print("   Press Ctrl+C to stop the server\n")
    os.system("python enhanced_dashboard.py")

def run_pipeline_example():
    """Show pipeline orchestrator example"""
    example = """
    ╔══════════════════════════════════════════════════════════════╗
    ║              PIPELINE ORCHESTRATOR EXAMPLE                   ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Here's how to use the Pipeline Orchestrator in your code:
    
    ```python
    from pipeline_orchestrator import DataPipeline
    
    # Create pipeline instance
    pipeline = DataPipeline(verbose=True)
    
    # Run full automated pipeline
    result = pipeline.run_full_pipeline(
        input_path="your_data.csv",
        output_path="cleaned_data.csv",
        clean_config={
            'remove_duplicates': True,
            'handle_nulls': 'fill_mean',
            'remove_outliers': False,
            'standardize_columns': True
        },
        generate_report_file=True
    )
    
    # Check results
    print(f"Success: {result['success']}")
    print(f"Quality Score: {result['quality_score']}")
    print(f"Final Shape: {result['final_shape']}")
    ```
    
    📝 This will:
       1. Load your data
       2. Analyze data quality
       3. Clean the data automatically
       4. Generate a detailed report
       5. Export cleaned data
    
    💡 Try it yourself by creating a Python script with the code above!
    """
    print(example)
    input("\nPress Enter to continue...")

def show_documentation():
    """Show documentation"""
    doc = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                       DOCUMENTATION                          ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📚 Main Documentation: README.md
    
    📁 Key Files:
       • data_loader.py         - Load CSV, Excel, JSON files
       • data_overview.py       - Data analysis and statistics
       • data_cleaner.py        - Advanced data cleaning
       • pipeline_orchestrator.py - Automated workflows
       • enhanced_dashboard.py  - Interactive web dashboard
    
    🎯 Quick Examples:
    
    1. Load and explore data:
       ```python
       from data_loader import DataLoader
       from data_overview import DataOverview
       
       loader = DataLoader()
       data = loader.load_csv("your_file.csv")
       
       overview = DataOverview()
       overview.set_data(data)
       print(overview.overview())
       ```
    
    2. Clean data:
       ```python
       from data_cleaner import DataCleaner
       
       cleaner = DataCleaner(data)
       cleaner.remove_duplicates()
       cleaner.fill_nulls(method='mean')
       cleaned = cleaner.data
       ```
    
    3. Run full pipeline:
       ```python
       from pipeline_orchestrator import DataPipeline
       
       pipeline = DataPipeline()
       result = pipeline.run_full_pipeline("input.csv", "output.csv")
       ```
    
    📖 For more details, see README.md
    """
    print(doc)
    input("\nPress Enter to continue...")

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies before continuing.")
        input("\nPress Enter to exit...")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                run_cli()
            elif choice == '2':
                run_gui()
            elif choice == '3':
                run_dashboard()
            elif choice == '4':
                run_pipeline_example()
            elif choice == '5':
                show_documentation()
            elif choice == '6':
                print("\n👋 Thank you for using the Data Science Pipeline!")
                print("   Made with ❤️  by the abdeen Team\n")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
