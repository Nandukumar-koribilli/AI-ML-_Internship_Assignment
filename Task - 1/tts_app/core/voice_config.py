"""
Voice configuration utilities for the TTS application.
"""

from typing import List, Dict, Optional, Tuple
from ..utils.constants import LANGUAGES, VOICE_CONFIGS


class VoiceConfig:
    """
    Utility class for managing voice configurations.
    """
    
    @staticmethod
    def get_languages() -> Dict[str, str]:
        """
        Get all available languages.
        
        Returns:
            Dictionary of language codes to display names.
        """
        return LANGUAGES.copy()
    
    @staticmethod
    def get_language_name(language_code: str) -> str:
        """
        Get the display name for a language code.
        
        Args:
            language_code: Language code (e.g., 'en-US').
        
        Returns:
            Language display name or the code if not found.
        """
        return LANGUAGES.get(language_code, language_code)
    
    @staticmethod
    def get_voices_for_language(language_code: str) -> Dict[str, List[str]]:
        """
        Get available voices for a language grouped by gender.
        
        Args:
            language_code: Language code (e.g., 'en-US').
        
        Returns:
            Dictionary with 'MALE' and 'FEMALE' keys containing voice lists.
        """
        return VOICE_CONFIGS.get(language_code, {"MALE": [], "FEMALE": []})
    
    @staticmethod
    def get_voices_by_gender(language_code: str, gender: str) -> List[str]:
        """
        Get voices for a specific language and gender.
        
        Args:
            language_code: Language code (e.g., 'en-US').
            gender: 'MALE' or 'FEMALE'.
        
        Returns:
            List of voice names.
        """
        voices = VOICE_CONFIGS.get(language_code, {})
        return voices.get(gender.upper(), [])
    
    @staticmethod
    def get_default_voice(language_code: str, gender: str = "MALE") -> Optional[str]:
        """
        Get the default voice for a language and gender.
        
        Args:
            language_code: Language code (e.g., 'en-US').
            gender: 'MALE' or 'FEMALE'.
        
        Returns:
            Default voice name or None if not found.
        """
        voices = VoiceConfig.get_voices_by_gender(language_code, gender)
        return voices[0] if voices else None
    
    @staticmethod
    def get_available_genders(language_code: str) -> List[str]:
        """
        Get available genders for a language.
        
        Args:
            language_code: Language code.
        
        Returns:
            List of available genders ('MALE', 'FEMALE').
        """
        voices = VOICE_CONFIGS.get(language_code, {})
        available = []
        if voices.get("MALE"):
            available.append("MALE")
        if voices.get("FEMALE"):
            available.append("FEMALE")
        return available if available else ["NEUTRAL"]
    
    @staticmethod
    def is_valid_voice(language_code: str, voice_name: str) -> bool:
        """
        Check if a voice name is valid for a language.
        
        Args:
            language_code: Language code.
            voice_name: Voice name to validate.
        
        Returns:
            True if valid, False otherwise.
        """
        voices = VOICE_CONFIGS.get(language_code, {})
        all_voices = voices.get("MALE", []) + voices.get("FEMALE", [])
        return voice_name in all_voices
    
    @staticmethod
    def get_voice_info(voice_name: str) -> Dict[str, str]:
        """
        Parse voice name to extract information.
        
        Args:
            voice_name: Voice name (e.g., 'en-US-Neural2-D').
        
        Returns:
            Dictionary with language, type, and variant info.
        """
        parts = voice_name.split("-")
        if len(parts) >= 4:
            return {
                "language": f"{parts[0]}-{parts[1]}",
                "type": parts[2],
                "variant": parts[3],
            }
        return {"language": "", "type": "", "variant": ""}
    
    @staticmethod
    def format_voice_display(voice_name: str) -> str:
        """
        Format voice name for display.
        
        Args:
            voice_name: Voice name (e.g., 'en-US-Neural2-D').
        
        Returns:
            Formatted display string.
        """
        info = VoiceConfig.get_voice_info(voice_name)
        if info["type"] and info["variant"]:
            return f"{info['type']} Voice {info['variant']}"
        return voice_name


class VoicePreset:
    """
    Predefined voice presets for common use cases.
    """
    
    PRESETS = {
        "professional_male_us": {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-D",
            "speaking_rate": 1.0,
            "pitch": -2.0,
            "description": "Professional male voice (US)",
        },
        "professional_female_us": {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-C",
            "speaking_rate": 1.0,
            "pitch": 0.0,
            "description": "Professional female voice (US)",
        },
        "professional_male_uk": {
            "language_code": "en-GB",
            "voice_name": "en-GB-Neural2-D",
            "speaking_rate": 0.95,
            "pitch": -1.0,
            "description": "Professional male voice (UK)",
        },
        "professional_female_uk": {
            "language_code": "en-GB",
            "voice_name": "en-GB-Neural2-A",
            "speaking_rate": 0.95,
            "pitch": 0.0,
            "description": "Professional female voice (UK)",
        },
        "narrator": {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-D",
            "speaking_rate": 0.85,
            "pitch": -4.0,
            "description": "Deep narrator voice",
        },
        "energetic": {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-J",
            "speaking_rate": 1.2,
            "pitch": 2.0,
            "description": "Energetic, upbeat voice",
        },
        "calm": {
            "language_code": "en-US",
            "voice_name": "en-US-Neural2-C",
            "speaking_rate": 0.8,
            "pitch": -1.0,
            "description": "Calm, soothing voice",
        },
    }
    
    @classmethod
    def get_preset(cls, preset_name: str) -> Optional[Dict]:
        """Get a voice preset by name."""
        return cls.PRESETS.get(preset_name)
    
    @classmethod
    def list_presets(cls) -> List[Tuple[str, str]]:
        """List all available presets with descriptions."""
        return [(name, preset["description"]) for name, preset in cls.PRESETS.items()]
