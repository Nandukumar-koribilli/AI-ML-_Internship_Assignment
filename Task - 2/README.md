# Mistral AI Integration Project

A comprehensive Python application integrating the Mistral AI API, featuring a robust CLI and a premium web-based chat interface.

## 🌟 Features

### Core Integration

- **Mistral API Connection**: Seamless integration with `mistral-tiny` model.
- **Robust Error Handling**: Auto-recovery and logging for API timeouts and connection issues.
- **Secure Configuration**: Environment-based API key management.

### 💻 Command Line Interface (CLI)

- **Interactive Session**: Chat with context retention.
- **Simple & Fast**: Lightweight interface for quick queries.

### 🎨 Premium Web Interface

- **Glassmorphism Design**: Modern, translucent UI with blur effects.
- **Dynamic Backgrounds**: Animated glowing elements for an immersive experience.
- **Markdown Support**: Full rendering of code blocks, lists, and formatted text.
- **Syntax Highlighting**: Beautiful code highlighting for developer-friendly responses.
- **Responsive Layout**: Works smoothly on different screen sizes.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Mistral API Key (pre-configured in `.env`)

### Installation

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Download the `.env` file containing the API key (sent via email - nandukumar9980@gmail.com ).
   - Place the `.env` file directly in this project folder.
   - _Note: The API key is not included in the repository for security reasons._

## 📖 Usage

### Option 1: Web Interface 

Launch the modern chat UI:

![Web Interface](images/Web%20View.png)

```bash
python web_app.py
```

> The application will print a clickable link: `http://127.0.0.1:5000`

### Option 2: CLI Chat

Run the terminal-based chat:

![CLI Interface](images/CLI%20View.png)

```bash
python cli_app.py
```

## 📂 Project Structure

| File/Directory  | Description                                            |
| --------------- | ------------------------------------------------------ |
| `api_client.py` | Core API wrapper class handling requests and logic.    |
| `web_app.py`    | Flask server backend handling routes and API proxying. |
| `cli_app.py`    | Terminal frontend for the chat application.            |
| `templates/`    | HTML templates including the main chat interface.      |
| `static/`       | CSS (Glassmorphism styles) and JavaScript logic.       |
| `app.log`       | Application logs for debugging.                        |

---
