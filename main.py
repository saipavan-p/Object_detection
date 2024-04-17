
import os
import subprocess
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

# Mounting the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure OpenCV for headless mode
cv2.setNumThreads(0)  # Disable multithreading to prevent issues

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Read and return the HTML file
    with open("templates/index.html", "r") as file:
        return file.read()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded image to a specific location
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    upload_files = os.listdir("uploads/")
    if not upload_files:
        return {"message": "No files found in the uploads folder."}
    
    first_upload_file = upload_files[0]
    # Call the Python notebook script with the first file
    subprocess.run(["python", "notebook/detect.py", f"uploads/{first_upload_file}"])    
    # # Call the Python notebook script
    # subprocess.run(["python", "notebook/detect.py", f"uploads/{file.filename}"])
    # Ensure the output folder exists
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    # Get the path of the first image in the output folder
    output_files = os.listdir(output_folder)
    if output_files:
        first_image_path = os.path.join(output_folder, output_files[0])
        return {"filename": first_image_path}
    else:
        return {"message": "No output images found."}

@app.get("{filename}")
async def display_image(filename):
    # Serve the processed image
    return FileResponse(filename)

