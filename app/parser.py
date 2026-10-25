import io
from pypdf import PdfReader
from fastapi import HTTPException


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from raw PDF bytes in memory.

    Raises HTTPException(400) if parsing fails or no text is extracted.
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        full_text = "\n".join(extracted_text).strip()
        if not full_text:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF contains no readable text or is an image scan.",
            )
        return full_text
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Failed to process PDF: {str(exc)}"
        )