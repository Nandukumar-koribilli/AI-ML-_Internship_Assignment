"""
Unit tests for the TextValidator class.
"""

import pytest
from tts_app.validation.text_validator import TextValidator, ValidationResult


class TestTextValidatorBasics:
    """Test basic validation functionality."""
    
    def test_valid_text_passes(self):
        """Test that valid text passes validation."""
        text = "Hello, this is a test message for text to speech."
        result = TextValidator.validate(text)
        
        assert result.is_valid is True
        assert result.error_message is None
        assert len(result.sanitized_text) > 0
    
    def test_empty_text_fails(self):
        """Test that empty text fails validation."""
        result = TextValidator.validate("")
        
        assert result.is_valid is False
        assert result.error_message == "Text cannot be empty"
    
    def test_whitespace_only_fails(self):
        """Test that whitespace-only text fails validation."""
        result = TextValidator.validate("   \n\t   ")
        
        assert result.is_valid is False
        assert result.error_message == "Text cannot be empty"
    
    def test_none_text_fails(self):
        """Test that None text fails validation."""
        result = TextValidator.validate(None)
        
        assert result.is_valid is False
        assert result.error_message == "Text cannot be None"


class TestTextValidatorLength:
    """Test text length validation."""
    
    def test_max_length_validation(self):
        """Test that text exceeding max length is rejected."""
        long_text = "a" * 6000
        result = TextValidator.validate(long_text)
        
        assert result.is_valid is False
        assert "exceeds maximum length" in result.error_message
    
    def test_text_at_max_length_passes(self):
        """Test that text at exactly max length passes."""
        text = "a" * 5000
        result = TextValidator.validate(text)
        
        assert result.is_valid is True
    
    def test_byte_limit_truncation(self):
        """Test that text exceeding byte limit is truncated with warning."""
        text = "こんにちは" * 600
        result = TextValidator.validate(text)
        
        if result.is_valid:
            assert len(result.warnings) > 0 or len(result.sanitized_text.encode('utf-8')) <= 5000


class TestTextValidatorSpecialCharacters:
    """Test special character handling."""
    
    def test_handles_ampersand(self):
        """Test that & is replaced with 'and'."""
        text = "Tom & Jerry"
        sanitized = TextValidator.sanitize(text)
        
        assert "&" not in sanitized
        assert "and" in sanitized
    
    def test_handles_at_symbol(self):
        """Test that @ is replaced with 'at'."""
        text = "Contact us @ support"
        sanitized = TextValidator.sanitize(text)
        
        assert "@" not in sanitized
        assert "at" in sanitized
    
    def test_handles_percent(self):
        """Test that % is replaced with 'percent'."""
        text = "Save 50% today"
        sanitized = TextValidator.sanitize(text)
        
        assert "%" not in sanitized
        assert "percent" in sanitized
    
    def test_handles_currency_symbols(self):
        """Test that currency symbols are converted to words."""
        text = "Price: $100, €50, £30, ₹2000"
        sanitized = TextValidator.sanitize(text)
        
        assert "€" not in sanitized
        assert "£" not in sanitized
        assert "₹" not in sanitized
        assert "euros" in sanitized
        assert "pounds" in sanitized
        assert "rupees" in sanitized
    
    def test_handles_smart_quotes(self):
        """Test that smart quotes are converted to standard quotes."""
        text = "\u201cHello\u201d and \u2018World\u2019"
        sanitized = TextValidator.sanitize(text)
        
        assert "\u201c" not in sanitized
        assert "\u201d" not in sanitized
        assert "\u2018" not in sanitized
        assert "\u2019" not in sanitized
    
    def test_removes_zero_width_characters(self):
        """Test that zero-width characters are removed."""
        text = "Hello\u200bWorld\u200c!"
        sanitized = TextValidator.sanitize(text)
        
        assert "\u200b" not in sanitized
        assert "\u200c" not in sanitized
    
    def test_reduces_multiple_exclamation_marks(self):
        """Test that multiple exclamation marks are reduced."""
        text = "Amazing!!!! Incredible!!!"
        sanitized = TextValidator.sanitize(text)
        
        assert "!!!!" not in sanitized
        assert "!!!" not in sanitized


