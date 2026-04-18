from langchain.tools import StructuredTool
from pydantic import BaseModel
import subprocess
import os

# ==============================
# CONFIG
# ==============================
LIBREOFFICE_PATH = "soffice"

# ==============================
# FUNCTION
# ==============================
def convert_ppt_to_pdf(input_file: str, output_dir: str):
    try:
        command = [
            LIBREOFFICE_PATH,
            "--headless",
            "--convert-to", "pdf",
            input_file,
            "--outdir", output_dir
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return {"error": result.stderr}

        filename = os.path.basename(input_file).replace(".pptx", ".pdf")
        output_path = os.path.join(output_dir, filename)
    
        print("Successfully converted ✅")
        return {"output": output_path}

    except Exception as e:
        return {"error": str(e)}

# ==============================
# INPUT SCHEMA
# ==============================
class PPTtoPDFInput(BaseModel):
    input_file: str
    output_dir: str

# ==============================
# TOOL
# ==============================
tool_ppt_to_pdf = StructuredTool.from_function(
    name="ppt_to_pdf_converter",
    description="Convert a PPT/PPTX file into a PDF using LibreOffice in headless mode, both the paths are provided as input, your output will only be the filename of pdf",
    func=convert_ppt_to_pdf,
    args_schema=PPTtoPDFInput
)
