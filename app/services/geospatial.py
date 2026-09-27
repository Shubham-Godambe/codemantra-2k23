"""
Geospatial service for GIS and map visualization.
Converts pixel coordinates to geographic coordinates.
Generates GeoJSON representations of detected trees.
"""

import json
import csv
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import numpy as np


class GeoSpatialConverter:
    """
    Converts pixel coordinates to geographic coordinates.
    For MVP without real GPS metadata, uses configurable reference location.
    """
    
    def __init__(self, 
                 image_width_meters: float = 500.0,
                 image_height_meters: float = 500.0,
                 ref_latitude: float = 28.7041,
                 ref_longitude: float = 77.1025):
        """
        Initialize geospatial converter.
        
        Args:
            image_width_meters: Width of image in meters (for pixel->meters conversion)
            image_height_meters: Height of image in meters
            ref_latitude: Reference latitude (demo center, e.g., Delhi)
            ref_longitude: Reference longitude (demo center, e.g., Delhi)
        """
        self.image_width_meters = image_width_meters
        self.image_height_meters = image_height_meters
        self.ref_latitude = ref_latitude
        self.ref_longitude = ref_longitude
        self.pixel_width = 0
        self.pixel_height = 0
        
    def set_image_dimensions(self, pixel_width: int, pixel_height: int) -> None:
        """Set image dimensions in pixels."""
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
    
    def pixel_to_geographic(self, pixel_x: float, pixel_y: float) -> Tuple[float, float]:
        """
        Convert pixel coordinates to geographic coordinates (lat, lon).
        
        Args:
            pixel_x: X position in image (pixels)
            pixel_y: Y position in image (pixels)
            
        Returns:
            Tuple of (latitude, longitude)
        """
        if self.pixel_width == 0 or self.pixel_height == 0:
            raise ValueError("Image dimensions not set")
        
        # Convert pixels to meters relative to image center
        meters_x = (pixel_x - self.pixel_width / 2) * (self.image_width_meters / self.pixel_width)
        meters_y = (pixel_y - self.pixel_height / 2) * (self.image_height_meters / self.pixel_height)
        
        # Convert meters to degrees
        # Approximate: 1 degree latitude ≈ 111 km, 1 degree longitude ≈ 111 km * cos(latitude)
        meters_per_degree_lat = 111000  # meters
        meters_per_degree_lon = 111000 * np.cos(np.radians(self.ref_latitude))
        
        latitude = self.ref_latitude + (meters_y / meters_per_degree_lat)
        longitude = self.ref_longitude + (meters_x / meters_per_degree_lon)
        
        return (latitude, longitude)
    
    def trees_to_geojson(self, trees: List[Dict]) -> Dict:
        """
        Convert detected trees to GeoJSON FeatureCollection.
        
        Args:
            trees: List of tree detection dictionaries
            
        Returns:
            GeoJSON FeatureCollection
        """
        features = []
        
        for tree in trees:
            lat, lon = self.pixel_to_geographic(tree['pixel_x'], tree['pixel_y'])
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # GeoJSON uses [lon, lat]
                },
                "properties": {
                    "tree_id": tree['tree_id'],
                    "pixel_x": round(tree['pixel_x'], 2),
                    "pixel_y": round(tree['pixel_y'], 2),
                    "radius_pixels": round(tree['radius_pixels'], 2),
                    "contour_area_pixels": round(tree['contour_area_pixels'], 2),
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "approximation": "demo_coordinates"
                }
            }
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "properties": {
                "name": "Detected Trees",
                "reference_location": f"Lat: {self.ref_latitude}, Lon: {self.ref_longitude}",
                "image_area_meters": self.image_width_meters * self.image_height_meters,
                "note": "Coordinates are approximate. For demonstration purposes."
            },
            "features": features
        }
        
        return geojson
    
    def save_geojson(self, geojson: Dict, output_path: str) -> None:
        """Save GeoJSON to file."""
        with open(output_path, 'w') as f:
            json.dump(geojson, f, indent=2)
    
    def save_csv(self, trees: List[Dict], output_path: str) -> None:
        """
        Save trees to CSV file.
        
        Args:
            trees: List of tree detections
            output_path: Path to save CSV
        """
        if not trees:
            # Create empty CSV with headers
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['tree_id', 'pixel_x', 'pixel_y', 'estimated_latitude', 
                               'estimated_longitude', 'detected_area_pixels', 'radius_pixels'])
            return
        
        with open(output_path, 'w', newline='') as f:
            fieldnames = ['tree_id', 'pixel_x', 'pixel_y', 'estimated_latitude', 
                         'estimated_longitude', 'detected_area_pixels', 'radius_pixels']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for tree in trees:
                lat, lon = self.pixel_to_geographic(tree['pixel_x'], tree['pixel_y'])
                writer.writerow({
                    'tree_id': tree['tree_id'],
                    'pixel_x': round(tree['pixel_x'], 2),
                    'pixel_y': round(tree['pixel_y'], 2),
                    'estimated_latitude': round(lat, 6),
                    'estimated_longitude': round(lon, 6),
                    'detected_area_pixels': round(tree['contour_area_pixels'], 2),
                    'radius_pixels': round(tree['radius_pixels'], 2)
                })
    
    def load_geojson(self, filepath: str) -> Dict:
        """Load GeoJSON from file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def calculate_tree_density(self, num_trees: int, area_m2: float) -> float:
        """
        Calculate tree density.
        
        Args:
            num_trees: Number of detected trees
            area_m2: Area in square meters
            
        Returns:
            Trees per square meter
        """
        if area_m2 == 0:
            return 0.0
        return num_trees / area_m2
    
    def calculate_tree_density_per_hectare(self, num_trees: int, area_m2: float) -> float:
        """Calculate trees per hectare (10,000 m²)."""
        if area_m2 == 0:
            return 0.0
        return (num_trees / area_m2) * 10000
