import cv2
import numpy as np
from PIL import Image

def generate_rgb_palette():
    """Génère une palette complète de couleurs RGB sous forme de plages HSV avec plus de nuances."""
    colors = {}
    color_bgr = {}
    step = 5  # Intervalle réduit pour une meilleure précision
    
    for hue in range(0, 180, step):
        for sat in [50, 100, 150, 200, 255]:
            for val in [50, 100, 150, 200, 255]:
                color_name = f"color_{hue}_{sat}_{val}"
                lower = [hue, max(10, sat - 50), max(10, val - 50)]
                upper = [hue + step - 1, min(255, sat + 50), min(255, val + 50)]
                
                colors[color_name] = [lower, upper]
                
                hsv_color = np.uint8([[[hue, sat, val]]])
                bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
                color_bgr[color_name] = tuple(map(int, bgr_color))
    
    return colors, color_bgr

# Charger l'image
image = cv2.imread('original.jpg')
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Charger la texture
texture = cv2.imread('texture.png')

# Générer la palette complète
colors, color_bgr = generate_rgb_palette()

# Créer une image vide pour dessiner les formes fusionnées
image_filled = np.zeros_like(image)

# Itérer sur les couleurs et appliquer le traitement
for i, (color_name, (lower, upper)) in enumerate(colors.items()):
    mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
    
    # Appliquer un filtrage morphologique pour réduire le bruit
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Trouver les contours après filtrage
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 1:  # Filtrer les petites zones
            continue
        
        # Créer un masque de la région
        mask_region = np.zeros_like(image, dtype=np.uint8)
        cv2.drawContours(mask_region, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        
        # Appliquer un décalage sur la texture
        offset_x = (i * 20) % texture.shape[1]
        offset_y = (i * 20) % texture.shape[0]
        
        texture_resized = np.roll(np.roll(texture, offset_x, axis=1), offset_y, axis=0)
        texture_resized = cv2.resize(texture_resized, (image.shape[1], image.shape[0]))
        
        # Convertir la texture en gris
        texture_gray = cv2.cvtColor(texture_resized, cv2.COLOR_BGR2GRAY)
        texture_gray = cv2.cvtColor(texture_gray, cv2.COLOR_GRAY2BGR)  # Retourne à 3 canaux (en gris)
        
        # Appliquer la couleur de la zone à la texture
        bgr_color = color_bgr[color_name]
        
        # Créer une image avec la couleur à appliquer (pour colorier la texture)
        color_overlay = np.zeros_like(texture_gray)
        color_overlay[:] = bgr_color  # Remplir l'image avec la couleur (RGB)
        
        # Appliquer la couleur sur la texture grise
        texture_colored = cv2.addWeighted(texture_gray, 0.5, color_overlay, 0.5, 0)
        
        # Appliquer la texture teintée à la région définie par le masque
        image_filled = np.where(mask_region == (255, 255, 255), texture_colored, image_filled)

# Convertir en niveaux de gris pour fusionner les zones proches
gray_filled = cv2.cvtColor(image_filled, cv2.COLOR_BGR2GRAY)
_, binary_filled = cv2.threshold(gray_filled, 1, 255, cv2.THRESH_BINARY)

# Appliquer une fermeture morphologique pour fusionner les zones voisines
binary_filled = cv2.morphologyEx(binary_filled, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))

# Détecter les nouveaux contours après fusion
contours, _ = cv2.findContours(binary_filled, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sauvegarder et afficher l’image
output_path = 'output.jpg'
cv2.imwrite(output_path, image_filled)
Image.open(output_path).show()
cv2.waitKey(0)
cv2.destroyAllWindows()
