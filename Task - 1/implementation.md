# Text-to-Speech (TTS) Application Implementation 

A comprehensive Text-to-Speech application using **Google Cloud Text-to-Speech API** with voice customization, speech controls, and a Streamlit web interface.


> [!IMPORTANT]
> **Google Cloud Setup Required**: You'll need to:
> 1. Create a Google Cloud Project
> 2. Enable the Text-to-Speech API
> 3. Create a Service Account and download the JSON key file
> 4. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
>
> I'll provide detailed setup instructions in the README.
---

### Project Structure

```
c:\Users\nandu\Downloads\internship\
├── tts_app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── tts_engine.py      # Core TTS with Google Cloud API
│   │   ├── voice_config.py    # Voice customization (male/female, accents)
│   │   └── audio_processor.py # Volume adjustment with pydub
│   ├── validation/
│   │   ├── __init__.py
│   │   └── text_validator.py  # Text validation logic
│   └── utils/
│       ├── __init__.py
│       └── constants.py       # Available voices, languages
├── tests/
│   ├── __init__.py
│   └── test_text_validator.py # Unit tests for validation
├── output/                    # Generated audio files
├── app.py                     # Streamlit web application
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # Setup instructions
```

---

### Core Components

[requirements.txt]
```
google-cloud-texttospeech>=2.16.0
streamlit>=1.29.0
pydub>=0.25.1
python-dotenv>=1.0.0
pytest>=7.4.0
```

---

**Voice Types Available:**
| Type | Quality | Free Tier |
|------|---------|-----------|
| Standard | Good | 4M chars/month |
| WaveNet | High (AI-generated) | 1M chars/month |
| Neural2 | Highest (latest AI) | 1M chars/month |

---

 [voice_config.py]
Voice configuration with male/female options:

**English Voices (examples):**
| Voice Name | Gender | Type | Accent |
|------------|--------|------|--------|
| en-US-Neural2-A | FEMALE | Neural2 | American |
| en-US-Neural2-D | MALE | Neural2 | American |
| en-GB-Neural2-A | FEMALE | Neural2 | British |
| en-GB-Neural2-D | MALE | Neural2 | British |
| en-AU-Neural2-A | FEMALE | Neural2 | Australian |
| en-AU-Neural2-B | MALE | Neural2 | Australian |
| en-IN-Neural2-A | FEMALE | Neural2 | Indian |
| en-IN-Neural2-B | MALE | Neural2 | Indian |

**Other Languages:**
- Spanish (es-ES, es-US)
- French (fr-FR, fr-CA)
- German (de-DE)
- Hindi (hi-IN)
- Japanese (ja-JP)
- And 40+ more languages

---

[audio_processor.py]
Additional audio processing with pydub:
- Post-synthesis volume adjustment
- Audio format conversion (MP3, WAV, OGG)
- Audio normalization

---

### Validation Component

[text_validator.py]
```python
class TextValidator:
    MAX_LENGTH = 5000  # Google Cloud limit per request
    
    def validate(text: str) -> ValidationResult
    def sanitize(text: str) -> str
    def handle_special_characters(text: str) -> str
    def normalize_unicode(text: str) -> str
```

**Validation Rules:**
- Maximum 5000 bytes per request (Google Cloud limit)
- Handle special characters (emojis, symbols)
- Normalize Unicode characters
- Strip excessive whitespace
- Reject empty input

[test_text_validator.py]
Unit tests:
- `test_empty_text_validation`
- `test_max_length_validation`
- `test_special_character_handling`
- `test_unicode_normalization`
- `test_whitespace_handling`
- `test_valid_text_passes`

---

### Web Application

[app.py]
Premium Streamlit web application:

**Features:**
1. **Text Input Section**
   - Large text area with character counter
   - Real-time validation feedback
   - Sample text buttons for quick testing

2. **Voice Selection Panel**
   - Language dropdown (50+ languages)
   - Voice type selector (Standard/WaveNet/Neural2)
   - Gender selector (Male/Female)
   - Voice preview with sample phrase

3. **Speech Controls**
   - Speaking Rate slider (0.25x - 4.0x)
   - Pitch slider (-20 to +20 semitones)
   - Volume slider (-96dB to +16dB)

4. **Output Section**
   - Generate Speech button with loading animation
   - Built-in audio player for browser playback
   - Download button (MP3 format)
   - Audio waveform visualization

**Design:**
- Dark theme with gradient accents
- Glassmorphism cards
- Smooth animations
- Mobile-responsive layout

---

## Setup Instructions (for README)

### 1. Google Cloud Setup
```bash
# 1. Go to Google Cloud Console: https://console.cloud.google.com
# 2. Create a new project or select existing
# 3. Enable Text-to-Speech API:
#    APIs & Services > Library > Search "Text-to-Speech" > Enable

# 4. Create Service Account:
#    IAM & Admin > Service Accounts > Create Service Account
#    - Name: tts-app-service
#    - Role: Cloud Text-to-Speech API User
#    - Create Key (JSON) > Download

# 5. Set environment variable (PowerShell):
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## Verification Plan

### Automated Tests
```bash
# Run unit tests
pytest tests/ -v

# Test with coverage
pytest tests/ --cov=tts_app
```

### Manual Verification
1. ✅ Generate speech with sample text
2. ✅ Test male and female voice options
3. ✅ Test different accents (US, UK, Australian, Indian)
4. ✅ Verify speech rate adjustment (slow to fast)
5. ✅ Verify pitch adjustment
6. ✅ Verify volume control
7. ✅ Test audio playback in browser
8. ✅ Test audio file download
9. ✅ Validate error handling for invalid input
10. ✅ Test maximum text length handling

---

## API Reference

### Speech Rate
- **Range**: 0.25 to 4.0
- **Default**: 1.0
- **0.5** = Half speed (slower)
- **2.0** = Double speed (faster)

### Pitch
- **Range**: -20.0 to 20.0 semitones
- **Default**: 0.0
- **Negative** = Lower pitch
- **Positive** = Higher pitch

### Volume Gain
- **Range**: -96.0 to 16.0 dB
- **Default**: 0.0
- **Negative** = Quieter
- **Positive** = Louder (may clip)
