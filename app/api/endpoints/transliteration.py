from fastapi import APIRouter, HTTPException
from app.models.models import (
    TransliterationRequest,
    TransliterationResponse,
    BatchTransliterationRequest,
    BatchTransliterationResponse
)
from app.services.transliteration import TransliterationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transliteration", tags=["transliteration"])


@router.post("/", response_model=TransliterationResponse)
async def transliterate_text(request: TransliterationRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    try:
        transliterated_text, source_language, detected_language = TransliterationService.transliterate(
            text=request.text,
            source_language=request.source_language,
            scheme=request.scheme
        )
        
        return TransliterationResponse(
            input_text=request.text,
            transliterated_text=transliterated_text,
            source_language=source_language,
            detected_language=detected_language
        )
    except Exception as e:
        logger.error(f"Transliteration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transliteration failed: {str(e)}")


@router.post("/batch", response_model=BatchTransliterationResponse)
async def transliterate_batch(request: BatchTransliterationRequest):

    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided for transliteration")
    
    results = []
    
    for item in request.texts:
        try:
            transliterated_text, source_language, detected_language = TransliterationService.transliterate(
                text=item.text,
                source_language=item.source_language,
                scheme=item.scheme or "iast"
            )
            
            results.append(TransliterationResponse(
                input_text=item.text,
                transliterated_text=transliterated_text,
                source_language=source_language,
                detected_language=detected_language
            ))
        except Exception as e:
            logger.error(f"Batch transliteration failed for text '{item.text[:20]}...': {e}")
            results.append(TransliterationResponse(
                input_text=item.text,
                transliterated_text=item.text,  # Return original on failure
                source_language=item.source_language or "unknown",
                detected_language=None
            ))
    
    return BatchTransliterationResponse(results=results)