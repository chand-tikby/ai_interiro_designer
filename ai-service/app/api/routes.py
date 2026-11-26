import base64
from fastapi import APIRouter, HTTPException, Request
from app.schemas.design import RoomDesignRequest, RoomDesignResponse
from app.services.interior_service import interior_service
from app.services.pdf_extractor import pdf_extractor

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-service",
        "version": "0.1.0"
    }


@router.post("/design/generate", response_model=RoomDesignResponse)
def generate_design(request: RoomDesignRequest):
    return interior_service.generate_recommendations(request)


@router.post("/extract")
async def extract_floorplan(request: Request):
    """
    Step 4 & 5:
    Accepts PDF binary buffer or JSON payload with base64 PDF.
    Uses PyMuPDF for vector commands + text, renders page to high-res image,
    and runs OpenCV line & contour detection for architectural elements.
    """
    content_type = request.headers.get("content-type", "")
    pdf_bytes = b""

    try:
        if "application/json" in content_type:
            data = await request.json()
            if "pdf_base64" in data:
                pdf_bytes = base64.b64decode(data["pdf_base64"])
            else:
                raise HTTPException(status_code=400, detail="Missing 'pdf_base64' in JSON body")
        else:
            # Raw binary PDF stream
            pdf_bytes = await request.body()

        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty PDF payload received")

        extracted_data = pdf_extractor.extract_floorplan_data(pdf_bytes)
        return {
            "status": "success",
            "message": "Floorplan parsed via PyMuPDF and OpenCV",
            "data": extracted_data
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(exc)}")
