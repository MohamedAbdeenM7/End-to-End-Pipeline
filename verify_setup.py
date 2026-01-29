"""
Simple verification script to check if all files are in place
"""

import os

print("\n" + "="*70)
print("📋 PROJECT FILE VERIFICATION")
print("="*70 + "\n")

files_to_check = [
    ("data_loader.py", "Data loading module"),
    ("data_overview.py", "Data analysis module"),
    ("data_cleaner.py", "Data cleaning module (ENHANCED)"),
    ("pipeline_orchestrator.py", "Pipeline orchestrator (NEW)"),
    ("main.py", "CLI interface"),
    ("gui.py", "GUI interface"),
    ("final_dash.py", "Basic dashboard"),
    ("enhanced_dashboard.py", "Enhanced dashboard (NEW)"),
    ("quick_start.py", "Quick start script (NEW)"),
    ("test_pipeline.py", "Test suite (NEW)"),
    ("requierments.txt", "Dependencies"),
    ("README.md", "Documentation"),
]

print("Checking files...\n")

all_present = True
for filename, description in files_to_check:
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  ✓ {filename:30s} ({size:,} bytes) - {description}")
    else:
        print(f"  ✗ {filename:30s} - MISSING - {description}")
        all_present = False

print("\n" + "="*70)

if all_present:
    print("✅ All files are present!")
else:
    print("⚠️  Some files are missing!")

print("="*70)

# Check if sample data exists
print("\nSample Data:")
if os.path.exists("cleaned_fordgobike.csv"):
    size = os.path.getsize("cleaned_fordgobike.csv")
    print(f"  ✓ cleaned_fordgobike.csv ({size:,} bytes)")
else:
    print("  ⚠️  cleaned_fordgobike.csv not found (dashboard will use dummy data)")

print("\n" + "="*70)
print("📦 NEXT STEPS:")
print("="*70)
print("\n1. Install dependencies:")
print("   pip install -r requierments.txt")
print("\n2. Run the quick start script:")
print("   python quick_start.py")
print("\n3. Or run individual components:")
print("   - CLI:       python main.py")
print("   - GUI:       python gui.py")
print("   - Dashboard: python enhanced_dashboard.py")
print("\n" + "="*70 + "\n")
