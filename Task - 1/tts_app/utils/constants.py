"""
Constants and voice data for the TTS application.
"""

LANGUAGES = {
    "en-US": "English (US)",
    "en-GB": "English (UK)",
    "en-AU": "English (Australian)",
    "en-IN": "English (Indian)",
    "es-ES": "Spanish (Spain)",
    "es-US": "Spanish (US)",
    "fr-FR": "French (France)",
    "fr-CA": "French (Canada)",
    "de-DE": "German",
    "it-IT": "Italian",
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese (Portugal)",
    "hi-IN": "Hindi",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "zh-CN": "Chinese (Mandarin)",
    "ar-XA": "Arabic",
    "ru-RU": "Russian",
    "nl-NL": "Dutch",
    "pl-PL": "Polish",
    "tr-TR": "Turkish",
    "vi-VN": "Vietnamese",
    "th-TH": "Thai",
    "id-ID": "Indonesian",
}

VOICE_CONFIGS = {
    "en-US": {
        "FEMALE": ["en-US-Neural2-C", "en-US-Neural2-E", "en-US-Neural2-F", "en-US-Neural2-G", "en-US-Neural2-H"],
        "MALE": ["en-US-Neural2-A", "en-US-Neural2-D", "en-US-Neural2-I", "en-US-Neural2-J"],
    },
    "en-GB": {
        "FEMALE": ["en-GB-Neural2-A", "en-GB-Neural2-C", "en-GB-Neural2-F"],
        "MALE": ["en-GB-Neural2-B", "en-GB-Neural2-D"],
    },
    "en-AU": {
        "FEMALE": ["en-AU-Neural2-A", "en-AU-Neural2-C"],
        "MALE": ["en-AU-Neural2-B", "en-AU-Neural2-D"],
    },
    "en-IN": {
        "FEMALE": ["en-IN-Neural2-A", "en-IN-Neural2-D"],
        "MALE": ["en-IN-Neural2-B", "en-IN-Neural2-C"],
    },
    "es-ES": {
        "FEMALE": ["es-ES-Neural2-A", "es-ES-Neural2-C", "es-ES-Neural2-D", "es-ES-Neural2-E"],
        "MALE": ["es-ES-Neural2-B", "es-ES-Neural2-F"],
    },
    "es-US": {
        "FEMALE": ["es-US-Neural2-A"],
        "MALE": ["es-US-Neural2-B", "es-US-Neural2-C"],
    },
    "fr-FR": {
        "FEMALE": ["fr-FR-Neural2-A", "fr-FR-Neural2-C", "fr-FR-Neural2-E"],
        "MALE": ["fr-FR-Neural2-B", "fr-FR-Neural2-D"],
    },
    "fr-CA": {
        "FEMALE": ["fr-CA-Neural2-A", "fr-CA-Neural2-C", "fr-CA-Neural2-D"],
        "MALE": ["fr-CA-Neural2-B"],
    },
    "de-DE": {
        "FEMALE": ["de-DE-Neural2-A", "de-DE-Neural2-C", "de-DE-Neural2-F"],
        "MALE": ["de-DE-Neural2-B", "de-DE-Neural2-D"],
    },
    "it-IT": {
        "FEMALE": ["it-IT-Neural2-A"],
        "MALE": ["it-IT-Neural2-C"],
    },
    "pt-BR": {
        "FEMALE": ["pt-BR-Neural2-A", "pt-BR-Neural2-C"],
        "MALE": ["pt-BR-Neural2-B"],
    },
    "pt-PT": {
        "FEMALE": ["pt-PT-Neural2-A", "pt-PT-Neural2-C", "pt-PT-Neural2-D"],
        "MALE": ["pt-PT-Neural2-B"],
    },
    "hi-IN": {
        "FEMALE": ["hi-IN-Neural2-A", "hi-IN-Neural2-D"],
        "MALE": ["hi-IN-Neural2-B", "hi-IN-Neural2-C"],
    },
    "ja-JP": {
        "FEMALE": ["ja-JP-Neural2-B"],
        "MALE": ["ja-JP-Neural2-C", "ja-JP-Neural2-D"],
    },
    "ko-KR": {
        "FEMALE": ["ko-KR-Neural2-A", "ko-KR-Neural2-B"],
        "MALE": ["ko-KR-Neural2-C"],
    },
    "zh-CN": {
        "FEMALE": ["cmn-CN-Neural2-A", "cmn-CN-Neural2-D"],
        "MALE": ["cmn-CN-Neural2-B", "cmn-CN-Neural2-C"],
    },
    "ar-XA": {
        "FEMALE": ["ar-XA-Neural2-A"],
        "MALE": ["ar-XA-Neural2-B", "ar-XA-Neural2-C"],
    },
    "ru-RU": {
        "FEMALE": ["ru-RU-Neural2-A", "ru-RU-Neural2-C"],
        "MALE": ["ru-RU-Neural2-B", "ru-RU-Neural2-D"],
    },
    "nl-NL": {
        "FEMALE": ["nl-NL-Neural2-A", "nl-NL-Neural2-D", "nl-NL-Neural2-E"],
        "MALE": ["nl-NL-Neural2-B", "nl-NL-Neural2-C"],
    },
    "pl-PL": {
        "FEMALE": ["pl-PL-Neural2-A", "pl-PL-Neural2-C", "pl-PL-Neural2-D", "pl-PL-Neural2-E"],
        "MALE": ["pl-PL-Neural2-B"],
    },
    "tr-TR": {
        "FEMALE": ["tr-TR-Neural2-A", "tr-TR-Neural2-C", "tr-TR-Neural2-D", "tr-TR-Neural2-E"],
        "MALE": ["tr-TR-Neural2-B"],
    },
    "vi-VN": {
        "FEMALE": ["vi-VN-Neural2-A"],
        "MALE": ["vi-VN-Neural2-D"],
    },
    "th-TH": {
        "FEMALE": ["th-TH-Neural2-C"],
        "MALE": [],
    },
    "id-ID": {
        "FEMALE": ["id-ID-Neural2-A", "id-ID-Neural2-D"],
        "MALE": ["id-ID-Neural2-B", "id-ID-Neural2-C"],
    },
}

