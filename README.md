# Hindi/Marathi to Hinglish Transliteration API

A FastAPI-based application that transliterates text from Devanagari script (Hindi/Marathi) to Roman script (Hinglish), preserving pronunciation.

## Features

- Transliterate Hindi/Marathi text to Hinglish (Romanized form)
- Auto-detection of source language (based on script)
- Support for different transliteration schemes (IAST, Harvard-Kyoto, etc.)
- Batch transliteration for multiple texts
- Optional database storage for transliteration history
- RESTful API design

## Example

Input:

```
कसा आहेस श्रेयश ?
```

Output:

```
Kasa aahes Shreyash?
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/hinglish-transliteration-api.git
   cd hinglish-transliteration-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python -m app.main
   ```

5. Open your browser or API client and navigate to:
   ```
   http://localhost:8000/docs
   ```

## API Usage

### Transliterate Single Text

**Endpoint:** `POST /api/transliteration/`

**Request:**

```json
{
  "text": "कसा आहेस श्रेयश ?",
  "source_language": "marathi",
  "scheme": "iast"
}
```

**Response:**

```json
{
  "input_text": "कसा आहेस श्रेयश ?",
  "transliterated_text": "Kasa aahes Shreyash?",
  "source_language": "marathi",
  "detected_language": null
}
```

### Batch Transliteration

**Endpoint:** `POST /api/transliteration/batch`

**Request:**

```json
{
  "texts": [
    {
      "text": "कसा आहेस श्रेयश ?",
      "source_language": "marathi"
    },
    {
      "text": "नमस्ते दुनिया",
      "source_language": "hindi"
    }
  ]
}
```

**Response:**

```json
{
  "results": [
    {
      "input_text": "कसा आहेस श्रेयश ?",
      "transliterated_text": "Kasa aahes Shreyash?",
      "source_language": "marathi",
      "detected_language": null
    },
    {
      "input_text": "नमस्ते दुनिया",
      "transliterated_text": "Namaste duniya",
      "source_language": "hindi",
      "detected_language": null
    }
  ]
}
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **indic-transliteration**: Core library for transliteration
- **SQLAlchemy**: ORM for database interactions (optional)
- **Uvicorn**: ASGI server for running the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
