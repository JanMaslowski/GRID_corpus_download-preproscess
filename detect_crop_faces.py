from typing import Tuple, Union
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

def crop_face_with_margin(
    image_path: str,
    margin_x: int,
    margin_y: int,
    offset_y: int
) -> np.ndarray:
    """Detects a face in the image, applies margins and offset, and saves the cropped face image.
    
    Args:
        image_path: Path to the input image file.
        margin_x: Horizontal margin around face bounding box in pixels.
        margin_y: Vertical margin around face bounding box in pixels.
        offset_y: Offset in pixels to move the cropping window down in y-direction.
        
    Returns:
        Cropped face image with margins and offset applied.
    """
    # Load the model and image
    base_options = python.BaseOptions(model_asset_path='detector.tflite')
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)
    image = mp.Image.create_from_file(image_path)


    detection_result = detector.detect(image)
    
    if not detection_result.detections:
        print("No face detected.")
        return None

    image_copy = np.copy(image.numpy_view())
    height, width, _ = image_copy.shape


    detection = detection_result.detections[0]
    bbox = detection.bounding_box
    x_min, y_min = bbox.origin_x, bbox.origin_y
    x_max = x_min + bbox.width
    y_max = y_min + bbox.height

    x_min = max(0, x_min - margin_x)
    y_min = max(0, y_min - margin_y + offset_y)
    x_max = min(width, x_max + margin_x)
    y_max = min(height, y_max + margin_y + offset_y)

    cropped_face = image_copy[y_min:y_max, x_min:x_max]
    rgb_cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

    filename, ext = os.path.splitext(image_path)
    cropped_filename = f"{filename}_cropped{ext}"

    cv2.imwrite(cropped_filename, rgb_cropped_face)
    print(f"Saved cropped face image as: {cropped_filename}")

    return rgb_cropped_face

# Example usage:
#image_path = 'frame_002.jpg'
#cropped_image = crop_face_with_margin(image_path, margin_x=10, margin_y=40, offset_y=-27)

# Display the cropped image if available
#if cropped_image is not None:
    #plt.imshow(cropped_image)
    #plt.axis('off')
    #plt.show()