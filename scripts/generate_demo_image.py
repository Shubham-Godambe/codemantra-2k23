"""
Generate synthetic demo forest image with tree-like circles.
Run this to create a sample image for testing without external data.
"""

import cv2
import numpy as np
from pathlib import Path
import sys

def generate_demo_forest_image(width=800, height=600, num_trees=25, output_path="data/sample/demo_forest.jpg"):
    """
    Generate a synthetic aerial-style forest image.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        num_trees: Number of trees to generate
        output_path: Where to save the image
    """
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Create base image - sky blue background
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add gradient sky
    for y in range(height):
        # Gradient from lighter blue at top to slightly darker
        intensity = int(100 + (y / height) * 20)
        image[y, :] = [200 - intensity // 3, 180 - intensity // 3, 120]  # Brown earth tones
    
    # Generate random trees as circles with green vegetation
    np.random.seed(42)  # For reproducibility
    
    tree_centers = []
    tree_radii = []
    
    for _ in range(num_trees):
        # Random position
        x = np.random.randint(100, width - 100)
        y = np.random.randint(100, height - 100)
        
        # Random size
        radius = np.random.randint(20, 60)
        
        # Check for overlap with existing trees
        overlap = False
        for cx, cy, cr in zip(tree_centers[::1], tree_centers[1::2] if len(tree_centers) > 1 else [], tree_radii):
            if len(tree_centers) > 0:
                if (x - cx)**2 + (y - cy)**2 < (radius + cr + 30)**2:
                    overlap = True
                    break
        
        if not overlap:
            tree_centers.append(x)
            tree_centers.append(y)
            tree_radii.append(radius)
            
            # Draw tree crown (filled circle)
            # Vary shade of green for realism
            green_shade = np.random.randint(60, 120)
            color = (50, green_shade, 40)  # BGR format
            
            cv2.circle(image, (x, y), radius, color, -1)
            
            # Add slight shadow effect with darker circle
            shadow_color = (30, green_shade - 20, 20)
            cv2.circle(image, (x + int(radius * 0.3), y + int(radius * 0.3)), 
                      int(radius * 0.4), shadow_color, -1)
    
    # Add some noise and texture to make it more realistic
    noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
    image = cv2.convertScaleAbs(image.astype(np.int16) + noise)
    
    # Add Gaussian blur for smoothing
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Save image
    cv2.imwrite(output_path, image)
    print(f"✓ Demo forest image generated: {output_path}")
    print(f"  - Resolution: {width}x{height}")
    print(f"  - Approximate trees: {len(tree_centers) // 2}")
    
    return output_path


if __name__ == "__main__":
    try:
        # Generate demo image
        demo_path = generate_demo_forest_image(
            width=1024,
            height=768,
            num_trees=35,
            output_path="data/sample/demo_forest.jpg"
        )
        print("\n✓ Sample data generated successfully!")
        print(f"  Use the image at: {demo_path}")
        
    except Exception as e:
        print(f"✗ Error generating demo image: {e}", file=sys.stderr)
        sys.exit(1)
