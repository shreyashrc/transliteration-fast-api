from typing import Optional, Tuple
import re
from indic_transliteration import sanscript
from indic_transliteration.detect import detect
import logging

# Try to import the Hinglish dictionary
try:
    from app.data.hinglish_dict import WORD_REPLACEMENTS, CONTEXT_REPLACEMENTS
except ImportError:
    # Define fallback dictionaries if import fails
    WORD_REPLACEMENTS = {
        "mobile": "mobile",
        "phone": "phone",
    }
    CONTEXT_REPLACEMENTS = {
        r"\bmobA?i?l[ae]?\b": "mobile",
        r"\bf[ao]n[ae]?\b": "phone",
    }

logger = logging.getLogger(__name__)

# Mapping between language names and their codes
LANGUAGE_MAP = {
    "hindi": "hi",
    "marathi": "mr",
    "sanskrit": "sa",
    "bengali": "bn",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "oriya": "or",
    "punjabi": "pa",
    "tamil": "ta",
    "telugu": "te",
}

# Scheme mapping
SCHEME_MAP = {
    "iast": sanscript.IAST,
    "hk": sanscript.HK,
    "slp1": sanscript.SLP1,
    "itrans": sanscript.ITRANS,
    "velthuis": sanscript.VELTHUIS,
    "wx": sanscript.WX,
    "kolkata": sanscript.KOLKATA,
}

# Post-processing rules to make transliteration more "Hinglish"-like
HINGLISH_RULES = [
    # Capitalize first letter of sentences
    (r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper()),
    
    # Capitalize proper nouns (simplified approach)
    (r'\b([a-z][a-z]+)([a-z][a-z]+)\b', 
     lambda m: m.group(1).capitalize() + m.group(2) if len(m.group(1)) > 2 else m.group(0)),
     
    # Fix spacing after punctuation
    (r'([.!?,;:])([a-zA-Z])', r'\1 \2'),
    
    # Preserve original spacing for question marks, etc.
    (r'\s+([.!?,;:])', r'\1'),
    
    # Convert ā (long a) to aa
    (r'ā', 'aa'),
    
    # Convert ī (long i) to i or ee based on context
    (r'ī', 'ee'),
    
    # Convert ū (long u) to u or oo based on context
    (r'ū', 'oo'),
    
    # Convert ṃ (anusvara) to m or n depending on following consonant
    (r'ṃ([kg])', r'n\1'),  # before gutturals
    (r'ṃ([cj])', r'n\1'),  # before palatals
    (r'ṃ([tdsn])', r'n\1'),  # before dentals
    (r'ṃ([pb])', r'm\1'),  # before labials
    (r'ṃ', 'm'),  # default
    
    # Convert ṅ, ñ, ṇ, n, m (various nasals) to n or m
    (r'[ṅñṇ]', 'n'),
    
    # Convert ś, ṣ (palatal and retroflex s) to sh
    (r'[śṣ]', 'sh'),
    
    # Convert ṛ (vocalic r) to ri
    (r'ṛ', 'ri'),
    
    # Convert ḍ, ḍh, ṭ, ṭh (retroflex consonants) to d, dh, t, th
    (r'ḍh', 'dh'),
    (r'ḍ', 'd'),
    (r'ṭh', 'th'),
    (r'ṭ', 't'),
    
    # Remove diacritical h after consonants that don't need it in English
    (r'([^cgpt])h', r'\1'),
    
    # Fix common combinations
    (r'ai', 'ai'),
    (r'au', 'au'),
]


