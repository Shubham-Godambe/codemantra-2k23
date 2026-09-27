# CODEMANTRA 2K23

## AI-Based Tree Enumeration and Forest Land Analysis Using Aerial Imagery

An academic MVP (Minimum Viable Product) for detecting, enumerating, and analyzing trees from aerial imagery using classical computer vision techniques, GIS visualization, and web technologies.

### Problem Statement

**"Application of Image Analytics For Tree Enumeration For Diversion of Forest Land"** 

This project addresses the Smart India Hackathon (2K23) problem statement focused on developing technologies for tree enumeration and forest land analysis using aerial imagery. The system aids in assessing forest composition and evaluating impacts on forest land diversion applications.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Quick Start](#quick-start)
6. [Project Structure](#project-structure)
7. [Usage Guide](#usage-guide)
8. [API Reference](#api-reference)
9. [Testing](#testing)
10. [Limitations](#limitations)
11. [Future Improvements](#future-improvements)
12. [Academic Integrity](#academic-integrity)

---

## Overview

CODEMANTRA 2K23 is a geospatial computer-vision prototype designed to:

- **Detect trees** from aerial/satellite imagery using OpenCV
- **Enumerate trees** with automatic counting
- **Calculate tree density** and forest metrics
- **Visualize results** on interactive maps
- **Export data** in CSV and GeoJSON formats
- **Validate detections** against ground-truth data

The system uses **classical computer vision** (not deep learning) with HSV-based vegetation segmentation, morphological operations, and contour detection. This makes it lightweight, interpretable, and suitable for educational purposes.

### Key Objectives

✅ Automated tree enumeration from aerial images  
✅ Vegetation segmentation and analysis  
✅ Geospatial visualization with Leaflet  
✅ Tree density calculation and forest metrics  
✅ Ground-truth validation framework  

---

## Features

### Core Functionality

- **Image Upload**: Drag-and-drop interface for JPG, PNG, JPEG, TIFF images (up to 50 MB)
- **Tree Detection**: OpenCV-based pipeline using HSV color space and contour detection
- **Configurable Parameters**: Adjust detection thresholds on-the-fly
  - Minimum/maximum tree area
  - Circularity threshold
  - Image dimensions (for density calculation)
- **Real-time Results**: Instant tree detection with visual overlay
- **Statistical Analysis**: Crown area statistics, tree density per hectare
- **Interactive Map**: Leaflet-based visualization with detected tree locations
- **Data Export**: Download results as CSV and GeoJSON
- **Ground-Truth Validation**: Compare detections against field data with accuracy metrics

### Technical Features

- **Fast Processing**: Optimized for images up to 1024x768 resolution
- **Transparent Parameters**: All detection parameters are displayed and configurable
- **Scalable**: Memory-efficient processing suitable for laptops
- **RESTful API**: Clean FastAPI endpoints for automation
- **Responsive UI**: Mobile-friendly dashboard and results pages

---

## Architecture

### Data Flow

```
Aerial Image Input
        ↓
  File Validation
        ↓
  Image Preprocessing (Resize)
        ↓
  RGB → HSV Conversion
        ↓
  Vegetation Segmentation (HSV Thresholding)
        ↓
  Morphological Operations (Erosion/Dilation)
        ↓
  Gaussian Blur & Denoising
        ↓
  Contour Detection
        ↓
  Shape Filtering (Area, Circularity)
        ↓
  Tree Identification & Labeling
        ↓
  Statistics Calculation
        ↓
  Pixel → Geographic Coordinate Conversion
        ↓
  GeoJSON/CSV Generation
        ↓
  Leaflet Map Visualization
        ↓
  Analysis & Reporting
```

### Component Overview

**Backend (FastAPI)**
- `app/main.py` - Application entry point
- `app/routes/` - API endpoint handlers
  - `upload.py` - Image upload and validation
  - `detection.py` - Tree detection orchestration
  - `analysis.py` - Analysis and validation endpoints

**Computer Vision (Services)**
- `app/services/tree_detector.py` - OpenCV-based detection pipeline
- `app/services/geospatial.py` - GIS conversion and export
- `app/services/validation.py` - Validation metrics

**Frontend**
- `app/templates/` - HTML pages
  - `index.html` - Dashboard with upload and detection
  - `results.html` - Analysis and statistics
  - `map.html` - Interactive map
  - `about.html` - Project information
- `app/static/css/style.css` - Styling
- `app/static/js/` - JavaScript functionality

**Data & Scripts**
- `data/uploads/` - User-uploaded images
- `data/results/` - Detection outputs
- `data/sample/` - Sample demo images
- `scripts/generate_demo_image.py` - Synthetic image generator

**Testing & Documentation**
- `tests/` - Unit tests
- `requirements.txt` - Dependencies
- `README.md` - This file

---

## Technology Stack

### Backend
- **Python 3.11+** - Programming language
- **FastAPI 0.104** - Web framework
- **Uvicorn** - ASGI server
- **python-multipart** - File upload handling

### Computer Vision & GIS
- **OpenCV 4.8** - Image processing and contour detection
- **NumPy 1.24** - Numerical operations
- **GeoPandas 0.14** - Geospatial data handling
- **Shapely 2.0** - Geometric operations
- **Rasterio 1.3** - Raster data I/O
- **Folium 0.14** - Map visualization (optional)
- **Pillow 10.1** - Image processing utilities

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Interactivity
- **Leaflet.js** - Interactive maps
- **Chart.js** - Data visualization

### Development & Testing
- **pytest 7.4** - Testing framework
- **git** - Version control

---

## Quick Start

### Prerequisites

- **Python 3.11+** installed
- **pip** package manager
- **Git** (optional, for cloning)

### Installation

1. **Clone the repository** (or extract the source):

```bash
cd codemantra-2k23
```

2. **Create a virtual environment**:

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Generate sample demo image** (optional):

```bash
python scripts/generate_demo_image.py
```

### Running the Application

1. **Start the server**:

```bash
python app/main.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2. **Open your browser**:

Navigate to: `http://127.0.0.1:8000`

3. **Use the application**:
   - Upload an aerial image
   - Configure detection parameters (or use defaults)
   - Click "Run Detection"
   - View results, explore the map, and download data

---

## Project Structure

```
codemantra-2k23/
│
├── app/
│   ├── main.py                          # FastAPI application entry point
│   │
│   ├── routes/                          # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── upload.py                    # Image upload endpoint
│   │   ├── detection.py                 # Tree detection endpoint
│   │   └── analysis.py                  # Analysis and validation endpoints
│   │
│   ├── services/                        # Core business logic
│   │   ├── __init__.py
│   │   ├── tree_detector.py             # OpenCV-based tree detector
│   │   ├── geospatial.py                # GIS conversion and export
│   │   └── validation.py                # Validation metrics
│   │
│   ├── templates/                       # HTML pages
│   │   ├── index.html                   # Dashboard
│   │   ├── results.html                 # Results & analysis
│   │   ├── map.html                     # Interactive map
│   │   └── about.html                   # Project information
│   │
│   └── static/                          # Static assets
│       ├── css/
│       │   └── style.css                # Main stylesheet
│       └── js/
│           ├── dashboard.js             # Dashboard functionality
│           ├── results.js               # Results page
│           └── map.js                   # Map visualization
│
├── data/
│   ├── uploads/                         # User-uploaded images
│   ├── results/                         # Detection outputs
│   └── sample/                          # Sample images for demo
│
├── tests/
│   ├── __init__.py
│   ├── test_detector.py                 # Tree detector tests
│   └── test_validation.py               # Validation tests
│
├── scripts/
│   └── generate_demo_image.py           # Generate synthetic forest images
│
├── requirements.txt                     # Python dependencies
├── README.md                            # This file
└── .gitignore                           # Git ignore rules
```

---

## Usage Guide

### Workflow

1. **Dashboard** (`/`)
   - Upload an aerial/forest image
   - Configure detection parameters (or keep defaults)
   - Click "Run Detection"

2. **Detection Results**
   - View stats: total trees, density, areas
   - See processed image with detected trees
   - Validate against ground truth (if available)

3. **Results Page** (`/results`)
   - View detailed analysis metrics
   - Explore tree crown area distribution chart
   - Download CSV with tree coordinates
   - Download GeoJSON for GIS software

4. **Map** (`/map`)
   - Interactive Leaflet map showing tree locations
   - Approximate geographic coordinates
   - Click markers for details

5. **About** (`/about`)
   - Project information
   - Architecture explanation
   - Limitations and future improvements

### Example: Detecting Trees in an Image

1. Upload a forest aerial image (JPG/PNG)
2. Adjust parameters if needed:
   - **Image Width/Height (meters)**: Set based on your image scale
   - **Min Tree Area**: Minimum crown size to detect
   - **Max Tree Area**: Maximum crown size to detect
   - **Circularity Threshold**: How round the object should be
3. Click "Run Detection"
4. View results and export as needed

---

## API Reference

### Endpoints

#### 1. Health Check

```
GET /api/health
```

Response:
```json
{
    "status": "healthy",
    "service": "CODEMANTRA 2K23 - Tree Enumeration API"
}
```

#### 2. Upload Image

```
POST /api/upload
Content-Type: multipart/form-data

file: <image_file>
```

Response:
```json
{
    "status": "success",
    "filename": "aerial_image.jpg",
    "filepath": "data/uploads/aerial_image.jpg",
    "width": 1024,
    "height": 768,
    "file_size_mb": 2.5
}
```

#### 3. Run Tree Detection

```
POST /api/detect
Query Parameters:
  - image_path (str): Path to uploaded image
  - min_tree_area (int, default=50): Minimum crown area
  - max_tree_area (int, default=10000): Maximum crown area
  - circularity (float, default=0.5): Circularity threshold (0-1)
  - image_width_m (float, default=500): Image width in meters
  - image_height_m (float, default=500): Image height in meters
```

Response:
```json
{
    "status": "success",
    "result_id": 1,
    "total_trees": 47,
    "image_dimensions": [1024, 768],
    "area_m2": 250000,
    "tree_density_per_hectare": 18.8,
    "average_tree_area_pixels": 542.3,
    "processed_image": "data/results/result_1_detected.jpg"
}
```

#### 4. Get Results

```
GET /api/results/{result_id}
```

Response:
```json
{
    "status": "success",
    "result_id": 1,
    "total_trees": 47,
    "trees": [
        {
            "tree_id": 1,
            "pixel_x": 250.5,
            "pixel_y": 180.3,
            "radius_pixels": 35.2,
            "contour_area_pixels": 542.1
        }
    ],
    "tree_density_per_hectare": 18.8
}
```

#### 5. Download GeoJSON

```
GET /api/results/{result_id}/geojson
```

Returns GeoJSON file with tree features including geographic coordinates.

#### 6. Download CSV

```
GET /api/results/{result_id}/csv
```

Returns CSV with columns: tree_id, pixel_x, pixel_y, estimated_latitude, estimated_longitude, detected_area_pixels

#### 7. Validate Detection

```
POST /api/validate
Query Parameters:
  - result_id (int): Detection result ID
  - ground_truth_count (int): Actual tree count
```

Response:
```json
{
    "status": "success",
    "detected_count": 47,
    "ground_truth_count": 50,
    "absolute_difference": 3,
    "accuracy": 0.94,
    "accuracy_percentage": 94.0
}
```

#### 8. Get Analysis

```
GET /api/analysis/{result_id}
```

Returns detailed analysis metrics.

---

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_detector.py

# Run with coverage
pytest --cov=app tests/
```

### Test Coverage

- **test_detector.py**: Tree detection functionality
  - Image loading and validation
  - Tree detection accuracy
  - Parameter handling
  - Statistics calculation

- **test_validation.py**: Validation and accuracy metrics
  - Accuracy calculations
  - Input validation
  - Error handling

### Example Test

```bash
pytest tests/test_detector.py::TestTreeDetector::test_detect_trees -v
```

---

## Limitations

### ⚠️ Important - Academic MVP

This is a **student portfolio project** for the Smart India Hackathon. The following limitations must be understood:

1. **Classical Computer Vision MVP**
   - Uses OpenCV with HSV thresholding, not deep learning
   - Accuracy heavily depends on image quality and vegetation type
   - Not suitable for dense forests or complex ecosystems

2. **Demo Coordinates**
   - Without GPS/georeferencing metadata, coordinates are APPROXIMATE
   - Uses a configurable demo reference location (Delhi by default)
   - Actual geographic accuracy requires image metadata or ground control points
   - **Never use for official land surveys without proper validation**

3. **No Species Classification**
   - Detects vegetation only, does not classify tree species
   - Would require multispectral analysis or trained models

4. **Simple Validation**
   - Count-based validation only
   - Does not perform spatial matching (IoU) or false positive analysis
   - Production systems require comprehensive ground-truth validation

5. **Single-Image Processing**
   - Processes one image at a time
   - No time-series or multi-temporal analysis

6. **Limited to Visual Spectrum**
   - No multispectral or hyperspectral analysis
   - Cannot calculate vegetation indices (NDVI, EVI, etc.)

7. **Not for Official Decisions**
   - **This is a prototype and NOT suitable for forest-land approval decisions**
   - Government land diversion requires official ground surveys and satellite data
   - Use only as a preliminary screening tool

8. **No External Data Integration**
   - No satellite data (Landsat, Sentinel-2)
   - No forest department database integration
   - No drone flight log processing

### Performance Notes

- Best results with clear, well-defined tree canopies
- Struggles with overlapping trees or dense vegetation
- Requires images at suitable resolution (recommended: 0.5-1 m/pixel)
- Processing time: ~5-10 seconds for 1024x768 images

---

## Future Improvements

### Phase 2: Enhanced Detection
- 🚀 Integrate YOLO or DeepForest deep learning models
- 🎯 Improve detection accuracy with trained models
- 📊 Add confidence scores to detections

### Phase 3: Geospatial Capabilities
- 🛰️ Sentinel-2 and Landsat satellite imagery support
- 🚁 Drone imagery processing with flight log data
- 📡 Multispectral analysis (NDVI, color-infrared)
- 🗺️ Real georeferenced raster processing with CRS handling

### Phase 4: Advanced Analysis
- 🌍 Automated species classification using spectral features
- 🌳 Forest health assessment (crown condition, stress indicators)
- 📈 Temporal analysis (growth tracking, deforestation monitoring)
- 🔬 Biomass estimation

### Phase 5: Validation & Field Work
- 📊 Improved ground-truth validation with spatial matching
- ✓ Confusion matrix and precision/recall computation
- 📱 Mobile app for field data collection
- 🗄️ Integration with forest department databases

### Phase 6: Production Deployment
- ☁️ Cloud deployment (AWS, GCP, Azure)
- 📋 Batch processing for large image collections
- 🔐 Authentication and role-based access control
- 📊 Advanced analytics dashboard

---

## Academic Integrity

This project is presented honestly as an **academic prototype**:

✅ **Transparent about limitations:**
- Clearly labeled as classical CV MVP (not deep learning)
- Demo coordinates marked as approximate
- Validation methodology is simple and documented

✅ **No fabrication:**
- No fake datasets or false performance claims
- Sample images are synthetic (clearly marked)
- No false claims about satellite integration or species classification

✅ **Suitable for:**
- Student portfolios and CV
- Master's applications
- Computer vision and GIS education
- Research on vegetation detection

✅ **Not suitable for:**
- Production forest monitoring
- Official government decisions
- Commercial forest assessment services
- Scientific publications (without proper validation)

### How to Present This Project

**On CV/Portfolio:**
> "Developed CODEMANTRA 2K23, a prototype geospatial computer-vision application for tree enumeration from aerial imagery. Implemented OpenCV-based vegetation detection pipeline with HSV segmentation, contour analysis, and geospatial coordinate conversion. Created interactive Leaflet-based map visualization and CSV/GeoJSON export. Built with FastAPI backend and responsive HTML/CSS/JavaScript frontend. Academic MVP for portfolio demonstration."

**In Interviews:**
> "This is a prototype I built to explore computer vision and GIS. It uses classical OpenCV techniques rather than deep learning, which keeps it lightweight and interpretable. The system can detect trees in aerial images and estimate forest density, though with limitations noted in the README. It's suitable for educational purposes and portfolio demonstration."

---

## Contributing

This is a student project. Contributions welcome for:
- Bug fixes
- Documentation improvements
- Additional test cases
- Performance optimizations
- Educational enhancements

---

## License

This project is created for educational purposes as part of the Smart India Hackathon 2K23.

---

## Acknowledgments

- **Smart India Hackathon 2023** - Problem statement and inspiration
- **OpenCV** - Computer vision library
- **FastAPI** - Web framework
- **Leaflet.js** - Map visualization
- **Chart.js** - Data visualization

---

## Support & Questions

For questions or issues:
1. Check the `About` page in the application
2. Review test cases in `tests/`
3. Consult OpenCV and GeoPandas documentation
4. Review the README limitations section

---

**Last Updated**: September 2026  
**Status**: Academic MVP - Version 1.0  
**Suitable for**: Student Portfolio, Master's Applications, Educational Demonstrations
