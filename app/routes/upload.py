"""
Upload route handler.
Handles image uploads and validation.
"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import cv2
import numpy as np

router = APIRouter(prefix="/api", tags=["upload"])

UPLOAD_DIR = "data/uploads"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff', 'tif'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image_file(file_path: str) -> dict:
    """
    Validate uploaded image file.
    
    Returns:
        Dictionary with image info {'valid': bool, 'width': int, 'height': int, 'error': str or None}
    """
    try:
        image = cv2.imread(file_path)
        if image is None:
            return {'valid': False, 'error': 'Could not read image. Ensure it is a valid image file.'}
        
        height, width = image.shape[:2]
        return {
            'valid': True,
            'width': width,
            'height': height,
            'channels': image.shape[2] if len(image.shape) > 2 else 1,
            'error': None
        }
    except Exception as e:
        return {'valid': False, 'error': f'Image validation error: {str(e)}'}


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload aerial image for tree detection.
    
    Allowed formats: JPG, JPEG, PNG, TIFF
    Max file size: 50 MB
    """
    
    # Validate file extension
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check file size
    file_size = 0
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.0f} MB")
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Validate image
    validation = validate_image_file(file_path)
    
    if not validation['valid']:
        os.remove(file_path)  # Clean up
        raise HTTPException(status_code=400, detail=validation['error'])
    
    return {
        'status': 'success',
        'message': 'Image uploaded successfully',
        'filename': file.filename,
        'filepath': file_path,
        'width': validation['width'],
        'height': validation['height'],
        'file_size_mb': round(file_size / 1024 / 1024, 2)
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'service': 'CODEMANTRA 2K23 - Tree Enumeration API'
    }