class TransliterationService:
    """Service for transliterating text from Indian languages to Roman script"""
    
    @staticmethod
    def detect_source_language(text: str) -> Optional[str]:
        """
        Detect the source language of the given text
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected language name or None if detection failed
        """
        try:
            # Using the detect.detect method to identify the script
            detected_script = detect.detect(text)
            
            # Map the detected script to language name
            if detected_script == sanscript.DEVANAGARI:
                # This is a simplification - we'd need a proper Language Detection model
                # logic to differentiate Hindi/Marathi/Sanskrit
                return "hindi"  # Default to Hindi
            return None
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return None
    
    @staticmethod
    def transliterate_to_hinglish(text: str) -> str:
        """
        Custom transliteration function specifically for Hindi/Marathi to Hinglish
        that produces more natural Romanized text without diacritics
        
        Args:
            text: Text in Devanagari script
            
        Returns:
            Transliterated text in natural Hinglish style
        """
        base_transliterated = sanscript.transliterate(
            text, 
            sanscript.DEVANAGARI, 
            sanscript.ITRANS
        )
        
        for word, replacement in WORD_REPLACEMENTS.items():
            base_transliterated = re.sub(r'\b' + word + r'\b', 
                                    replacement, 
                                    base_transliterated, 
                                    flags=re.IGNORECASE)
            
        for pattern, replacement in CONTEXT_REPLACEMENTS.items():
            base_transliterated = re.sub(pattern, replacement, base_transliterated, flags=re.IGNORECASE)
        
        for word, replacement in WORD_REPLACEMENTS.items():
            base_transliterated = re.sub(r'\b' + word + r'\b', 
                                     replacement, 
                                     base_transliterated, 
                                     flags=re.IGNORECASE)
            
        for pattern, replacement in CONTEXT_REPLACEMENTS.items():
            base_transliterated = re.sub(pattern, replacement, base_transliterated, flags=re.IGNORECASE)
            
        conversions = [
            (r'aa', 'a'),      # Sometimes single 'a' looks more natural
            (r'A', 'a'),       # Normalize A to a
            (r'I', 'i'),       # Normalize I to i
            (r'U', 'u'),       # Normalize U to u
            (r'RR', 'ri'),     # Convert vocalic R to ri
            (r'chh', 'ch'),    # Simplify chh to ch in most cases
            (r'shh', 'sh'),    # Simplify shh to sh
            (r'Sh', 'sh'),     # Normalize retroflex sh
            (r'\.n', 'n'),     # Simplify dots
            (r'\.m', 'm'),     # Simplify dots
            (r'~N', 'n'),      # Normalize to n
            (r'~n', 'n'),      # Normalize to n
            (r'N\^', 'n'),     # Normalize to n
            (r'ph', 'f'),      # In many cases, ph sounds like f in Hinglish
        ]
        
        for pattern, replacement in conversions:
            base_transliterated = re.sub(pattern, replacement, base_transliterated)
        
        for pattern, replacement in conversions:
            base_transliterated = re.sub(pattern, replacement, base_transliterated)
        
        base_transliterated = re.sub(r'(^|[.!?]\s+)([a-z])', 
                                  lambda m: m.group(1) + m.group(2).upper(), 
                                  base_transliterated)
        
        base_transliterated = base_transliterated.replace("'", "")
        
        return base_transliterated

    @staticmethod
    def transliterate(
        text: str, 
        source_language: Optional[str] = None,
        scheme: str = "itrans"
    ) -> Tuple[str, str, Optional[str]]:
        """
        Transliterate text from Devanagari to Roman script
        
        Args:
            text: Text to transliterate
            source_language: Source language (optional)
            scheme: Transliteration scheme to use
            
        Returns:
            Tuple of (transliterated_text, source_language, detected_language)
        """
        detected_language = None
        
        if not source_language:
            detected_language = TransliterationService.detect_source_language(text)
            source_language = detected_language or "hindi"  # Default to Hindi
                
        try:
            # Use our custom Hinglish transliteration instead of standard schemes
            transliterated = TransliterationService.transliterate_to_hinglish(text)
            
            # Apply post-processing for Hinglish style
            for pattern, replacement in HINGLISH_RULES:
                if callable(replacement):
                    transliterated = re.sub(pattern, replacement, transliterated)
                else:
                    transliterated = re.sub(pattern, replacement, transliterated)
            
            # Additional cleanup for Hinglish style
            # Convert double vowels to single in some common cases
            transliterated = re.sub(r'([aeiou])\1', r'\1', transliterated)
            
            # Fix common phone-related terms
            transliterated = re.sub(r'\bmoba[a]?il[a]?\b', 'mobile', transliterated, flags=re.IGNORECASE)
            transliterated = re.sub(r'\bphon[a]?\b', 'phone', transliterated, flags=re.IGNORECASE)
            
            return transliterated, source_language, detected_language
            
        except Exception as e:
            logger.error(f"Transliteration failed: {e}")
            return text, source_language, detected_language  # Return original text on failure