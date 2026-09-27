"""
Tree detection route handler.
Handles image processing and tree detection.
"""

import os
import json
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.tree_detector import TreeDetector, TreeDetectionResult
from app.services.geospatial import GeoSpatialConverter
import cv2

router = APIRouter(prefix="/api", tags=["detection"])

RESULTS_DIR = "data/results"
UPLOAD_DIR = "data/uploads"

# Store results in memory (for MVP)
_detection_results = {}
_result_counter = 0


@router.post("/detect")
async def detect_trees(
    image_path: str = Query(...),
    min_tree_area: int = Query(50),
    max_tree_area: int = Query(10000),
    circularity: float = Query(0.5),
    image_width_m: float = Query(500.0),
    image_height_m: float = Query(500.0)
):
    """
    Run tree detection on uploaded image.
    
    Args:
        image_path: Path to uploaded image
        min_tree_area: Minimum tree area (pixels)
        max_tree_area: Maximum tree area (pixels)
        circularity: Minimum circularity threshold (0-1)
        image_width_m: Image width in meters (for density calculation)
        image_height_m: Image height in meters
    """
    
    # Validate image exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        # Initialize detector with parameters
        detector = TreeDetector(
            min_tree_area=max(10, min_tree_area),
            max_tree_area=min(50000, max_tree_area),
            circularity_threshold=max(0.0, min(1.0, circularity))
        )
        
        # Run detection
        detection_result = detector.detect_trees(image_path)
        
        # Set geospatial parameters
        geo_converter = GeoSpatialConverter(
            image_width_meters=image_width_m,
            image_height_meters=image_height_m
        )
        geo_converter.set_image_dimensions(
            detection_result.image_shape[0],
            detection_result.image_shape[1]
        )
        
        # Calculate density
        area_m2 = image_width_m * image_height_m
        tree_density_per_m2 = geo_converter.calculate_tree_density(detection_result.total_trees, area_m2)
        tree_density_per_hectare = geo_converter.calculate_tree_density_per_hectare(detection_result.total_trees, area_m2)
        
        # Create results directory
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        # Save processed image
        result_id = len(_detection_results) + 1
        processed_image_path = os.path.join(RESULTS_DIR, f"result_{result_id}_detected.jpg")
        detector.save_detection_image(detection_result.processed_image, processed_image_path)
        
        # Save binary mask
        mask_path = os.path.join(RESULTS_DIR, f"result_{result_id}_mask.jpg")
        detector.save_binary_mask(detection_result.binary_mask, mask_path)
        
        # Generate and save GeoJSON
        geojson = geo_converter.trees_to_geojson(detection_result.trees)
        geojson_path = os.path.join(RESULTS_DIR, f"result_{result_id}_trees.geojson")
        geo_converter.save_geojson(geojson, geojson_path)
        
        # Generate and save CSV
        csv_path = os.path.join(RESULTS_DIR, f"result_{result_id}_trees.csv")
        geo_converter.save_csv(detection_result.trees, csv_path)
        
        # Store in memory
        _detection_results[result_id] = {
            'detection_result': detection_result,
            'geo_converter': geo_converter,
            'image_path': image_path,
            'processed_image_path': processed_image_path,
            'geojson_path': geojson_path,
            'csv_path': csv_path,
            'area_m2': area_m2,
            'tree_density_per_m2': tree_density_per_m2,
            'tree_density_per_hectare': tree_density_per_hectare
        }
        
        return {
            'status': 'success',
            'result_id': result_id,
            'total_trees': detection_result.total_trees,
            'image_dimensions': detection_result.image_shape,
            'image_area_pixels': detection_result.image_area_pixels,
            'area_m2': area_m2,
            'tree_density_per_m2': round(tree_density_per_m2, 6),
            'tree_density_per_hectare': round(tree_density_per_hectare, 2),
            'average_tree_area_pixels': round(detection_result.average_tree_area, 2),
            'min_tree_area_pixels': round(detection_result.min_tree_area, 2),
            'max_tree_area_pixels': round(detection_result.max_tree_area, 2),
            'processed_image': processed_image_path,
            'message': 'Trees detected successfully'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


@router.get("/results/{result_id}")
async def get_results(result_id: int):
    """Get detection results by ID."""
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    result_data = _detection_results[result_id]
    detection_result = result_data['detection_result']
    
    return {
        'status': 'success',
        'result_id': result_id,
        'total_trees': detection_result.total_trees,
        'trees': detection_result.trees,
        'image_dimensions': detection_result.image_shape,
        'image_area_pixels': detection_result.image_area_pixels,
        'area_m2': result_data['area_m2'],
        'average_tree_area_pixels': round(detection_result.average_tree_area, 2),
        'tree_density_per_m2': round(result_data['tree_density_per_m2'], 6),
        'tree_density_per_hectare': round(result_data['tree_density_per_hectare'], 2),
        'detection_parameters': detection_result.detection_parameters
    }


@router.get("/results/{result_id}/geojson")
async def download_geojson(result_id: int):
    """Download GeoJSON file."""
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    geojson_path = _detection_results[result_id]['geojson_path']
    
    if not os.path.exists(geojson_path):
        raise HTTPException(status_code=404, detail="GeoJSON file not found")
    
    return FileResponse(geojson_path, filename=f"trees_{result_id}.geojson")


@router.get("/results/{result_id}/csv")
async def download_csv(result_id: int):
    """Download CSV file."""
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    csv_path = _detection_results[result_id]['csv_path']
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    return FileResponse(csv_path, filename=f"trees_{result_id}.csv")


@router.get("/results/{result_id}/image")
async def get_processed_image(result_id: int):
    """Get processed detection image."""
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    image_path = _detection_results[result_id]['processed_image_path']
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path, media_type="image/jpeg")
