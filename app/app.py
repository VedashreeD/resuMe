import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.file_handling import save_uploaded_file, save_multiple_files
from utils.pdf_to_docx import(
    extract_text_from_pdf, generate_diff, create_docx_from_pdf,
)
from utils.hugging_face_api import get_llm_suggestions  # Assuming this function exists
from fastapi.responses import JSONResponse

app = FastAPI()
UPLOAD_FOLDER = r"..\\uploaded_files"

# Enable CORS for all origins (you can be more specific if necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify the frontend's URL instead
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Route for file upload
@app.post("/upload")
async def upload_files(
    resume: UploadFile = File(...),
    additional_files: List[UploadFile] = File(...),
    job_description: str = Form(...),
):
    # Handle the resume file (PDF)
    if resume.content_type == 'application/pdf':
        try:
            # Save the resume file
            resume_filename = os.path.join(UPLOAD_FOLDER, resume.filename)
            with open(resume_filename, 'wb') as f:
                f.write(await resume.read())

            # Convert PDF to DOCX and extract text
            docx_filename = os.path.join(UPLOAD_FOLDER, resume.filename.replace('.pdf', '.docx'))
            if not os.path.exists(docx_filename):
                docx_filename = create_docx_from_pdf(resume_filename, docx_filename)

            # Extract text from the original and new PDFs
            original_text = extract_text_from_pdf(resume_filename)
            new_text = extract_text_from_pdf(docx_filename)  # Assuming docx is the newly generated version

            # Store additional files (same as before)
            additional_file_info = []
            for file in additional_files:
                additional_filename = os.path.join(UPLOAD_FOLDER, file.filename)
                with open(additional_filename, 'wb') as f:
                    f.write(await file.read())

            # Read the content of the file and store it in additional_file_info
            if file.content_type.startswith("text/"):  # If it's a text file
                with open(additional_filename, 'r') as f:
                    file_content = f.read()  # Read text content
            else:  # For binary files like PDF, DOCX, etc.
                with open(additional_filename, 'rb') as f:
                    file_content = f.read()  # Read binary content

            # Append the file information, including the content
            additional_file_info.append({
                "filename": file.filename,
                "content": file_content  # Save the content of the file
            })

            # Get suggestions from the LLM based on the original text or diff (you can choose which one to use)
            llm_suggestions = get_llm_suggestions(original_text, additional_file_info, job_description)  # Replace with diff if you want to use diff instead

            
            # Generate the diff between the two texts
            diff = generate_diff(original_text, llm_suggestions)

            data = {
                "message": "Files uploaded and stored successfully",
                "diff": diff,  # Return the diff to the frontend
                "llm_suggestions": llm_suggestions,  # Return the LLM suggestions
                "additional_files": additional_file_info,
            }
            return JSONResponse(content=data)

        except Exception as e:
            return {"error": f"Error saving files: {str(e)}"}
    else:
        return {"error": "The resume file is not a PDF."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
