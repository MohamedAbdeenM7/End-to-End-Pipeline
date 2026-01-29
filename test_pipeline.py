"""
Test Suite for Data Science Pipeline
Run this to verify all components are working correctly
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)
    
    modules = [
        ('data_loader', 'DataLoader'),
        ('data_overview', 'DataOverview'),
        ('data_cleaner', 'DataCleaner'),
        ('pipeline_orchestrator', 'DataPipeline')
    ]
    
    all_passed = True
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"  ✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ✗ {module_name}.{class_name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_data_loader():
    """Test DataLoader functionality"""
    print("\n" + "="*60)
    print("TEST 2: DataLoader")
    print("="*60)
    
    try:
        from data_loader import DataLoader
        import pandas as pd
        import tempfile
        import os
        
        # Create temporary test CSV
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        test_data.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        # Test loading
        loader = DataLoader()
        loaded_data = loader.load_csv(temp_file.name)
        
        # Cleanup
        os.unlink(temp_file.name)
        
        if loaded_data is not None and len(loaded_data) == 5:
            print("  ✓ CSV loading works")
            print(f"    Loaded {len(loaded_data)} rows, {len(loaded_data.columns)} columns")
            return True
        else:
            print("  ✗ CSV loading failed")
            return False
            
    except Exception as e:
        print(f"  ✗ DataLoader test failed: {e}")
        return False

def test_data_overview():
    """Test DataOverview functionality"""
    print("\n" + "="*60)
    print("TEST 3: DataOverview")
    print("="*60)
    
    try:
        from data_overview import DataOverview
        import pandas as pd
        import numpy as np
        
        # Create test data
        test_data = pd.DataFrame({
            'numeric': [1, 2, 3, 4, 5, 5],  # Has duplicate
            'text': ['a', 'b', 'c', 'd', 'e', 'a'],
            'with_null': [1, 2, None, 4, 5, 6]
        })
        
        overview = DataOverview()
        overview.set_data(test_data)
        
        # Test methods
        tests_passed = 0
        total_tests = 5
        
        # Test shape
        if overview.shape() == (6, 3):
            print("  ✓ shape() works")
            tests_passed += 1
        else:
            print("  ✗ shape() failed")
        
        # Test sample
        sample = overview.sample(n=3)
        if sample is not None and len(sample) == 3:
            print("  ✓ sample() works")
            tests_passed += 1
        else:
            print("  ✗ sample() failed")
        
        # Test duplicates
        dup = overview.duplicates()
        if dup is not None:
            print("  ✓ duplicates() works")
            tests_passed += 1
        else:
            print("  ✗ duplicates() failed")
        
        # Test overview
        ov = overview.overview()
        if ov is not None and len(ov) == 3:
            print("  ✓ overview() works")
            tests_passed += 1
        else:
            print("  ✗ overview() failed")
        
        # Test stats
        stats = overview.get_stats(numeric=True)
        if stats is not None:
            print("  ✓ get_stats() works")
            tests_passed += 1
        else:
            print("  ✗ get_stats() failed")
        
        print(f"\n  Passed {tests_passed}/{total_tests} tests")
        return tests_passed == total_tests
        
    except Exception as e:
        print(f"  ✗ DataOverview test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_cleaner():
    """Test DataCleaner functionality"""
    print("\n" + "="*60)
    print("TEST 4: DataCleaner")
    print("="*60)
    
    try:
        from data_cleaner import DataCleaner
        import pandas as pd
        import numpy as np
        
        # Create test data
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 5, None],
            'B': ['a', 'b', 'c', 'd', 'e', 'a', 'f'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5, 100.0, 6.6]  # 100.0 is outlier
        })
        
        cleaner = DataCleaner(test_data.copy())
        
        tests_passed = 0
        total_tests = 6
        
        # Test remove_duplicates
        cleaner_dup = DataCleaner(test_data.copy())
        before = len(cleaner_dup.data)
        cleaner_dup.remove_duplicates()
        after = len(cleaner_dup.data)
        if after < before:
            print("  ✓ remove_duplicates() works")
            tests_passed += 1
        else:
            print("  ✗ remove_duplicates() failed")
        
        # Test remove_nulls
        cleaner_null = DataCleaner(test_data.copy())
        before = len(cleaner_null.data)
        cleaner_null.remove_nulls()
        after = len(cleaner_null.data)
        if after < before:
            print("  ✓ remove_nulls() works")
            tests_passed += 1
        else:
            print("  ✗ remove_nulls() failed")
        
        # Test fill_nulls
        cleaner_fill = DataCleaner(test_data.copy())
        cleaner_fill.fill_nulls(value=0)
        if cleaner_fill.data.isnull().sum().sum() == 0:
            print("  ✓ fill_nulls() works")
            tests_passed += 1
        else:
            print("  ✗ fill_nulls() failed")
        
        # Test standardize_column_names
        test_cols = pd.DataFrame({'Column Name': [1, 2], 'Another-Column': [3, 4]})
        cleaner_cols = DataCleaner(test_cols)
        cleaner_cols.standardize_column_names()
        if 'column_name' in cleaner_cols.data.columns:
            print("  ✓ standardize_column_names() works")
            tests_passed += 1
        else:
            print("  ✗ standardize_column_names() failed")
        
        # Test rename_columns
        cleaner_rename = DataCleaner(test_data.copy())
        cleaner_rename.rename_columns({'A': 'Column_A'})
        if 'Column_A' in cleaner_rename.data.columns:
            print("  ✓ rename_columns() works")
            tests_passed += 1
        else:
            print("  ✗ rename_columns() failed")
        
        # Test get_cleaning_report
        report = cleaner.get_cleaning_report()
        if report is not None and 'original_shape' in report:
            print("  ✓ get_cleaning_report() works")
            tests_passed += 1
        else:
            print("  ✗ get_cleaning_report() failed")
        
        print(f"\n  Passed {tests_passed}/{total_tests} tests")
        return tests_passed == total_tests
        
    except Exception as e:
        print(f"  ✗ DataCleaner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline():
    """Test Pipeline Orchestrator"""
    print("\n" + "="*60)
    print("TEST 5: Pipeline Orchestrator")
    print("="*60)
    
    try:
        from pipeline_orchestrator import DataPipeline
        import pandas as pd
        import tempfile
        import os
        
        # Create temporary test CSV
        test_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 5],
            'B': ['a', 'b', 'c', 'd', 'e', 'a'],
            'C': [1.1, 2.2, None, 4.4, 5.5, 6.6]
        })
        
        temp_input = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        test_data.to_csv(temp_input.name, index=False)
        temp_input.close()
        
        temp_output = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_output.close()
        
        # Test pipeline
        pipeline = DataPipeline(verbose=False)
        
        tests_passed = 0
        total_tests = 3
        
        # Test load_data
        if pipeline.load_data(temp_input.name) is not None:
            print("  ✓ load_data() works")
            tests_passed += 1
        else:
            print("  ✗ load_data() failed")
        
        # Test analyze_data_quality
        quality = pipeline.analyze_data_quality()
        if quality is not None and 'quality_score' in quality:
            print("  ✓ analyze_data_quality() works")
            tests_passed += 1
        else:
            print("  ✗ analyze_data_quality() failed")
        
        # Test auto_clean
        cleaned = pipeline.auto_clean(remove_duplicates=True, handle_nulls='drop')
        if cleaned is not None:
            print("  ✓ auto_clean() works")
            tests_passed += 1
        else:
            print("  ✗ auto_clean() failed")
        
        # Cleanup
        os.unlink(temp_input.name)
        if os.path.exists(temp_output.name):
            os.unlink(temp_output.name)
        
        print(f"\n  Passed {tests_passed}/{total_tests} tests")
        return tests_passed == total_tests
        
    except Exception as e:
        print(f"  ✗ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 DATA SCIENCE PIPELINE - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Module Imports", test_imports()))
    results.append(("DataLoader", test_data_loader()))
    results.append(("DataOverview", test_data_overview()))
    results.append(("DataCleaner", test_data_cleaner()))
    results.append(("Pipeline Orchestrator", test_pipeline()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your pipeline is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
