"""
Hinglish Dictionary - Common word mappings for improved transliteration
"""

# Common Hindi/Marathi to natural Hinglish word mappings
WORD_REPLACEMENTS = {
    # Hindi common words with natural Hinglish spellings
    "nahin": "nahi",
    "hai": "hai",
    "hain": "hain",
    "kya": "kya",
    "kyaa": "kya",
    "aap": "aap",
    "tum": "tum",
    "kaise": "kaise",
    "kaisa": "kaisa",
    "achha": "accha",
    "accha": "accha",
    "achcha": "accha",
    "achaa": "accha",
    "theek": "theek",
    "thik": "theek",
    "dhanyavaad": "dhanyavad",
    "namaste": "namaste",
    "namaskar": "namaskar",
    "kahan": "kahan",
    "kahaan": "kahan",
    "yahan": "yahan",
    "yahaan": "yahan",
    "vahan": "vahan",
    "vahaan": "vahan",
    "bahut": "bahut",
    "bharat": "bharat",
    "desh": "desh",
    "videsh": "videsh",
    "shaam": "sham",
    "subah": "subah",
    "raat": "raat",
    "din": "din",
    "dopahar": "dopahar",
    
    # Marathi common words with natural Hinglish spellings
    "kasa": "kasa",
    "kasaa": "kasa",
    "aahes": "ahes",
    "aahe": "ahe",
    "tumhi": "tumhi",
    "mi": "mi",
    "mee": "mi",
    "aaj": "aaj",
    "udya": "udya",
    "kal": "kal",
    "dhanyavad": "dhanyavad",
    
    # Technology terms
    "mobile": "mobile",
    "mobail": "mobile",
    "fon": "phone",
    "phon": "phone",
    "computer": "computer",
    "kompyuter": "computer",
    "internet": "internet",
    "inTaranet": "internet",
    "website": "website",
    "vebsait": "website",
    "email": "email",
    "imela": "email",
    
    # Names and places - common transliterations
    "mumbai": "mumbai",
    "dilli": "delhi",
    "kolkata": "kolkata",
    "bangalore": "bangalore",
    "bengaluru": "bengaluru",
    "hyderabad": "hyderabad",
    "bharat": "bharat",
    "india": "india",
}

# Term replacements for specific contexts
CONTEXT_REPLACEMENTS = {
    # Patterns that should be handled in context
    r"\bmobA?i?l[ae]?\b": "mobile",
    r"\bf[ao]n[ae]?\b": "phone",
    r"\bph[ao]n[ae]?\b": "phone",
    r"\bkompyuTar\b": "computer",
    r"\bk[ao]mpyuter\b": "computer",
}