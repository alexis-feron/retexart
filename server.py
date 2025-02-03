from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/process", methods=["POST"])
def process():
    try:
        image = request.files["image"]
        texture = request.files["texture"]
        image_path = os.path.join(UPLOAD_FOLDER, "original.jpg")
        texture_path = os.path.join(UPLOAD_FOLDER, "texture.jpg")
        
        image.save(image_path)
        texture.save(texture_path)

        # Run the script
        result = subprocess.run(["python3", "launch.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({"success": True, "output_url": "/output"}), 200
        else:
            return jsonify({"success": False, "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/output")
def get_output():
    return send_file("output.jpg", mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
