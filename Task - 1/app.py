"""
Text-to-Speech Web Application using Streamlit.

A beautiful web interface for converting text to speech using
Google Cloud Text-to-Speech API with voice customization options.
"""

import os
import io
import streamlit as st
from datetime import datetime

from tts_app.core.tts_engine import TextToSpeechEngine
from tts_app.core.voice_config import VoiceConfig, VoicePreset
from tts_app.validation.text_validator import TextValidator
from tts_app.utils.constants import (
    LANGUAGES, VOICE_CONFIGS, SAMPLE_TEXTS,
    SPEECH_RATE_MIN, SPEECH_RATE_MAX, SPEECH_RATE_DEFAULT,
    PITCH_MIN, PITCH_MAX, PITCH_DEFAULT,
    VOLUME_MIN, VOLUME_MAX, VOLUME_DEFAULT,
    MAX_CHARACTERS
)

st.set_page_config(
    page_title="Text to Speech",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #6b7280;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .settings-card {
        background: linear-gradient(145deg, #1e1e2e, #2d2d44);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-title {
        color: #a78bfa;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stTextArea textarea {
        background: #1e1e2e;
        border: 2px solid #374151;
        border-radius: 12px;
        color: #e5e7eb;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    .stSelectbox > div > div {
        background: #1e1e2e;
        border: 2px solid #374151;
        border-radius: 12px;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #1e1e2e;
        border-color: #374151;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    [data-baseweb="popover"] {
        background-color: #1e1e2e !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1e1e2e !important;
    }
    
    [data-baseweb="menu"] li {
        color: #e5e7eb !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #374151 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        color: #ffffff !important;
        background-color: #1e1e2e !important;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .audio-container {
        background: linear-gradient(145deg, #1e1e2e, #2d2d44);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .stats-box {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        display: inline-block;
        margin: 0.25rem;
        color: #a78bfa;
        font-size: 0.85rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .css-1d391kg {
        background: #1e1e2e;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    .voice-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None
    if 'audio_generated' not in st.session_state:
        st.session_state.audio_generated = False
    if 'generation_time' not in st.session_state:
        st.session_state.generation_time = None


def get_tts_engine():
    """Get or create TTS engine instance."""
    credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    
    if not os.path.exists(credentials_path):
        st.error("❌ Credentials file not found! Please ensure 'credentials.json' is in the project directory.")
        st.stop()
    
    return TextToSpeechEngine(credentials_path)


def main():
    """Main application function."""
    init_session_state()
    
    st.markdown('<h1 class="main-header">🎤 Text to Speech</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your text into natural-sounding speech with AI-powered voices</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Enter Your Text")
        
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        with sample_col1:
            if st.button("📌 Sample English", use_container_width=True):
                st.session_state.sample_text = SAMPLE_TEXTS.get("en-US", SAMPLE_TEXTS["default"])
        with sample_col2:
            if st.button("📌 Sample Hindi", use_container_width=True):
                st.session_state.sample_text = SAMPLE_TEXTS.get("hi-IN", SAMPLE_TEXTS["default"])
        with sample_col3:
            if st.button("📌 Sample Spanish", use_container_width=True):
                st.session_state.sample_text = SAMPLE_TEXTS.get("es-ES", SAMPLE_TEXTS["default"])
        
        default_text = st.session_state.get('sample_text', '')
        text_input = st.text_area(
            "Enter text to convert to speech",
            value=default_text,
            height=200,
            max_chars=MAX_CHARACTERS,
            placeholder="Type or paste your text here...",
            label_visibility="collapsed"
        )
        
        if text_input:
            stats = TextValidator.get_text_stats(text_input)
            estimated_duration = TextValidator.estimate_speech_duration(text_input)
            
            stats_cols = st.columns(4)
            with stats_cols[0]:
                st.metric("Characters", f"{stats['characters']:,}")
            with stats_cols[1]:
                st.metric("Words", f"{stats['words']:,}")
            with stats_cols[2]:
                st.metric("Sentences", stats['sentences'])
            with stats_cols[3]:
                st.metric("Est. Duration", f"{estimated_duration:.1f}s")
    
    with col2:
        st.markdown("### 🎙️ Voice Settings")
        
        language_options = list(LANGUAGES.keys())
        language_display = [f"{LANGUAGES[code]}" for code in language_options]
        
        selected_lang_idx = st.selectbox(
            "Language",
            range(len(language_options)),
            format_func=lambda x: language_display[x],
            index=0
        )
        selected_language = language_options[selected_lang_idx]
        
        available_genders = VoiceConfig.get_available_genders(selected_language)
        gender_display = {"MALE": "👨 Male", "FEMALE": "👩 Female", "NEUTRAL": "🔘 Neutral"}
        
        selected_gender = st.selectbox(
            "Voice Gender",
            available_genders,
            format_func=lambda x: gender_display.get(x, x)
        )
        
        voices = VoiceConfig.get_voices_by_gender(selected_language, selected_gender)
        if voices:
            voice_display = [VoiceConfig.format_voice_display(v) for v in voices]
            selected_voice_idx = st.selectbox(
                "Voice",
                range(len(voices)),
                format_func=lambda x: voice_display[x]
            )
            selected_voice = voices[selected_voice_idx]
        else:
            selected_voice = None
            st.info("No specific voices available for this selection.")
        
        st.markdown("---")
        
        st.markdown("### ⚡ Speech Controls")
        
        speaking_rate = st.slider(
            "Speaking Rate",
            min_value=SPEECH_RATE_MIN,
            max_value=SPEECH_RATE_MAX,
            value=SPEECH_RATE_DEFAULT,
            step=0.05,
            help="Adjust the speed of speech (0.25 = slow, 4.0 = fast)"
        )
        
        rate_labels = {0.25: "Very Slow", 0.5: "Slow", 1.0: "Normal", 1.5: "Fast", 2.0: "Very Fast", 4.0: "Maximum"}
        rate_label = min(rate_labels.keys(), key=lambda x: abs(x - speaking_rate))
        st.caption(f"Speed: {rate_labels[rate_label]}")
        
        pitch = st.slider(
            "Pitch",
            min_value=PITCH_MIN,
            max_value=PITCH_MAX,
            value=PITCH_DEFAULT,
            step=1.0,
            help="Adjust voice pitch (-20 = lower, +20 = higher)"
        )
        
        volume_gain = st.slider(
            "Volume Gain (dB)",
            min_value=-10.0,
            max_value=VOLUME_MAX,
            value=VOLUME_DEFAULT,
            step=1.0,
            help="Adjust output volume"
        )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    with generate_col2:
        generate_button = st.button("🎵 Generate Speech", use_container_width=True, type="primary")
    
    if generate_button:
        if not text_input or not text_input.strip():
            st.error("❌ Please enter some text to convert to speech.")
        else:
            validation_result = TextValidator.validate(text_input)
            
            if not validation_result.is_valid:
                st.error(f"❌ {validation_result.error_message}")
            else:
                for warning in validation_result.warnings:
                    st.warning(f"⚠️ {warning}")
                
                with st.spinner("🎙️ Generating speech... Please wait."):
                    try:
                        engine = get_tts_engine()
                        
                        start_time = datetime.now()
                        
                        audio_content = engine.synthesize_speech(
                            text=validation_result.sanitized_text,
                            language_code=selected_language,
                            voice_name=selected_voice,
                            voice_gender=selected_gender,
                            speaking_rate=speaking_rate,
                            pitch=pitch,
                            volume_gain_db=volume_gain,
                            audio_encoding="MP3"
                        )
                        
                        end_time = datetime.now()
                        generation_time = (end_time - start_time).total_seconds()
                        
                        st.session_state.audio_data = audio_content
                        st.session_state.audio_generated = True
                        st.session_state.generation_time = generation_time
                        
                        st.success(f"✅ Speech generated successfully in {generation_time:.2f} seconds!")
                        
                    except Exception as e:
                        error_message = str(e)
                        if "401" in error_message or "invalid authentication credentials" in error_message.lower():
                            st.error("🔑 **Authentication Error (401)**")
                            st.error("The Application failed to authenticate with Google Cloud.")
                            st.info("""
                            **How to fix:**
                            1. Ensure you have a valid `credentials.json` file in the project directory.
                            2. Check if the Google Cloud Project has the **Text-to-Speech API** enabled.
                            3. Verify your Service Account has the correct permissions.
                            """)
                        else:
                            st.error(f"❌ Error generating speech: {error_message}")
                        
                        st.session_state.audio_generated = False
    
    if st.session_state.audio_generated and st.session_state.audio_data:
        st.markdown("---")
        st.markdown("### 🎧 Generated Audio")
        
        audio_col1, audio_col2, audio_col3 = st.columns([1, 2, 1])
        
        with audio_col2:
            st.audio(st.session_state.audio_data, format="audio/mp3")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_output_{timestamp}.mp3"
            
            st.download_button(
                label="📥 Download Audio",
                data=st.session_state.audio_data,
                file_name=filename,
                mime="audio/mp3",
                use_container_width=True
            )
            
            try:
                from tts_app.core.audio_processor import AudioProcessor
                audio_info = AudioProcessor.get_audio_info(st.session_state.audio_data)
                st.caption(f"Duration: {audio_info['duration_seconds']:.2f}s | Channels: {audio_info['channels']} | Sample Rate: {audio_info['frame_rate']}Hz")
            except:
                pass
    
    with st.sidebar:
        st.markdown("## ℹ️ About")
        st.markdown("""
        This application uses **Google Cloud Text-to-Speech** API to convert text into natural-sounding speech.
        
        **Features:**
        - 🌍 Select many languages
        - 👨👩 Male & Female Voices
        - 🎚️ Adjustable Speech Rate
        - 🔊 Pitch & Volume Control
        - 📥 Download as MP3
        """)
        
        st.markdown("---")
        
        st.markdown("## 🎭 Voice Presets")
        presets = VoicePreset.list_presets()
        
        for preset_name, description in presets:
            with st.expander(description):
                preset = VoicePreset.get_preset(preset_name)
                st.write(f"**Language:** {preset['language_code']}")
                st.write(f"**Voice:** {preset['voice_name']}")
                st.write(f"**Rate:** {preset['speaking_rate']}")
                st.write(f"**Pitch:** {preset['pitch']}")


if __name__ == "__main__":
    main()
