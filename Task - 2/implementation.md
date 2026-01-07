# Mistral API Integration Plan

## Goal Description
Create a Python application that integrates with the Mistral API. The project will include a basic API connection script, a CLI for interactive chatting with history support, error handling/logging, and a simple Flask-based web interface.

## User Review Required
> [!IMPORTANT]
> The API Key will be stored in a `.env` file. Please ensure this file is not shared if the code is pushed to a public repository.

## Proposed Changes

### Configuration
#### [.env]
- Store `MISTRAL_API_KEY`.
- Download the `.env` file containing the API key (sent via email -  nandukumar9980@gmail.com  ).

####  [requirements.txt]
- `requests`
- `python-dotenv`
- `flask`

### Core Logic
#### [api_client.py]
- `MistralClient` class.
- Method `send_prompt(messages)`: Sends request to Mistral API endpoint `https://api.mistral.ai/v1/chat/completions`.
- Error handling for timeouts and status codes.
- Logging to `app.log`.

### CLI Interface
#### [cli_app.py]
- Interactive loop.
- Maintains chat history context.
- Formats output (bullet points, etc. handled by markdown approximation or direct print).

### Web Interface
#### [web_app.py]
- Flask server.
- Route `/`: Serves `index.html`.
- Route `/api/chat`: Proxy to `api_client.py`.

#### [templates/index.html]
- Chat interface structure.

#### [static/style.css]
- Styling for the chat UI.

#### [static/script.js]
- Frontend logic to send messages to Flask and render responses.

## Verification Plan

### Automated Tests
- Run `cli_app.py` and interact manually.
- Run `examples/basic_connect.py` (optional) to test connection.

### Manual Verification
- Start Flask app `python web_app.py`.
- Open browser at `http://127.0.0.1:5000`.
- Send a message and check response.
