"""
Text-to-Speech Engine using Google Cloud Text-to-Speech API.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import texttospeech
from google.oauth2 import service_account


class TextToSpeechEngine:
    """
    A wrapper class for Google Cloud Text-to-Speech API.
    
    Provides methods to synthesize speech from text with various
    voice options, speech rate, pitch, and volume controls.
    """
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the TTS engine with Google Cloud credentials.
        
        Args:
            credentials_path: Path to the Google Cloud service account JSON file.
                            If None, uses GOOGLE_APPLICATION_CREDENTIALS env var.
        """
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        else:
            self.client = texttospeech.TextToSpeechClient()
    
    def list_voices(self, language_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available voices, optionally filtered by language.
        
        Args:
            language_code: Optional language code to filter voices (e.g., 'en-US').
        
        Returns:
            List of voice information dictionaries.
        """
        request = texttospeech.ListVoicesRequest(language_code=language_code or "")
        response = self.client.list_voices(request=request)
        
        voices = []
        for voice in response.voices:
            voice_info = {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
            voices.append(voice_info)
        
        return voices
    
    def synthesize_speech(
        self,
        text: str,
        language_code: str = "en-US",
        voice_name: Optional[str] = None,
        voice_gender: str = "NEUTRAL",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume_gain_db: float = 0.0,
        audio_encoding: str = "MP3",
    ) -> bytes:
        """
        Convert text to speech audio.
        
        Args:
            text: The text to convert to speech.
            language_code: Language code (e.g., 'en-US', 'es-ES').
            voice_name: Specific voice name (e.g., 'en-US-Neural2-D').
                       If None, uses default voice for the language.
            voice_gender: Voice gender - 'MALE', 'FEMALE', or 'NEUTRAL'.
            speaking_rate: Speed of speech (0.25 to 4.0, default 1.0).
            pitch: Voice pitch in semitones (-20.0 to 20.0, default 0.0).
            volume_gain_db: Volume gain in dB (-96.0 to 16.0, default 0.0).
            audio_encoding: Audio format - 'MP3', 'LINEAR16', or 'OGG_OPUS'.
        
        Returns:
            Audio content as bytes.
        
        Raises:
            ValueError: If parameters are out of valid ranges.
            google.api_core.exceptions.GoogleAPIError: If API call fails.
        """
        if not 0.25 <= speaking_rate <= 4.0:
            raise ValueError("speaking_rate must be between 0.25 and 4.0")
        if not -20.0 <= pitch <= 20.0:
            raise ValueError("pitch must be between -20.0 and 20.0")
        if not -96.0 <= volume_gain_db <= 16.0:
            raise ValueError("volume_gain_db must be between -96.0 and 16.0")
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        gender_map = {
            "MALE": texttospeech.SsmlVoiceGender.MALE,
            "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
            "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
        }
        ssml_gender = gender_map.get(voice_gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)
        
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=ssml_gender,
        )
        
        if voice_name:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
            )
        
        encoding_map = {
            "MP3": texttospeech.AudioEncoding.MP3,
            "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }
        audio_encoding_enum = encoding_map.get(audio_encoding, texttospeech.AudioEncoding.MP3)
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding_enum,
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume_gain_db=volume_gain_db,
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        
        return response.audio_content
    
    def synthesize_ssml(
        self,
        ssml: str,
        language_code: str = "en-US",
        voice_name: Optional[str] = None,
        voice_gender: str = "NEUTRAL",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume_gain_db: float = 0.0,
        audio_encoding: str = "MP3",
    ) -> bytes:
        """
        Convert SSML to speech audio.
        
        Args:
            ssml: SSML markup to convert to speech.
            Other args same as synthesize_speech.
        
        Returns:
            Audio content as bytes.
        """
        if not 0.25 <= speaking_rate <= 4.0:
            raise ValueError("speaking_rate must be between 0.25 and 4.0")
        if not -20.0 <= pitch <= 20.0:
            raise ValueError("pitch must be between -20.0 and 20.0")
        if not -96.0 <= volume_gain_db <= 16.0:
            raise ValueError("volume_gain_db must be between -96.0 and 16.0")
        
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        
        gender_map = {
            "MALE": texttospeech.SsmlVoiceGender.MALE,
            "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
            "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
        }
        ssml_gender = gender_map.get(voice_gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL)
        
        if voice_name:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
            )
        else:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=ssml_gender,
            )
        
        encoding_map = {
            "MP3": texttospeech.AudioEncoding.MP3,
            "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }
        audio_encoding_enum = encoding_map.get(audio_encoding, texttospeech.AudioEncoding.MP3)
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=audio_encoding_enum,
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume_gain_db=volume_gain_db,
        )
        
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        
        return response.audio_content
    
    @staticmethod
    def save_audio(audio_content: bytes, filepath: str) -> str:
        """
        Save audio content to a file.
        
        Args:
            audio_content: Audio data as bytes.
            filepath: Path to save the audio file.
        
        Returns:
            The filepath where audio was saved.
        """
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(filepath, "wb") as audio_file:
            audio_file.write(audio_content)
        
        return filepath


if __name__ == "__main__":
    engine = TextToSpeechEngine("credentials.json")
    
    voices = engine.list_voices("en-US")
    print("Available English (US) voices:")
    for voice in voices[:5]:
        print(f"  - {voice['name']} ({voice['gender']})")
    
    text = "Hello! This is a test of the Google Cloud Text-to-Speech API."
    audio = engine.synthesize_speech(
        text=text,
        language_code="en-US",
        voice_name="en-US-Neural2-D",
        speaking_rate=1.0,
        pitch=0.0,
    )
    
    output_path = engine.save_audio(audio, "output/test_speech.mp3")
    print(f"Audio saved to: {output_path}")
