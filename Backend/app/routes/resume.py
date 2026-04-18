from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.services.resume_parser import parse_pdf, parse_docx
from app.services.llm_service import analyze_resume, validate_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB in bytes


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """
    Upload a resume (PDF or DOCX) and get the parsed text content.
    """
    # Validate file type
    content_type = file.content_type
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}. "
                   f"Allowed types: PDF (.pdf), Word (.docx)",
        )

    # Read file bytes
    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    
    # Validate file size (max 2MB)
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the maximum limit of 2MB. Uploaded file size: {len(file_bytes) / (1024 * 1024):.2f}MB"
        )

    file_type = ALLOWED_TYPES[content_type]

    try:
        if file_type == "pdf":
            result = parse_pdf(file_bytes)
        else:
            result = parse_docx(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse resume: {str(e)}",
        )

    # Use LLM to analyze the resume if GROQ_API_KEY is configured
    analysis = None
    if os.getenv("GROQ_API_KEY"):
        try:
            # First, validate if the document is actually a resume
            validation = await validate_resume(result["full_text"])
            
            if not validation.get("is_valid_resume", False):
                raise HTTPException(
                    status_code=400,
                    detail=f"Please upload a valid resume. {validation.get('reason', 'The uploaded document does not appear to be a resume.')}"
                )
            
            # If validation passes, proceed with full analysis
            analysis = await analyze_resume(result["full_text"])
        except HTTPException:
            raise  # Re-raise validation errors
        except Exception as e:
            # We don't want to completely fail the request if LLM fails
            analysis = {
                "error": "Failed to analyze resume with LLM.",
                "details": str(e)
            }
    else:
        analysis = {"error": "GROQ_API_KEY not configured on the server."}

    return {
        "status": "success",
        "filename": file.filename,
        "file_type": file_type,
        "data": result,
        "analysis": analysis
    }
