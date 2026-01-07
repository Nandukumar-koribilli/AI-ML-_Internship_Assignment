"""
Text validation module for the TTS application.
Handles special characters, length validation, and text sanitization.
"""

import re
import unicodedata
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of text validation."""
    is_valid: bool
    sanitized_text: str
    error_message: Optional[str] = None
    warnings: list = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class TextValidator:
    """
    Validates and sanitizes text for TTS conversion.
    """
    
    MAX_BYTES = 5000
    MAX_CHARACTERS = 5000
    
    PROBLEMATIC_CHARS = {
        '\x00': '',
        '\x0b': ' ',
        '\x0c': ' ',
        '\r': '\n',
    }
    
    MULTIPLE_SPACES_PATTERN = re.compile(r' {2,}')
    MULTIPLE_NEWLINES_PATTERN = re.compile(r'\n{3,}')
    
    @classmethod
    def validate(cls, text: str) -> ValidationResult:
        """
        Validate text for TTS conversion.
        
        Args:
            text: Text to validate.
        
        Returns:
            ValidationResult with validation status and sanitized text.
        """
        warnings = []
        
        if text is None:
            return ValidationResult(
                is_valid=False,
                sanitized_text="",
                error_message="Text cannot be None"
            )
        
        text = text.strip()
        
        if not text:
            return ValidationResult(
                is_valid=False,
                sanitized_text="",
                error_message="Text cannot be empty"
            )
        
        if len(text) > cls.MAX_CHARACTERS:
            return ValidationResult(
                is_valid=False,
                sanitized_text=text[:cls.MAX_CHARACTERS],
                error_message=f"Text exceeds maximum length of {cls.MAX_CHARACTERS} characters. Current length: {len(text)}"
            )
        
        sanitized_text = cls.sanitize(text)
        
        byte_count = len(sanitized_text.encode('utf-8'))
        if byte_count > cls.MAX_BYTES:
            while len(sanitized_text.encode('utf-8')) > cls.MAX_BYTES:
                sanitized_text = sanitized_text[:-100]
            sanitized_text = sanitized_text.strip()
            warnings.append(f"Text was truncated to fit the {cls.MAX_BYTES} byte limit")
        
        if not cls._has_speakable_content(sanitized_text):
            return ValidationResult(
                is_valid=False,
                sanitized_text=sanitized_text,
                error_message="Text contains no speakable content"
            )
        
        return ValidationResult(
            is_valid=True,
            sanitized_text=sanitized_text,
            warnings=warnings
        )
    
    @classmethod
    def sanitize(cls, text: str) -> str:
        """
        Sanitize text by handling special characters and normalizing.
        
        Args:
            text: Text to sanitize.
        
        Returns:
            Sanitized text.
        """
        if not text:
            return ""
        
        for char, replacement in cls.PROBLEMATIC_CHARS.items():
            text = text.replace(char, replacement)
        
        text = cls.normalize_unicode(text)
        text = cls.handle_special_characters(text)
        text = cls._clean_whitespace(text)
        
        return text.strip()
    
    @classmethod
    def normalize_unicode(cls, text: str) -> str:
        """
        Normalize Unicode characters to their canonical form.
        
        Args:
            text: Text to normalize.
        
        Returns:
            Normalized text.
        """
        return unicodedata.normalize('NFC', text)
    
    @classmethod
    def handle_special_characters(cls, text: str) -> str:
        """
        Handle special characters that might cause TTS issues.
        
        Args:
            text: Text with special characters.
        
        Returns:
            Text with special characters handled.
        """
        replacements = {
            '&': ' and ',
            '@': ' at ',
            '#': ' number ',
            '%': ' percent ',
            '+': ' plus ',
            '=': ' equals ',
            '<': ' less than ',
            '>': ' greater than ',
            '~': ' approximately ',
            '^': ' caret ',
            '|': ' pipe ',
            '\\': ' backslash ',
            '`': '',
            '€': ' euros ',
            '£': ' pounds ',
            '¥': ' yen ',
            '₹': ' rupees ',
            '©': ' copyright ',
            '®': ' registered ',
            '™': ' trademark ',
            '°': ' degrees ',
            '•': ', ',
            '…': '...',
            '—': ' - ',
            '–': ' - ',
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        text = re.sub(r'[\u200b-\u200f\u2028-\u202f\ufeff]', '', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        text = re.sub(r'[.]{4,}', '...', text)
        
        return text
    
    @classmethod
    def _clean_whitespace(cls, text: str) -> str:
        """
        Clean up excessive whitespace.
        
        Args:
            text: Text with potential whitespace issues.
        
        Returns:
            Text with cleaned whitespace.
        """
        text = cls.MULTIPLE_SPACES_PATTERN.sub(' ', text)
        text = cls.MULTIPLE_NEWLINES_PATTERN.sub('\n\n', text)
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        text = '\n'.join(lines)
        
        return text
    
    @classmethod
    def _has_speakable_content(cls, text: str) -> bool:
        """
        Check if text has content that can be spoken.
        
        Args:
            text: Text to check.
        
        Returns:
            True if text has speakable content.
        """
        cleaned = re.sub(r'[\s\W]+', '', text)
        return len(cleaned) > 0
    
    @classmethod
    def get_text_stats(cls, text: str) -> dict:
        """
        Get statistics about the text.
        
        Args:
            text: Text to analyze.
        
        Returns:
            Dictionary with text statistics.
        """
        if not text:
            return {
                "characters": 0,
                "bytes": 0,
                "words": 0,
                "sentences": 0,
                "paragraphs": 0,
            }
        
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        paragraphs = text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        return {
            "characters": len(text),
            "bytes": len(text.encode('utf-8')),
            "words": len(text.split()),
            "sentences": sentence_count,
            "paragraphs": max(1, paragraph_count),
        }
    
    @classmethod
    def estimate_speech_duration(cls, text: str, speaking_rate: float = 1.0) -> float:
        """
        Estimate the duration of speech for given text.
        
        Args:
            text: Text to estimate.
            speaking_rate: Speaking rate multiplier.
        
        Returns:
            Estimated duration in seconds.
        """
        words_per_minute = 150 * speaking_rate
        word_count = len(text.split())
        
        return (word_count / words_per_minute) * 60
    
    @classmethod
    def split_long_text(cls, text: str, max_chars: int = 4500) -> list:
        """
        Split long text into chunks that fit within the API limit.
        
        Args:
            text: Text to split.
            max_chars: Maximum characters per chunk.
        
        Returns:
            List of text chunks.
        """
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                if len(sentence) > max_chars:
                    words = sentence.split()
                    current_chunk = ""
                    for word in words:
                        if len(current_chunk) + len(word) + 1 <= max_chars:
                            current_chunk += (" " if current_chunk else "") + word
                        else:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = word
                else:
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
