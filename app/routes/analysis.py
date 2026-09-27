"""
Analysis route handler.
Handles validation and basic analysis.
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.validation import Validator
from app.routes.detection import _detection_results

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/validate")
async def validate_detection(
    result_id: int = Query(...),
    ground_truth_count: int = Query(...)
):
    """
    Validate detection against ground truth count.
    
    Args:
        result_id: Detection result ID
        ground_truth_count: Actual tree count from field data
    """
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    try:
        detection_count = _detection_results[result_id]['detection_result'].total_trees
        
        validator = Validator()
        validation_result = validator.validate_count(detection_count, ground_truth_count)
        
        return {
            'status': 'success',
            'result_id': result_id,
            'detected_count': validation_result.detected_count,
            'ground_truth_count': validation_result.ground_truth_count,
            'absolute_difference': validation_result.absolute_difference,
            'accuracy': validation_result.accuracy,
            'accuracy_percentage': validation_result.accuracy_percentage,
            'note': 'Simple count-based validation. Production systems would include spatial matching and IoU metrics.'
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/analysis/{result_id}")
async def get_analysis(result_id: int):
    """Get analysis metrics for detection result."""
    
    if result_id not in _detection_results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    result_data = _detection_results[result_id]
    detection_result = result_data['detection_result']
    
    return {
        'status': 'success',
        'result_id': result_id,
        'total_trees': detection_result.total_trees,
        'estimated_area_m2': result_data['area_m2'],
        'estimated_tree_density':  {
            'trees_per_m2': round(result_data['tree_density_per_m2'], 6),
            'trees_per_hectare': round(result_data['tree_density_per_hectare'], 2)
        },
        'crown_area_statistics': {
            'average_pixels': round(detection_result.average_tree_area, 2),
            'min_pixels': round(detection_result.min_tree_area, 2),
            'max_pixels': round(detection_result.max_tree_area, 2)
        },
        'image_dimensions': {
            'width_pixels': detection_result.image_shape[0],
            'height_pixels': detection_result.image_shape[1],
            'total_area_pixels': detection_result.image_area_pixels
        }
    }
