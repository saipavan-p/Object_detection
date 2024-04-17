# main.py (FastAPI backend)

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse


app = FastAPI()

# Mounting the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


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
    return {"filename": file.filename}


@app.get("/display/{filename}")
async def display_image(filename):
    # Serve the uploaded image
    return FileResponse(f"uploads/{filename}")