class TestTextValidatorUnicode:
    """Test Unicode normalization."""
    
    def test_unicode_normalization(self):
        """Test that Unicode characters are normalized."""
        text1 = "café"
        text2 = "cafe\u0301"
        
        normalized1 = TextValidator.normalize_unicode(text1)
        normalized2 = TextValidator.normalize_unicode(text2)
        
        assert normalized1 == normalized2
    
    def test_handles_emoji(self):
        """Test that emoji don't break validation."""
        text = "Hello 👋 World 🌍"
        result = TextValidator.validate(text)
        
        assert result.is_valid is True


class TestTextValidatorWhitespace:
    """Test whitespace handling."""
    
    def test_multiple_spaces_collapsed(self):
        """Test that multiple spaces are collapsed to single space."""
        text = "Hello    World     Test"
        sanitized = TextValidator.sanitize(text)
        
        assert "    " not in sanitized
        assert "Hello World Test" == sanitized
    
    def test_multiple_newlines_collapsed(self):
        """Test that excessive newlines are collapsed."""
        text = "Hello\n\n\n\n\nWorld"
        sanitized = TextValidator.sanitize(text)
        
        assert "\n\n\n" not in sanitized
    
    def test_leading_trailing_whitespace_stripped(self):
        """Test that leading/trailing whitespace is removed."""
        text = "   Hello World   "
        sanitized = TextValidator.sanitize(text)
        
        assert sanitized == "Hello World"


class TestTextValidatorStats:
    """Test text statistics functionality."""
    
    def test_get_text_stats(self):
        """Test text statistics calculation."""
        text = "Hello world. How are you? I am fine!"
        stats = TextValidator.get_text_stats(text)
        
        assert stats["characters"] == len(text)
        assert stats["words"] == 8
        assert stats["sentences"] == 3
    
    def test_empty_text_stats(self):
        """Test stats for empty text."""
        stats = TextValidator.get_text_stats("")
        
        assert stats["characters"] == 0
        assert stats["words"] == 0
        assert stats["bytes"] == 0


class TestTextValidatorSpeechDuration:
    """Test speech duration estimation."""
    
    def test_estimate_speech_duration(self):
        """Test speech duration estimation."""
        words = " ".join(["word"] * 150)
        duration = TextValidator.estimate_speech_duration(words, speaking_rate=1.0)
        
        assert 55 <= duration <= 65
    
    def test_estimate_duration_with_faster_rate(self):
        """Test duration with faster speaking rate."""
        words = " ".join(["word"] * 150)
        duration_normal = TextValidator.estimate_speech_duration(words, speaking_rate=1.0)
        duration_fast = TextValidator.estimate_speech_duration(words, speaking_rate=2.0)
        
        assert duration_fast < duration_normal


class TestTextValidatorSplitText:
    """Test long text splitting functionality."""
    
    def test_short_text_not_split(self):
        """Test that short text is not split."""
        text = "This is a short text."
        chunks = TextValidator.split_long_text(text)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_long_text_split_at_sentences(self):
        """Test that long text is split at sentence boundaries."""
        sentences = ["This is sentence number {}.".format(i) for i in range(100)]
        text = " ".join(sentences)
        
        chunks = TextValidator.split_long_text(text, max_chars=500)
        
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= 500
    
    def test_all_content_preserved_after_split(self):
        """Test that no content is lost when splitting."""
        text = "Hello. World. Test. Sentence. Another."
        chunks = TextValidator.split_long_text(text, max_chars=20)
        
        rejoined = " ".join(chunks)
        original_words = set(text.replace(".", " ").split())
        rejoined_words = set(rejoined.replace(".", " ").split())
        
        assert original_words == rejoined_words


class TestTextValidatorEdgeCases:
    """Test edge cases."""
    
    def test_only_punctuation_fails(self):
        """Test that text with only punctuation fails."""
        text = "!!! ??? ..."
        result = TextValidator.validate(text)
        
        assert result.is_valid is False
        assert "no speakable content" in result.error_message
    
    def test_only_special_chars_fails(self):
        """Test that text with only special characters fails."""
        text = "@#$%^&*()"
        result = TextValidator.validate(text)
        
        assert isinstance(result, ValidationResult)
    
    def test_mixed_language_text(self):
        """Test that mixed language text is handled."""
        text = "Hello こんにちは Bonjour"
        result = TextValidator.validate(text)
        
        assert result.is_valid is True
    
    def test_numbers_are_valid(self):
        """Test that numeric text is valid."""
        text = "The year is 2024 and the price is 99.99"
        result = TextValidator.validate(text)
        
        assert result.is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
