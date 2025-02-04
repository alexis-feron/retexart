from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


OUTPUT_FOLDER = "outputs"
TEXTURE_FOLDER = "textures"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEXTURE_FOLDER, exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, multipart/form-data"
    return response

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/process", methods=["POST"])
def process():
    try:
        print("Processing request...")

        # Sauvegarder l'image téléchargée
        image = request.files["image"]
        image_path = os.path.join(UPLOAD_FOLDER, "original.jpg")
        image.save(image_path)

        # Vérifier si une texture est choisie depuis la liste ou une nouvelle est téléchargée
        texture_name = request.form.get("texture_name")  # Nom de la texture choisie
        if texture_name:
            # Si la texture est choisie depuis la liste, on copie celle-ci dans le dossier `uploads`
            texture_path = os.path.join(TEXTURE_FOLDER, texture_name)
            # Copie de la texture existante vers `uploads/texture.jpg`
            with open(os.path.join(UPLOAD_FOLDER, "texture.jpg"), 'wb') as f_out:
                with open(texture_path, 'rb') as f_in:
                    f_out.write(f_in.read())
        else:
            texture = request.files.get("new-texture")  # Fichier de texture envoyé
            if texture and allowed_file(texture.filename):
                # Sauvegarder la nouvelle texture sous `uploads/texture.jpg`
                texture_path = os.path.join(UPLOAD_FOLDER, "texture.jpg")
                texture.save(texture_path)
            else:
                return jsonify({"success": False, "error": "Aucune texture valide sélectionnée"}), 400

        # Lancer le traitement
        result = subprocess.run(["python", "launch.py"], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({"success": True, "output_url": "/output"}), 200
        else:
            print(result.stderr)
            return jsonify({"success": False, "error": result.stderr}), 500
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/output")
def get_output():
    return send_file("output.jpg", mimetype="image/jpeg")

# Route pour lister les textures
@app.route("/textures", methods=["GET"])
def get_textures():
    try:
        textures = [f for f in os.listdir(TEXTURE_FOLDER) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]
        return jsonify(textures), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
