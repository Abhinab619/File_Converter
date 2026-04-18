from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
from agent_service import get_agent_executor
from fastapi.middleware.cors import CORSMiddleware


 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

agent_executor = get_agent_executor()


@app.post("/convert")
async def convert(file: UploadFile = File(...)):

    input_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run agent
    response = agent_executor.invoke({
        "input": f"""
Convert PPT to PDF

input_file: {input_path}
output_dir: {OUTPUT_DIR}
"""
    })




    import json
    import re

    tool_output = response.get("output")

    if not tool_output:
        return {"error": "Conversion failed"}

    # Extract JSON part from mixed output
    match = re.search(r'\{.*"filename".*\}', tool_output, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group())
             
            filename = os.path.basename(data.get("filename"))
        except:
            return {"error": "Failed to parse filename"}
    else:
        return {"error": "Filename not found in response"}

    return {"filename": filename} 

@app.get("/download/{filename}")
def download_file(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(path):
        return {"error": "File not found"}

    return FileResponse(path, media_type='application/pdf', filename=filename)