from fastapi import FastAPI, File, UploadFile
from pathlib import Path

app = FastAPI()

upload_dir = Path(__file__).parent / "uploads"  # Define upload directory

# Create the upload directory if it doesn't exist
upload_dir.mkdir(parents=True, exist_ok=True)


@app.post("/upload-image")
async def upload_image(image: UploadFile = File(...)):
    # Get the uploaded filename
    filename = image.filename

    # Create a unique path to save the image
    filepath = upload_dir / filename

    # Save the uploaded image to the specified location
    contents = await image.read()
    with open(filepath, "wb") as f:
        f.write(contents)

    # Return a success message (optional)
    return {"message": f"Image '{filename}' uploaded successfully!"}

