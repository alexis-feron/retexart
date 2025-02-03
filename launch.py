import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

def generate_rgb_palette():
    """Génère une palette de couleurs RGB sous forme de plages HSV avec plus de nuances."""
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

# Charger l'image et la texture
image = cv2.imread('original.jpg')
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
texture = cv2.imread('textures/texture-laine.jpg')

# Générer la palette de couleurs
colors, color_bgr = generate_rgb_palette()

# Créer une image vide pour dessiner les formes fusionnées
image_filled = np.zeros_like(image)

# Pré-calculer le redimensionnement de la texture pour éviter des appels répétés
texture_resized = cv2.resize(texture, (image.shape[1], image.shape[0]))

# Utiliser un masque pour éviter les répétitions dans la boucle
for color_name, (lower, upper) in tqdm(colors.items(), desc="Traitement des couleurs", total=len(colors)):
    # Appliquer le masque de couleur une fois
    mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))

    # Éviter le filtrage excessif et réduire le noyau
    kernel = np.ones((3, 3), np.uint8)  # Réduit la taille du noyau
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Remplacer la recherche de contours par une méthode plus rapide
    # Utiliser np.where pour obtenir des régions avec des couleurs similaires
    region = np.where(mask == 255)

    if len(region[0]) > 0:  # Si la région n'est pas vide
        # Créer un masque de la région
        mask_region = np.zeros_like(image, dtype=np.uint8)
        mask_region[region] = 255  # Remplir la région où la couleur est trouvée
        
        # Appliquer un décalage constant pour la texture
        offset_x = (hash(color_name) * 20) % texture.shape[1]
        offset_y = (hash(color_name) * 20) % texture.shape[0]

        # Optimiser le mouvement de la texture
        texture_moved = np.roll(texture_resized, offset_x, axis=1)
        texture_moved = np.roll(texture_moved, offset_y, axis=0)

        # Convertir la texture en gris et redimensionner
        texture_gray = cv2.cvtColor(texture_moved, cv2.COLOR_BGR2GRAY)
        texture_gray = cv2.cvtColor(texture_gray, cv2.COLOR_GRAY2BGR)
        
        # Appliquer la couleur à la texture
        bgr_color = color_bgr[color_name]
        color_overlay = np.zeros_like(texture_gray)
        color_overlay[:] = bgr_color

        # Fusionner la texture et la couleur
        texture_colored = cv2.addWeighted(texture_gray, 0.5, color_overlay, 0.5, 0)

        # Appliquer la texture colorée à la région
        image_filled[region] = texture_colored[region]

# Remplir les trous noirs avec cv2.inpaint
mask_black = np.all(image_filled == [0, 0, 0], axis=-1).astype(np.uint8) * 255
image_filled = cv2.inpaint(image_filled, mask_black, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Sauvegarder et afficher l’image
output_path = 'output.jpg'
cv2.imwrite(output_path, image_filled)
Image.open(output_path).show()
cv2.waitKey(0)
cv2.destroyAllWindows()
