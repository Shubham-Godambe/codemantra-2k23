"""
OpenCV-based tree detection service.
Classical computer vision approach for tree enumeration from aerial imagery.
Not a deep learning model - uses vegetation segmentation and blob detection.
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import json


class TreeDetectionResult:
    """Result object for tree detection."""
    
    def __init__(self):
        self.trees: List[Dict] = []
        self.total_trees: int = 0
        self.processed_image: Optional[np.ndarray] = None
        self.binary_mask: Optional[np.ndarray] = None
        self.image_shape: Tuple[int, int] = (0, 0)
        self.image_area_pixels: float = 0.0
        self.average_tree_area: float = 0.0
        self.min_tree_area: float = 0.0
        self.max_tree_area: float = 0.0
        self.detection_parameters: Dict = {}
        
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            'total_trees': self.total_trees,
            'trees': self.trees,
            'image_shape': self.image_shape,
            'image_area_pixels': self.image_area_pixels,
            'average_tree_area': self.average_tree_area,
            'min_tree_area': self.min_tree_area,
            'max_tree_area': self.max_tree_area,
            'detection_parameters': self.detection_parameters
        }


class TreeDetector:
    """
    OpenCV-based tree detector.
    Uses classical computer vision techniques:
    - HSV color space for vegetation detection
    - Morphological operations for noise reduction
    - Contour detection for tree identification
    """
    
    def __init__(self,
                 min_tree_area: int = 50,
                 max_tree_area: int = 10000,
                 vegetation_lower_h: int = 35,
                 vegetation_upper_h: int = 85,
                 vegetation_lower_s: int = 40,
                 vegetation_upper_s: int = 255,
                 vegetation_lower_v: int = 40,
                 vegetation_upper_v: int = 255,
                 circularity_threshold: float = 0.5):
        """
        Initialize tree detector.
        
        Args:
            min_tree_area: Minimum object area (pixels) to consider as tree
            max_tree_area: Maximum object area (pixels) to consider as tree
            vegetation_lower_h, vegetation_upper_h: HSV Hue range for greenery
            vegetation_lower_s, vegetation_upper_s: HSV Saturation range
            vegetation_lower_v, vegetation_upper_v: HSV Value range
            circularity_threshold: Minimum circularity (0-1) for shape filtering
        """
        self.min_tree_area = min_tree_area
        self.max_tree_area = max_tree_area
        self.vegetation_lower = np.array([vegetation_lower_h, vegetation_lower_s, vegetation_lower_v])
        self.vegetation_upper = np.array([vegetation_upper_h, vegetation_upper_s, vegetation_upper_v])
        self.circularity_threshold = circularity_threshold
        
    def detect_trees(self, image_path: str, resize_width: int = 1024) -> TreeDetectionResult:
        """
        Detect trees in an aerial image.
        
        Args:
            image_path: Path to aerial image file
            resize_width: Width to resize image to (for performance)
            
        Returns:
            TreeDetectionResult object with detection results
        """
        result = TreeDetectionResult()
        
        # Load image
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")
        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")
        
        original_shape = image.shape
        result.image_shape = (original_shape[1], original_shape[0])  # (width, height)
        result.image_area_pixels = result.image_shape[0] * result.image_shape[1]
        
        # Resize for faster processing
        scale = resize_width / image.shape[1]
        resized_image = cv2.resize(image, (resize_width, int(image.shape[0] * scale)))
        
        # Step 1: Convert BGR to HSV
        hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
        
        # Step 2: Create vegetation mask using HSV thresholding
        # Looking for green colors (vegetation)
        vegetation_mask = cv2.inRange(hsv, self.vegetation_lower, self.vegetation_upper)
        
        # Step 3: Apply morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        vegetation_mask = cv2.morphologyEx(vegetation_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        vegetation_mask = cv2.morphologyEx(vegetation_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Step 4: Apply Gaussian blur for smoothing
        blurred = cv2.GaussianBlur(vegetation_mask, (7, 7), 0)
        
        # Step 5: Find contours
        contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Scale factor for converting back to original image coordinates
        scale_factor = 1.0 / scale
        
        # Step 6: Filter contours by area and shape
        result.detection_parameters = {
            'min_tree_area': self.min_tree_area,
            'max_tree_area': self.max_tree_area,
            'vegetation_threshold': str(self.vegetation_lower) + ' to ' + str(self.vegetation_upper),
            'circularity_threshold': self.circularity_threshold,
            'resize_width': resize_width,
            'scale_factor': scale_factor
        }
        
        trees = []
        tree_areas = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < self.min_tree_area or area > self.max_tree_area:
                continue
            
            # Calculate circularity as a shape filter
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter ** 2)
            
            # Filter by circularity (trees should be roughly circular)
            if circularity < self.circularity_threshold:
                continue
            
            # Fit circle
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            # Scale back to original image coordinates
            x_original = x * scale_factor
            y_original = y * scale_factor
            radius_original = radius * scale_factor
            
            trees.append({
                'tree_id': len(trees) + 1,
                'pixel_x': float(x_original),
                'pixel_y': float(y_original),
                'radius_pixels': float(radius_original),
                'contour_area_pixels': float(area * (scale_factor ** 2)),
                'circularity': float(circularity),
                'center': (float(x_original), float(y_original))
            })
            
            tree_areas.append(area * (scale_factor ** 2))
        
        result.trees = trees
        result.total_trees = len(trees)
        
        if tree_areas:
            result.average_tree_area = float(np.mean(tree_areas))
            result.min_tree_area = float(np.min(tree_areas))
            result.max_tree_area = float(np.max(tree_areas))
        
        # Generate visualization
        result.processed_image = self._draw_detections(image, trees, scale_factor)
        result.binary_mask = vegetation_mask
        
        return result
    
    def _draw_detections(self, image: np.ndarray, trees: List[Dict], scale_factor: float) -> np.ndarray:
        """Draw detected trees on image."""
        result_image = image.copy()
        
        for tree in trees:
            x = int(tree['pixel_x'])
            y = int(tree['pixel_y'])
            radius = int(tree['radius_pixels'])
            tree_id = tree['tree_id']
            
            # Draw circle
            cv2.circle(result_image, (x, y), radius, (0, 255, 0), 2)
            
            # Add tree ID label
            cv2.putText(result_image, f"T{tree_id}", (x - 15, y - radius - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return result_image
    
    def save_detection_image(self, processed_image: np.ndarray, output_path: str) -> None:
        """Save processed image with detections."""
        cv2.imwrite(output_path, processed_image)
    
    def save_binary_mask(self, binary_mask: np.ndarray, output_path: str) -> None:
        """Save binary vegetation mask."""
        cv2.imwrite(output_path, binary_mask)
