# CODEMANTRA 2K23 - Quick Start Guide

## System Requirements

- **Python**: 3.11 or higher (3.13.3+ tested)
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Disk Space**: ~500MB for dependencies and sample images

## Installation & Setup (5 minutes)

### Step 1: Navigate to Project Directory

```bash
cd codemantra-2k23
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Installation time**: ~2-3 minutes (depending on internet speed)

### Step 4: Generate Sample Image (Optional)

```bash
python scripts/generate_demo_image.py
```

This creates a synthetic forest image at `data/sample/demo_forest.jpg` for testing.

### Step 5: Verify Installation

```bash
python test_application.py
```

If all 4 tests pass, your installation is complete!

### Step 6: Run Tests (Optional)

```bash
pytest tests/ -v
```

Expected: 20/20 tests should pass.

---

## Starting the Application

### Option A: Using Startup Scripts (Recommended)

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
bash run.sh
```

### Option B: Manual Start

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Option C: Production Mode

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Accessing the Application

1. Start the server (see above)
2. Open browser: **http://127.0.0.1:8000**
3. You should see the CODEMANTRA 2K23 dashboard

---

## Basic Workflow

### 1. Upload Image
- Click upload area or drag-and-drop
- Supports: JPG, JPEG, PNG, TIFF
- Maximum size: 50 MB

### 2. Configure Parameters (Optional)
- **Image Width/Height**: Set based on image scale (default: 500m)
- **Min/Max Tree Area**: Filter by tree size (adjust if needed)
- **Circularity**: Shape filter (0.5 is good for most cases)

### 3. Run Detection
- Click "Run Detection" button
- Processing takes 5-15 seconds depending on image size
- View results on dashboard

### 4. Explore Results
- **Dashboard**: Summary statistics
- **Results Page**: Detailed analysis and tree table
- **Map**: Interactive Leaflet map with tree locations

### 5. Export Data
- Download as CSV for spreadsheet analysis
- Download as GeoJSON for GIS software (QGIS, ArcGIS, etc.)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cv2'"

**Solution:**
```bash
pip install --force-reinstall opencv-python
```

### Issue: "Address already in use"

The port 8000 is already occupied. Either:
- Kill the existing process: `netstat -ano | findstr :8000` (Windows)
- Change the port: `uvicorn app.main:app --port 8001`

### Issue: No trees are being detected

1. Check if the image has sufficient green content
2. Adjust the detection parameters:
   - Lower "Min Tree Area" for smaller trees
   - Raise "Max Tree Area" if detection is cutting off large trees
   - Adjust circularity threshold (0.3-0.7)
3. Test with the provided sample image

### Issue: Application crashes on upload

- Ensure the image file is not corrupted
- Try with the sample image: `data/sample/demo_forest.jpg`
- Check file size (max 50 MB)

---

## Development

### Run Tests
```bash
pytest tests/ -v
```

### Check Code
```bash
# Install linting tools (optional)
pip install pylint flake8

pylint app/
flake8 app/
```

### Add New Features
The project structure supports easy extension:
- Add new routes in `app/routes/`
- Add new services in `app/services/`
- Update frontend in `app/templates/` and `app/static/`

---

## Project Structure

```
codemantra-2k23/
├── app/                    # Application code
│   ├── main.py            # FastAPI entry point
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── templates/         # HTML pages
│   └── static/            # CSS, JS, images
├── data/
│   ├── uploads/           # User-uploaded images
│   ├── results/           # Detection outputs
│   └── sample/            # Demo images
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
├── README.md              # Full documentation
├── test_application.py    # E2E tests
├── run.bat/run.sh        # Startup scripts
└── .gitignore            # Git ignore rules
```

---

## Using with Your Own Images

1. Prepare an aerial/forest image
2. Best results with:
   - Clear, well-defined tree canopies
   - RGB or color images
   - Resolution: 0.5-2 m/pixel (aerial)
   - 1024x768 to 2048x2048 pixels recommended

3. Upload to the dashboard
4. Adjust detection parameters if needed:
   - Vegetation density affects detection
   - Parameter tuning is image-dependent

5. Export and analyze results

---

## Tips for Best Results

1. **Image Quality**: Clearer images = better results
2. **Image Scale**: Know approximately how many meters the image covers
3. **Time of Year**: Summer images (more green) work better
4. **Cloud Cover**: Clouds reduce accuracy
5. **Tree Overlap**: Overlapping trees may be detected as one
6. **Parameter Tuning**: Experiment with detection parameters for your specific images

---

## API Reference (for Advanced Users)

See `README.md` or navigate to `http://127.0.0.1:8000/docs` (when running) for full API documentation.

### Quick API Examples

```bash
# Health check
curl http://127.0.0.1:8000/api/health

# Upload image
curl -X POST -F "file=@images/forest.jpg" http://127.0.0.1:8000/api/upload

# Run detection
curl -X POST "http://127.0.0.1:8000/api/detect?image_path=data/uploads/forest.jpg&min_tree_area=50&max_tree_area=10000"
```

---

## Support & Resources

- **Documentation**: See `README.md`
- **Code**: Well-commented source code in `app/`
- **Tests**: `tests/` directory shows usage examples
- **About Page**: In-app `/about` page with more information

---

## What's Included

✓ **Tree Detection**: OpenCV-based vegetation segmentation  
✓ **Geospatial Conversion**: Pixel to geographic coordinate mapping  
✓ **Interactive Maps**: Leaflet.js map visualization  
✓ **Data Export**: CSV and GeoJSON outputs  
✓ **Validation**: Ground-truth comparison metrics  
✓ **Web Interface**: Clean, responsive dashboard  
✓ **Unit Tests**: 20 tests covering core functionality  
✓ **Documentation**: Comprehensive README and comments  

---

## Next Steps

1. Run `test_application.py` to verify everything works
2. Start the server with `run.bat` (Windows) or `bash run.sh` (macOS/Linux)
3. Open http://127.0.0.1:8000 in your browser
4. Upload a sample or your own aerial image
5. Run detection and explore the results!

---

**Version**: 1.0  
**Status**: Academic MVP - Fully Functional  
**Last Updated**: September 2026
