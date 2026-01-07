const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let messages = [];

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if(this.value === '') this.style.height = 'auto';
});

// Handle Enter key
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // UI Updates
    appendMessage('user', text);
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Disable inputs
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Add to history
    messages.push({role: "user", content: text});

    // Show loading
    const loadingId = appendLoading();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ messages: messages })
        });

        const data = await response.json();
        removeLoading(loadingId);

        if (data.response) {
            appendMessage('assistant', data.response);
            messages.push({role: "assistant", content: data.response});
        } else if (data.error) {
            appendMessage('error', 'Error: ' + data.error);
        } else {
             appendMessage('error', 'Error: Unknown response from server');
        }

    } catch (error) {
        removeLoading(loadingId);
        appendMessage('error', 'Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable inputs
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.classList.add('message');
    div.classList.add(role === 'user' ? 'user-message' : 'ai-message');
    
    if (role === 'assistant' || role === 'error') {
        div.innerHTML = marked.parse(text);
        // Highlight code blocks
        div.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    } else {
        div.textContent = text;
    }

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoading() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.classList.add('message', 'ai-message');
    div.innerHTML = '<em>Thinking...</em>';
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return id;
}

function removeLoading(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
