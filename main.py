from fastapi import FastAPI, Request, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import Formats
from PIL import Image
import os
import traceback

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Directory where files will be saved
UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("homepage.html", context)

@app.post("/convert/")
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    format: Formats = Form(...)
):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    # Save the uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # Convert the format to uppercase to match Pillow's expected format
    format_str = format.value.upper()

    try:
        img = Image.open(file_location)
        new_file_location = file_location.rsplit('.', 1)[0] + f".{format_str}"
        img.save(new_file_location, format=format_str)
        return HTMLResponse(content=f'<p class="text-green-500">File converted successfully: <a href="/{new_file_location}" class="text-blue-500 underline">{new_file_location}</a></p>', status_code=200)
    except Exception as e:
        # Capture the error message and traceback
        error_message = str(e)
        error_trace = traceback.format_exc()
        # Return the error response with traceback for debugging
        return HTMLResponse(content=f'<p class="text-red-500">Error: {error_message}<br><pre>{error_trace}</pre></p>', status_code=500)