VOICE_TYPES = {
    "Standard": "Standard quality, faster processing",
    "WaveNet": "High quality AI voice",
    "Neural2": "Highest quality, most natural sounding",
}

SPEECH_RATE_MIN = 0.25
SPEECH_RATE_MAX = 4.0
SPEECH_RATE_DEFAULT = 1.0

PITCH_MIN = -20.0
PITCH_MAX = 20.0
PITCH_DEFAULT = 0.0

VOLUME_MIN = -96.0
VOLUME_MAX = 16.0
VOLUME_DEFAULT = 0.0

MAX_TEXT_LENGTH = 5000
MAX_CHARACTERS = 5000

AUDIO_ENCODINGS = {
    "MP3": "MP3",
    "LINEAR16": "WAV (16-bit)",
    "OGG_OPUS": "OGG Opus",
}

DEFAULT_AUDIO_ENCODING = "MP3"

SAMPLE_TEXTS = {
    "en-US": "Hello! Welcome to the Text-to-Speech application. This is a sample text to demonstrate the voice synthesis capabilities.",
    "en-GB": "Good day! Welcome to the Text-to-Speech application. This is a sample text to demonstrate the voice synthesis capabilities.",
    "en-IN": "Namaste! Welcome to the Text-to-Speech application. This is a sample text to demonstrate the voice synthesis capabilities.",
    "es-ES": "¡Hola! Bienvenido a la aplicación de texto a voz. Este es un texto de ejemplo para demostrar las capacidades de síntesis de voz.",
    "fr-FR": "Bonjour! Bienvenue dans l'application de synthèse vocale. Ceci est un exemple de texte pour démontrer les capacités de synthèse vocale.",
    "de-DE": "Hallo! Willkommen bei der Text-to-Speech-Anwendung. Dies ist ein Beispieltext, um die Sprachsynthesefähigkeiten zu demonstrieren.",
    "hi-IN": "नमस्ते! टेक्स्ट-टू-स्पीच एप्लिकेशन में आपका स्वागत है। यह वॉइस सिंथेसिस क्षमताओं को प्रदर्शित करने के लिए एक नमूना पाठ है।",
    "ja-JP": "こんにちは！テキスト読み上げアプリケーションへようこそ。これは音声合成機能を実演するためのサンプルテキストです。",
    "default": "Hello! Welcome to the Text-to-Speech application. This is a sample text to demonstrate the voice synthesis capabilities.",
}
