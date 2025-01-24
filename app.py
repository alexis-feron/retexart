import cv2
import numpy as np
from PIL import Image

def apply_texture_to_regions(image_path, texture_path, output_path, threshold=100):
    # Charger l'image de base
    base_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

    # Détection des contours pour trouver les zones homogènes
    _, thresh = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Charger la texture et préparer la sortie
    texture = cv2.imread(texture_path)
    output = base_image.copy()

    for contour in contours:
        # Obtenir un rectangle englobant la région détectée
        x, y, w, h = cv2.boundingRect(contour)

        # Ajuster la texture à la taille de la région détectée
        texture_resized = cv2.resize(texture, (w, h))

        # Créer un masque pour la zone de l'image originale
        mask = np.zeros_like(gray_image)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Appliquer la texture en respectant la forme détectée
        roi = output[y:y+h, x:x+w]
        texture_masked = cv2.bitwise_and(texture_resized, texture_resized, mask=mask[y:y+h, x:x+w])
        output[y:y+h, x:x+w] = cv2.addWeighted(roi, 0.5, texture_masked, 0.5, 0)

    # Sauvegarder et afficher le résultat final
    cv2.imwrite(output_path, output)
    Image.open(output_path).show()
    print(f"Image retexturée sauvegardée sous {output_path}")

# Exemple d'utilisation
apply_texture_to_regions("original.jpg", "texture.png", "texture_picture.jpg", threshold=120)
