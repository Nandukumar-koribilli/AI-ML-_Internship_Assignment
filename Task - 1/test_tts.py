"""
Test script for the TTS Engine.
"""

from tts_app.core.tts_engine import TextToSpeechEngine

def test_tts_engine():
    print("Initializing TTS Engine...")
    engine = TextToSpeechEngine("credentials.json")

    print("Listing English US voices...")
    voices = engine.list_voices("en-US")
    print(f"Found {len(voices)} voices")

    for voice in voices[:5]:
        print(f"  - {voice['name']} ({voice['gender']})")

    print()
    print("Generating test speech...")
    audio = engine.synthesize_speech(
        text="Hello! This is a test of the Google Cloud Text to Speech API.",
        language_code="en-US",
        voice_name="en-US-Neural2-D",
        speaking_rate=1.0,
        pitch=0.0
    )

    output_path = engine.save_audio(audio, "output/test_speech.mp3")
    print(f"Audio saved to: {output_path}")
    print(f"Audio size: {len(audio)} bytes")
    print("TTS Engine test completed successfully!")


if __name__ == "__main__":
    test_tts_engine()
