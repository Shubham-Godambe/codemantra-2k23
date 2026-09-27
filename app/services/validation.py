"""
Validation service for ground-truth comparison and accuracy metrics.
Simple count-based validation for MVP.
"""

from typing import Dict, Optional


class ValidationResult:
    """Result of ground-truth validation."""
    
    def __init__(self,
                 detected_count: int,
                 ground_truth_count: int):
        self.detected_count = detected_count
        self.ground_truth_count = ground_truth_count
        self.absolute_difference = abs(detected_count - ground_truth_count)
        
        # Calculate accuracy as: 1 - (abs_diff / ground_truth)
        if ground_truth_count > 0:
            self.accuracy = max(0.0, 1.0 - (self.absolute_difference / ground_truth_count))
        else:
            self.accuracy = 0.0
        
        self.accuracy_percentage = self.accuracy * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'detected_count': self.detected_count,
            'ground_truth_count': self.ground_truth_count,
            'absolute_difference': self.absolute_difference,
            'accuracy': round(self.accuracy, 4),
            'accuracy_percentage': round(self.accuracy_percentage, 2)
        }


class Validator:
    """Validator for comparing detections against ground truth."""
    
    @staticmethod
    def validate_count(detected_count: int, ground_truth_count: int) -> ValidationResult:
        """
        Validate detection count against ground truth.
        
        Note: This is a simple count-based validation.
        For a production system, you would need:
        - Spatial matching of detections to actual trees
        - False positive/negative analysis
        - Precision/recall metrics
        - IoU (Intersection over Union) calculations
        
        This MVP uses simple count comparison.
        
        Args:
            detected_count: Number of trees detected
            ground_truth_count: Actual tree count (from field data)
            
        Returns:
            ValidationResult object
        """
        if ground_truth_count <= 0:
            raise ValueError("Ground truth count must be positive")
        
        if detected_count < 0:
            raise ValueError("Detected count cannot be negative")
        
        return ValidationResult(detected_count, ground_truth_count)
    
    @staticmethod
    def validate_ground_truth_input(value: str) -> int:
        """
        Validate user input for ground truth count.
        
        Args:
            value: String input from user
            
        Returns:
            Integer count
            
        Raises:
            ValueError: If input is invalid
        """
        try:
            count = int(value)
            if count < 0:
                raise ValueError("Tree count cannot be negative")
            return count
        except ValueError as e:
            raise ValueError(f"Invalid ground truth value: {str(e)}")
