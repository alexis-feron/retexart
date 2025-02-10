import numpy as np
import cv2
from launch import generate_rgb_palette 

def test_generate_rgb_palette():
    colors, color_bgr = generate_rgb_palette()
    
    assert isinstance(colors, dict), "La palette doit être un dictionnaire."
    assert isinstance(color_bgr, dict), "La palette BGR doit être un dictionnaire."
    assert len(colors) > 0, "La palette ne doit pas être vide."

    sample_key = "color_0_50_50"
    assert sample_key in colors, "Clé manquante dans la palette."
    assert len(colors[sample_key]) == 2, "Chaque couleur doit avoir des bornes inférieure et supérieure."

    hsv_sample = np.uint8([[[0, 50, 50]]])
    bgr_sample = cv2.cvtColor(hsv_sample, cv2.COLOR_HSV2BGR)[0][0]
    assert color_bgr[sample_key] == tuple(map(int, bgr_sample)), "Erreur de conversion HSV -> BGR."

def test_image_loading():
    image = cv2.imread('uploads/original.jpg')
    assert image is not None, "L'image originale est introuvable."

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    assert hsv_image.shape == image.shape, "L'image HSV doit avoir la même dimension que l'originale."

def test_color_detection():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image[:] = (0, 255, 0)  # Image verte

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower = np.array([50, 100, 100])
    upper = np.array([70, 255, 255])
    
    mask = cv2.inRange(hsv_image, lower, upper)
    assert np.count_nonzero(mask) > 0, "Le masque doit détecter du vert."

def test_mask_operations():
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[30:70, 30:70] = 255

    kernel = np.ones((1, 1), np.uint8)
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_opened = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

    assert np.array_equal(mask, mask_opened), "L'opération morphologique ne doit pas modifier un masque propre."

def test_texture_application():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    texture = np.ones((100, 100, 3), dtype=np.uint8) * 255  # Texture blanche
    
    offset_x = 10
    offset_y = 10

    texture_moved = np.roll(texture, offset_x, axis=1)
    texture_moved = np.roll(texture_moved, offset_y, axis=0)

    assert texture_moved[0, 0][0] == 255, "Erreur dans le décalage de la texture."

def test_inpainting():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, background_mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(background_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    assert len(contours) == 0, "L'image est vide, il ne doit pas y avoir de contours."
