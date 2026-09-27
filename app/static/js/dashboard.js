/* Dashboard JavaScript */

let uploadedImagePath = null;
let detectionResultId = null;
let currentDetectionResult = null;

// Array to store tree chart for potential updates
let treeChartInstance = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
    setupDetectionButton();
    setupValidationButton();
    setupExportButtons();
});

// ===== UPLOAD FUNCTIONALITY =====

function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');

    // Click to upload
    uploadArea.addEventListener('click', () => imageInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageUpload(files[0]);
        }
    });

    // File input change
    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageUpload(e.target.files[0]);
        }
    });
}

async function handleImageUpload(file) {
    const statusDiv = document.getElementById('uploadStatus');
    const detectBtn = document.getElementById('detectBtn');

    // Validate file
    const validExtensions = ['jpg', 'jpeg', 'png', 'tiff', 'tif'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
        showStatus('uploadStatus', `Invalid file type. Allowed: ${validExtensions.join(', ')}`, 'error');
        return;
    }

    const maxSize = 50 * 1024 * 1024; // 50 MB
    if (file.size > maxSize) {
        showStatus('uploadStatus', `File too large. Maximum: 50 MB`, 'error');
        return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('previewImage').style.display = 'block';
    };
    reader.readAsDataURL(file);

    // Upload file
    const formData = new FormData();
    formData.append('file', file);

    try {
        showStatus('uploadStatus', 'Uploading...', 'info');
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const data = await response.json();
        uploadedImagePath = data.filepath;

        // Show image info
        document.getElementById('fileName').textContent = data.filename;
        document.getElementById('fileSize').textContent = data.file_size_mb;
        document.getElementById('fileDimensions').textContent = `${data.width} x ${data.height}`;
        document.getElementById('imageInfo').style.display = 'block';

        showStatus('uploadStatus', 'Image uploaded successfully!', 'success');
        detectBtn.disabled = false;
        
        // Hidden input for image path (for detection)
        detectionResultId = null;
        document.getElementById('resultsCard').style.display = 'none';
        document.getElementById('validationCard').style.display = 'none';

    } catch (error) {
        showStatus('uploadStatus', `Upload error: ${error.message}`, 'error');
        detectBtn.disabled = true;
    }
}

// ===== DETECTION FUNCTIONALITY =====

function setupDetectionButton() {
    const detectBtn = document.getElementById('detectBtn');
    detectBtn.addEventListener('click', runDetection);
}

async function runDetection() {
    if (!uploadedImagePath) {
        showStatus('detectionStatus', 'Please upload an image first', 'error');
        return;
    }

    const imageWidth = parseFloat(document.getElementById('imageWidth').value) || 500;
    const imageHeight = parseFloat(document.getElementById('imageHeight').value) || 500;
    const minArea = parseInt(document.getElementById('minArea').value) || 50;
    const maxArea = parseInt(document.getElementById('maxArea').value) || 10000;
    const circularity = parseFloat(document.getElementById('circularity').value) || 0.5;

    // Show processing overlay
    document.getElementById('processingOverlay').style.display = 'flex';

    try {
        const params = new URLSearchParams({
            image_path: uploadedImagePath,
            min_tree_area: minArea,
            max_tree_area: maxArea,
            circularity: circularity,
            image_width_m: imageWidth,
            image_height_m: imageHeight
        });

        const response = await fetch(`/api/detect?${params}`, {
            method: 'POST'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Detection failed');
        }

        const data = await response.json();
        detectionResultId = data.result_id;
        currentDetectionResult = data;

        // Display results
        displayDetectionResults(data);
        
        document.getElementById('resultsCard').style.display = 'block';
        document.getElementById('validationCard').style.display = 'block';

        showStatus('detectionStatus', `Detection complete! ${data.total_trees} trees detected.`, 'success');

    } catch (error) {
        showStatus('detectionStatus', `Detection error: ${error.message}`, 'error');
    } finally {
        document.getElementById('processingOverlay').style.display = 'none';
    }
}

function displayDetectionResults(data) {
    document.getElementById('totalTrees').textContent = data.total_trees;
    document.getElementById('density').textContent = data.tree_density_per_hectare.toFixed(2);
    document.getElementById('imageArea').textContent = data.area_m2.toFixed(0);
    document.getElementById('avgArea').textContent = data.average_tree_area_pixels.toFixed(0);
}

// ===== VALIDATION FUNCTIONALITY =====

function setupValidationButton() {
    const validateBtn = document.getElementById('validateBtn');
    validateBtn.addEventListener('click', runValidation);
}

async function runValidation() {
    if (!detectionResultId) {
        showStatus('validationResult', 'No detection result available', 'error');
        return;
    }

    const groundTruth = parseInt(document.getElementById('groundTruth').value);
    
    if (isNaN(groundTruth) || groundTruth < 0) {
        showStatus('validationResult', 'Please enter a valid ground truth count', 'error');
        return;
    }

    try {
        const params = new URLSearchParams({
            result_id: detectionResultId,
            ground_truth_count: groundTruth
        });

        const response = await fetch(`/api/validate?${params}`, {
            method: 'POST'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Validation failed');
        }

        const data = await response.json();
        
        // Display validation results
        document.getElementById('detectedCount').textContent = data.detected_count;
        document.getElementById('truthCount').textContent = data.ground_truth_count;
        document.getElementById('difference').textContent = data.absolute_difference;
        document.getElementById('accuracy').textContent = data.accuracy.toFixed(4);
        document.getElementById('accuracyPercent').textContent = ` (${data.accuracy_percentage.toFixed(2)}%)`;
        
        document.getElementById('validationResult').style.display = 'block';

    } catch (error) {
        document.getElementById('validationResult').style.display = 'block';
        document.getElementById('detectedCount').parentElement.innerHTML = `
            <p style="color: red;">Validation error: ${error.message}</p>
        `;
    }
}

// ===== EXPORT FUNCTIONALITY =====

function setupExportButtons() {
    document.getElementById('viewMapBtn').addEventListener('click', () => {
        if (detectionResultId) {
            window.location.href = '/map';
        }
    });

    document.getElementById('downloadCSVBtn').addEventListener('click', () => {
        if (detectionResultId) {
            window.location.href = `/api/results/${detectionResultId}/csv`;
        }
    });

    document.getElementById('downloadGeoJSONBtn').addEventListener('click', () => {
        if (detectionResultId) {
            window.location.href = `/api/results/${detectionResultId}/geojson`;
        }
    });
}

// ===== UTILITY FUNCTIONS =====

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `status-message ${type}`;
    element.style.display = 'block';
}
