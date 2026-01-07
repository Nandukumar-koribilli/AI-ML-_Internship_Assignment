"""
Audio processing utilities for the TTS application.
Uses pydub for additional audio manipulation.
"""

import io
from typing import Optional
from pydub import AudioSegment


class AudioProcessor:
    """
    Audio processing utilities for post-synthesis manipulation.
    """
    
    @staticmethod
    def adjust_volume(audio_bytes: bytes, volume_change_db: float, format: str = "mp3") -> bytes:
        """
        Adjust the volume of audio.
        
        Args:
            audio_bytes: Audio content as bytes.
            volume_change_db: Volume change in dB (positive = louder, negative = quieter).
            format: Audio format ('mp3', 'wav', 'ogg').
        
        Returns:
            Processed audio as bytes.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        adjusted_audio = audio + volume_change_db
        output_buffer = io.BytesIO()
        adjusted_audio.export(output_buffer, format=format)
        return output_buffer.getvalue()
    
    @staticmethod
    def change_speed(audio_bytes: bytes, speed_factor: float, format: str = "mp3") -> bytes:
        """
        Change the playback speed of audio.
        
        Note: This changes both speed and pitch. For pitch-preserved speed change,
        more advanced processing would be needed.
        
        Args:
            audio_bytes: Audio content as bytes.
            speed_factor: Speed multiplier (e.g., 1.5 = 50% faster).
            format: Audio format.
        
        Returns:
            Processed audio as bytes.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        new_frame_rate = int(audio.frame_rate * speed_factor)
        adjusted_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": new_frame_rate
        })
        adjusted_audio = adjusted_audio.set_frame_rate(audio.frame_rate)
        output_buffer = io.BytesIO()
        adjusted_audio.export(output_buffer, format=format)
        return output_buffer.getvalue()
    
    @staticmethod
    def normalize_audio(audio_bytes: bytes, target_dbfs: float = -20.0, format: str = "mp3") -> bytes:
        """
        Normalize audio to a target dBFS level.
        
        Args:
            audio_bytes: Audio content as bytes.
            target_dbfs: Target dBFS level (default -20.0).
            format: Audio format.
        
        Returns:
            Normalized audio as bytes.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        change_db = target_dbfs - audio.dBFS
        normalized_audio = audio + change_db
        output_buffer = io.BytesIO()
        normalized_audio.export(output_buffer, format=format)
        return output_buffer.getvalue()
    
    @staticmethod
    def convert_format(audio_bytes: bytes, from_format: str, to_format: str) -> bytes:
        """
        Convert audio from one format to another.
        
        Args:
            audio_bytes: Audio content as bytes.
            from_format: Source format ('mp3', 'wav', 'ogg').
            to_format: Target format.
        
        Returns:
            Converted audio as bytes.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=from_format)
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format=to_format)
        return output_buffer.getvalue()
    
    @staticmethod
    def get_audio_duration(audio_bytes: bytes, format: str = "mp3") -> float:
        """
        Get the duration of audio in seconds.
        
        Args:
            audio_bytes: Audio content as bytes.
            format: Audio format.
        
        Returns:
            Duration in seconds.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        return len(audio) / 1000.0
    
    @staticmethod
    def get_audio_info(audio_bytes: bytes, format: str = "mp3") -> dict:
        """
        Get information about an audio file.
        
        Args:
            audio_bytes: Audio content as bytes.
            format: Audio format.
        
        Returns:
            Dictionary with audio information.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        return {
            "duration_seconds": len(audio) / 1000.0,
            "channels": audio.channels,
            "sample_width": audio.sample_width,
            "frame_rate": audio.frame_rate,
            "dBFS": audio.dBFS,
        }
    
    @staticmethod
    def add_silence(
        audio_bytes: bytes,
        silence_before_ms: int = 0,
        silence_after_ms: int = 0,
        format: str = "mp3"
    ) -> bytes:
        """
        Add silence before and/or after audio.
        
        Args:
            audio_bytes: Audio content as bytes.
            silence_before_ms: Milliseconds of silence to add before.
            silence_after_ms: Milliseconds of silence to add after.
            format: Audio format.
        
        Returns:
            Audio with added silence.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        
        if silence_before_ms > 0:
            silence_before = AudioSegment.silent(duration=silence_before_ms)
            audio = silence_before + audio
        
        if silence_after_ms > 0:
            silence_after = AudioSegment.silent(duration=silence_after_ms)
            audio = audio + silence_after
        
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format=format)
        return output_buffer.getvalue()
    
    @staticmethod
    def fade_in_out(
        audio_bytes: bytes,
        fade_in_ms: int = 0,
        fade_out_ms: int = 0,
        format: str = "mp3"
    ) -> bytes:
        """
        Apply fade in and/or fade out effects.
        
        Args:
            audio_bytes: Audio content as bytes.
            fade_in_ms: Duration of fade in effect in milliseconds.
            fade_out_ms: Duration of fade out effect in milliseconds.
            format: Audio format.
        
        Returns:
            Audio with fade effects applied.
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        
        if fade_in_ms > 0:
            audio = audio.fade_in(fade_in_ms)
        
        if fade_out_ms > 0:
            audio = audio.fade_out(fade_out_ms)
        
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format=format)
        return output_buffer.getvalue()
