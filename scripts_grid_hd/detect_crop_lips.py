import numpy as np
import cv2
import mediapipe as mp
import os
import matplotlib.pyplot as plt

def crop_lips_with_margin(
    image_path: str,
    margin_x: int,
    margin_y: int,
    offset_x: int = 0,
    offset_y: int = 0,
    face_mesh=None
) -> np.ndarray:
    """Detects the lips in the image, applies margins and offset, and saves the cropped lips image.
    
    Args:
        image_path: Path to the input image file.
        margin_x: Horizontal margin around the lips bounding box in pixels.
        margin_y: Vertical margin around the lips bounding box in pixels.
        offset_x: Horizontal offset in pixels to move the cropping window.
        offset_y: Vertical offset in pixels to move the cropping window.
        
    Returns:
        Cropped lips image with margins and offset applied, or None if no lips are detected.
    """
    
    # Define the lip connections as a set of tuples
    FACEMESH_LIPS = frozenset([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                               (17, 314), (314, 405), (405, 321), (321, 375),
                               (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                               (37, 0), (0, 267), (267, 269), (269, 270), (270, 409),
                               (409, 291), (78, 95), (95, 88), (88, 178), (178, 87),
                               (87, 14), (14, 317), (317, 402), (402, 318), (318, 324),
                               (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                               (82, 13), (13, 312), (312, 311), (311, 310), (310, 415),
                               (415, 308)])
    
    # Load the input image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect facial landmarks
    results = face_mesh.process(rgb_image)
    
    if not results.multi_face_landmarks:
        print("No face landmarks detected.")
        return None
    
    # Initialize variables to store the bounding box of the lips
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    # Calculate the bounding box of the lips
    for face_landmarks in results.multi_face_landmarks:
        for idx in set(idx for pair in FACEMESH_LIPS for idx in pair):
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    
    # Apply margins and offsets
    min_x = max(min_x - margin_x + offset_x, 0)
    min_y = max(min_y - margin_y + offset_y, 0)
    max_x = min(max_x + margin_x + offset_x, image.shape[1])
    max_y = min(max_y + margin_y + offset_y, image.shape[0])
    
    # Crop the lips region
    cropped_lips = rgb_image[min_y:max_y, min_x:max_x]
    
    # Convert to BGR for saving
    bgr_cropped_lips = cv2.cvtColor(cropped_lips, cv2.COLOR_RGB2BGR)
    
    # Save the cropped lips image
    filename, ext = os.path.splitext(image_path)
    cropped_filename = f"{filename}_cropped_lips{ext}"
    #cv2.imwrite(cropped_filename, bgr_cropped_lips)
    #print(f"Saved cropped lips image as: {cropped_filename}")
    
    return cropped_lips


# Example usage:
#image_path = 'frame_006.jpg'
#cropped_image = crop_lips_with_margin(image_path, margin_x=10, margin_y=10, offset_y=0)


#if cropped_image is not None:
    #plt.imshow(cropped_image)
    #plt.axis('off')
    #plt.show()