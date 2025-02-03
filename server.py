from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FILE = "output.jpg"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/process")
async def process(image: UploadFile = File(...), texture: UploadFile = File(...)):
    try:
        image_path = os.path.join(UPLOAD_FOLDER, "original.jpg")
        texture_path = os.path.join(UPLOAD_FOLDER, "texture.jpg")

        # Sauvegarde des fichiers uploadés
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        with open(texture_path, "wb") as buffer:
            shutil.copyfileobj(texture.file, buffer)

        # Exécuter le script launch.py
        result = subprocess.run(["python3", "launch.py"], capture_output=True, text=True)

        if result.returncode == 0:
            return JSONResponse(content={"success": True, "output_url": "/output"})
        else:
            return JSONResponse(content={"success": False, "error": result.stderr}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

@app.get("/output")
async def get_output():
    if os.path.exists(OUTPUT_FILE):
        return FileResponse(OUTPUT_FILE, media_type="image/jpeg")
    return JSONResponse(content={"error": "Output file not found"}, status_code=404)

