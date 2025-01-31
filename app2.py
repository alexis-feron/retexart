import cv2
import numpy as np

def generate_rgb_palette():
    """Génère une palette complète de couleurs RGB sous forme de plages HSV avec encore plus de nuances."""
    colors = {}
    color_bgr = {}
    step = 5  # Réduction de l'intervalle de teinte pour plus de précision
    
    for hue in range(0, 180, step):  # Hue varie de 0 à 179 en OpenCV
        for sat in [50, 100, 150, 200, 255]:  # Ajout de plus de variations de saturation
            for val in [50, 100, 150, 200, 255]:  # Ajout de plus de variations de valeur
                color_name = f"color_{hue}_{sat}_{val}"
                lower = [hue, max(20, sat - 30), max(20, val - 30)]  # Plage inférieure
                upper = [hue + step - 1, min(255, sat + 30), min(255, val + 30)]  # Plage supérieure
                
                colors[color_name] = [lower, upper]
                
                # Convertir la couleur dominante de HSV à BGR pour l'affichage
                hsv_color = np.uint8([[[hue, sat, val]]])
                bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
                color_bgr[color_name] = tuple(map(int, bgr_color))
    
    return colors, color_bgr

# Charger l'image
image = cv2.imread('original.jpg')
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Générer la palette complète
colors, color_bgr = generate_rgb_palette()

# Créer une image de base (vide) pour dessiner les contours remplis
image_filled = np.zeros_like(image)

# Itérer sur les couleurs et appliquer le traitement
for color_name, (lower, upper) in colors.items():
    mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image_filled, contours, -1, color_bgr[color_name], thickness=cv2.FILLED)

# Afficher l'image résultante
cv2.imshow("Zones de couleur remplies", image_filled)
cv2.waitKey(0)
cv2.destroyAllWindows()