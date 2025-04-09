import numpy as np
import cv2
import mediapipe as mp

def crop_lips_center_fixed(
    image: np.ndarray,
    crop_width: int = 128,
    crop_height: int = 64,
    offset_x: int = 0,
    offset_y: int = 0,
    face_mesh=None
) -> np.ndarray:
    """
    Wykrywa usta na obrazie, oblicza ich środek i wycina stały region o rozmiarze crop_width x crop_height.
    
    Args:
        image: Obraz w formacie numpy (BGR, jak z cv2).
        crop_width: Szerokość wyciętego regionu w pikselach.
        crop_height: Wysokość wyciętego regionu w pikselach.
        offset_x: Poziome przesunięcie środka wycinka.
        offset_y: Pionowe przesunięcie środka wycinka.
        face_mesh: Opcjonalnie obiekt face_mesh (jeśli nie podany, należy go utworzyć).
        
    Returns:
        Wycinek ust jako obraz (np. w formacie RGB) lub None, jeśli nie wykryto ust.
    """
    # Definicja indeksów ust wg MediaPipe
    FACEMESH_LIPS = frozenset([
        (61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
        (17, 314), (314, 405), (405, 321), (321, 375),
        (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
        (37, 0), (0, 267), (267, 269), (269, 270), (270, 409),
        (409, 291), (78, 95), (95, 88), (88, 178), (178, 87),
        (87, 14), (14, 317), (317, 402), (402, 318), (318, 324),
        (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
        (82, 13), (13, 312), (312, 311), (311, 310), (310, 415),
        (415, 308)
    ])
    
    # Sprawdź, czy obraz jest poprawny
    if image is None or image.size == 0:
        print("Podany obraz jest pusty lub nieprawidłowy.")
        return None
    
    # Konwersja do RGB dla MediaPipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Wykryj landmarki twarzy
    results = face_mesh.process(rgb_image)
    if not results.multi_face_landmarks:
        print("Nie wykryto landmarków twarzy.")
        return None

    # Zakładamy, że przetwarzamy pierwszą wykrytą twarz
    face_landmarks = results.multi_face_landmarks[0]
    
    # Zbierz wszystkie punkty ust
    lip_points = []
    for idx in set(idx for pair in FACEMESH_LIPS for idx in pair):
        landmark = face_landmarks.landmark[idx]
        x = int(landmark.x * image.shape[1])
        y = int(landmark.y * image.shape[0])
        lip_points.append((x, y))
    lip_points = np.array(lip_points)
    
    # Oblicz środek ust jako średnią ze współrzędnych
    center_x = int(np.mean(lip_points[:, 0])) + offset_x
    center_y = int(np.mean(lip_points[:, 1])) + offset_y
    
    # Oblicz granice wycinka
    half_w = crop_width // 2
    half_h = crop_height // 2
    x1 = max(center_x - half_w, 0)
    y1 = max(center_y - half_h, 0)
    x2 = min(center_x + half_w, image.shape[1])
    y2 = min(center_y + half_h, image.shape[0])
    
    # Wytnij region ust
    cropped_lips = rgb_image[y1:y2, x1:x2]
    
    return cropped_lips