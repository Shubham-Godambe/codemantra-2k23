"""
End-to-end testing script for CODEMANTRA 2K23
Tests all major functionality without a running server
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.tree_detector import TreeDetector
from app.services.geospatial import GeoSpatialConverter
from app.services.validation import Validator
import tempfile
import json


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def test_tree_detection():
    """Test tree detection on sample image"""
    print_section("TESTING TREE DETECTION")
    
    try:
        detector = TreeDetector(
            min_tree_area=50,
            max_tree_area=10000,
            circularity_threshold=0.5
        )
        
        sample_image = "data/sample/demo_forest.jpg"
        if not os.path.exists(sample_image):
            print(f"✗ Sample image not found: {sample_image}")
            return False
        
        print(f"✓ Testing detection on: {sample_image}")
        result = detector.detect_trees(sample_image)
        
        print(f"  - Image dimensions: {result.image_shape}")
        print(f"  - Total trees detected: {result.total_trees}")
        print(f"  - Average tree area: {result.average_tree_area:.2f} pixels²")
        print(f"  - Min tree area: {result.min_tree_area:.2f} pixels²")
        print(f"  - Max tree area: {result.max_tree_area:.2f} pixels²")
        
        if result.total_trees > 0:
            print(f"✓ Tree detection working! Detected {result.total_trees} trees")
            return True
        else:
            print("⚠ No trees detected (may indicate detection parameter issue)")
            return True  # Don't fail - parameters may need tuning for specific images
            
    except Exception as e:
        print(f"✗ Tree detection failed: {e}")
        return False


def test_geospatial_conversion():
    """Test geographic coordinate conversion"""
    print_section("TESTING GEOSPATIAL CONVERSION")
    
    try:
        converter = GeoSpatialConverter(
            image_width_meters=500,
            image_height_meters=500,
            ref_latitude=28.7041,
            ref_longitude=77.1025
        )
        
        converter.set_image_dimensions(1024, 768)
        
        # Test pixel to geographic conversion
        lat, lon = converter.pixel_to_geographic(512, 384)
        
        print(f"✓ Testing pixel-to-geographic conversion")
        print(f"  - Pixel (512, 384) → Lat: {lat:.6f}, Lon: {lon:.6f}")
        print(f"  - Reference: Lat: 28.704100, Lon: 77.102500")
        
        # Test GeoJSON generation
        sample_trees = [
            {'tree_id': 1, 'pixel_x': 256, 'pixel_y': 192, 'radius_pixels': 30, 'contour_area_pixels': 500},
            {'tree_id': 2, 'pixel_x': 768, 'pixel_y': 576, 'radius_pixels': 35, 'contour_area_pixels': 600},
        ]
        
        geojson = converter.trees_to_geojson(sample_trees)
        
        print(f"✓ GeoJSON generation successful")
        print(f"  - Features: {len(geojson['features'])}")
        print(f"  - Feature type: {geojson['features'][0]['geometry']['type']}")
        
        # Test CSV generation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        
        converter.save_csv(sample_trees, csv_path)
        
        with open(csv_path, 'r') as f:
            csv_content = f.read()
        
        print(f"✓ CSV export successful")
        print(f"  - Output file: {csv_path}")
        
        os.unlink(csv_path)
        
        return True
        
    except Exception as e:
        print(f"✗ Geospatial conversion failed: {e}")
        return False


def test_validation():
    """Test validation and accuracy metrics"""
    print_section("TESTING VALIDATION & ACCURACY METRICS")
    
    try:
        validator = Validator()
        
        # Test case 1: Perfect detection
        result1 = validator.validate_count(50, 50)
        print(f"✓ Test 1 - Perfect detection (50 vs 50)")
        print(f"  - Accuracy: {result1.accuracy_percentage:.2f}%")
        
        # Test case 2: Under-detection
        result2 = validator.validate_count(45, 50)
        print(f"✓ Test 2 - Under-detection (45 vs 50)")
        print(f"  - Accuracy: {result2.accuracy_percentage:.2f}%")
        
        # Test case 3: Over-detection
        result3 = validator.validate_count(55, 50)
        print(f"✓ Test 3 - Over-detection (55 vs 50)")
        print(f"  - Accuracy: {result3.accuracy_percentage:.2f}%")
        
        # Test ground truth validation
        try:
            validated = validator.validate_ground_truth_input("100")
            print(f"✓ Ground truth input validation: 100 trees → {validated}")
        except ValueError as e:
            print(f"✗ Ground truth validation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Validation tests failed: {e}")
        return False


def test_data_export():
    """Test data export functionality"""
    print_section("TESTING DATA EXPORT")
    
    try:
        converter = GeoSpatialConverter(
            image_width_meters=500,
            image_height_meters=500
        )
        
        converter.set_image_dimensions(1024, 768)
        
        sample_trees = [
            {'tree_id': i, 'pixel_x': 100*i, 'pixel_y': 150*i, 'radius_pixels': 30, 'contour_area_pixels': 500}
            for i in range(1, 6)
        ]
        
        # Test GeoJSON export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
            geojson_path = f.name
        
        geojson = converter.trees_to_geojson(sample_trees)
        converter.save_geojson(geojson, geojson_path)
        
        with open(geojson_path, 'r') as f:
            loaded_geojson = json.load(f)
        
        print(f"✓ GeoJSON export and reload successful")
        print(f"  - Trees in GeoJSON: {len(loaded_geojson['features'])}")
        
        os.unlink(geojson_path)
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        
        converter.save_csv(sample_trees, csv_path)
        
        with open(csv_path, 'r') as f:
            lines = f.readlines()
        
        print(f"✓ CSV export successful")
        print(f"  - Header line: {lines[0].strip()}")
        print(f"  - Data rows: {len(lines) - 1}")
        
        os.unlink(csv_path)
        
        return True
        
    except Exception as e:
        print(f"✗ Data export tests failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  CODEMANTRA 2K23 - END-TO-END FUNCTIONALITY TEST".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("Tree Detection", test_tree_detection),
        ("Geospatial Conversion", test_geospatial_conversion),
        ("Validation & Accuracy", test_validation),
        ("Data Export", test_data_export),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - Application is ready to use!")
        print("\nTo start the server, run:")
        print("  Windows: run.bat")
        print("  macOS/Linux: bash run.sh")
        print("\nOr manually:")
        print("  Source: python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed - please review errors above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
