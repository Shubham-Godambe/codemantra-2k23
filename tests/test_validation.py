"""
Unit tests for validation service.
"""

import pytest
from app.services.validation import Validator, ValidationResult


class TestValidationResult:
    """Test ValidationResult class."""
    
    def test_perfect_detection(self):
        """Test when detection matches ground truth."""
        result = ValidationResult(detected_count=50, ground_truth_count=50)
        
        assert result.detected_count == 50
        assert result.ground_truth_count == 50
        assert result.absolute_difference == 0
        assert result.accuracy == 1.0
        assert result.accuracy_percentage == 100.0
    
    def test_half_detection(self):
        """Test when detection is half of ground truth."""
        result = ValidationResult(detected_count=25, ground_truth_count=50)
        
        assert result.absolute_difference == 25
        assert result.accuracy == 0.5
        assert result.accuracy_percentage == 50.0
    
    def test_over_detection(self):
        """Test when detection exceeds ground truth."""
        result = ValidationResult(detected_count=60, ground_truth_count=50)
        
        assert result.absolute_difference == 10
        assert result.accuracy == 0.8
        assert result.accuracy_percentage == 80.0
    
    def test_zero_ground_truth(self):
        """Test handling of zero ground truth."""
        result = ValidationResult(detected_count=10, ground_truth_count=1)
        
        # With ground truth = 1, diff = 9, accuracy = max(0, 1 - 9/1) = 0
        assert result.accuracy == 0.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = ValidationResult(detected_count=45, ground_truth_count=50)
        result_dict = result.to_dict()
        
        assert result_dict['detected_count'] == 45
        assert result_dict['ground_truth_count'] == 50
        assert 'accuracy_percentage' in result_dict


class TestValidator:
    """Test Validator class."""
    
    def test_validate_count_success(self):
        """Test successful validation."""
        result = Validator.validate_count(48, 50)
        
        assert result.detected_count == 48
        assert result.ground_truth_count == 50
        assert result.absolute_difference == 2
    
    def test_validate_count_invalid_ground_truth(self):
        """Test validation with invalid ground truth."""
        with pytest.raises(ValueError):
            Validator.validate_count(50, 0)
        
        with pytest.raises(ValueError):
            Validator.validate_count(50, -1)
    
    def test_validate_count_negative_detected(self):
        """Test validation with negative detected count."""
        with pytest.raises(ValueError):
            Validator.validate_count(-5, 50)
    
    def test_validate_ground_truth_input_valid(self):
        """Test ground truth input validation."""
        value = Validator.validate_ground_truth_input("50")
        assert value == 50
    
    def test_validate_ground_truth_input_invalid(self):
        """Test invalid ground truth input."""
        with pytest.raises(ValueError):
            Validator.validate_ground_truth_input("abc")
        
        with pytest.raises(ValueError):
            Validator.validate_ground_truth_input("-5")
    
    def test_validate_ground_truth_input_zero(self):
        """Test zero ground truth input."""
        value = Validator.validate_ground_truth_input("0")
        assert value == 0


class TestAccuracyCalculations:
    """Test various accuracy calculation scenarios."""
    
    def test_accuracy_scenarios(self):
        """Test various accuracy scenarios."""
        
        # Perfect match
        r1 = ValidationResult(100, 100)
        assert r1.accuracy_percentage == 100.0
        
        # 90% accuracy
        r2 = ValidationResult(90, 100)
        assert r2.accuracy_percentage == 90.0
        
        # 50% accuracy
        r3 = ValidationResult(50, 100)
        assert r3.accuracy_percentage == 50.0
        
        # ~20% accuracy
        r4 = ValidationResult(80, 100)
        assert r4.accuracy_percentage == 80.0
