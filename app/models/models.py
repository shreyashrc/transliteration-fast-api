from pydantic import BaseModel, Field
from typing import Optional, List


class TransliterationRequest(BaseModel):
    """Request model for transliteration endpoint"""
    text: str = Field(..., description="The text to transliterate")
    source_language: Optional[str] = Field(
        None, 
        description="Source language (hindi, marathi, etc.). If not provided, auto-detection will be attempted."
    )
    scheme: Optional[str] = Field(
        "itrans", 
        description="Transliteration scheme to use (iast, hk, slp1, itrans, etc.)"
    )


class TransliterationResponse(BaseModel):
    input_text: str = Field(..., description="Original input text")
    transliterated_text: str = Field(..., description="Transliterated text")
    source_language: str = Field(..., description="Source language used for transliteration")
    detected_language: Optional[str] = Field(
        None, 
        description="Detected language (if auto-detection was used)"
    )


class BatchTransliterationRequest(BaseModel):
    texts: List[TransliterationRequest] = Field(..., description="List of texts to transliterate")


class BatchTransliterationResponse(BaseModel):
    results: List[TransliterationResponse] = Field(..., description="Transliteration results")