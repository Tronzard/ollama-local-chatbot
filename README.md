# Local LLM Chatbot — Python + Ollama

A lightweight command-line AI chatbot built with **Python**, **Ollama**, and the **OpenAI Python SDK**. It runs a local language model, maintains conversational context, validates messages with Pydantic, and saves chat history to JSON—without requiring a paid LLM API.

This is my first hands-on Generative AI project, built to learn LLM API integration, environment configuration, HTTP/JSON, data validation, and error handling.

## Features

- **Local LLM inference** using Ollama and `qwen2.5:1.5b`
- **Interactive terminal chat** with a configurable system prompt
- **Conversation context** using the 10 most recent saved messages
- **Persistent chat history** saved to `chat_history.json` and loaded on restart
- **Commands:** `/save`, `/clear`, and `/exit`
- **Pydantic validation** for conversation messages
- **Environment-based configuration** with `.env`
- **Basic error handling** for API and file-operation failures

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Application logic |
| Ollama | Local model serving |
| Qwen2.5 1.5B | Language model |
| OpenAI Python SDK | OpenAI-compatible API client |
| python-dotenv | Load configuration from `.env` |
| Pydantic | Validate and serialize chat messages |
| HTTPX | Demonstrate raw HTTP + JSON requests |

## Project Structure

```text
day01-chatbot/
├── chat.py             # Main interactive chatbot
├── hello.py            # First LLM API call
├── http_demo.py        # Raw HTTP/JSON example
├── pydantic_demo.py    # Pydantic validation example
├── test_env.py         # Environment variable check
├── requirements.txt    # Python dependencies
├── .env.example        # Example local configuration
├── .gitignore
└── README.md
```

`chat_history.json` is created automatically when a conversation is saved. `.venv/`, `.env`, and `chat_history.json` should not be committed to Git.

## Getting Started

### 1. Prerequisites

- Python 3.11 or 3.12
- [Ollama](https://ollama.com/download) installed and running
- Git (optional)

Download the model:

```bash
ollama pull qwen2.5:1.5b
```

Check that it is installed:

```bash
ollama list
```

### 2. Create a virtual environment

Open a terminal in the project folder. On **Windows PowerShell**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On **macOS/Linux**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If you haven't created a `requirements.txt` yet, install the packages directly:

```bash
python -m pip install openai python-dotenv pydantic httpx
```

### 4. Configure the app

Create a `.env` file **in the project root**, next to `chat.py`:

```dotenv
LLM_BASE_URL=http://localhost:11434/v1/
LLM_MODEL=qwen2.5:1.5b
LLM_API_KEY=ollama
```

`LLM_API_KEY=ollama` is a placeholder for the local server, **not a real secret key**. You can also copy `.env.example` to `.env` if that file is included in your repository.

### 5. Run the chatbot

Make sure Ollama is running, then execute:

```bash
python chat.py
```

Example session:

```text
Welcome to your local AI chatbot!
Commands: /save, /clear, /exit

You: What is gradient descent?
AI: Gradient descent is an optimization method ...

You: Can you explain it with an example?
AI: Sure! Imagine you're trying to ...

You: /save
Conversation saved!
```

Model answers vary from run to run.

## Chat Commands

| Command | Action |
| --- | --- |
| `/save` | Save the current conversation to JSON |
| `/clear` | Clear active conversation and saved history |
| `/exit` | Save the conversation and exit |

## Other Learning Scripts

Run these separately to explore individual concepts:

```bash
python test_env.py       # Read configuration from .env
python hello.py          # Make one LLM API call
python http_demo.py      # Send a direct HTTP request to Ollama
python pydantic_demo.py  # Validate message data with Pydantic
```

## How It Works

```text
Terminal input
    ↓
Python CLI (chat.py)
    ↓
Recent conversation + system prompt
    ↓
OpenAI-compatible HTTP request
    ↓
Ollama → Local Qwen model
    ↓
Response displayed in terminal
    ↓
Messages saved to JSON
```

**Conversation history is managed by Python**, not stored in the model's weights. The script sends only the 10 most recent chat messages with each request, so older information may fall out of context.

## Limitations & Next Steps

This is a learning project, not a production chatbot. It does not yet provide streaming responses, document retrieval (RAG), authentication, or a graphical interface.

Planned learning exercises:

- Experiment with system prompts and generation settings
- Add token-by-token streaming responses
- Explore structured JSON outputs
- Add embeddings and semantic search
- Build a simple retrieval-augmented generation pipeline

## What I Learned

- How to call a local LLM through an OpenAI-compatible API
- How HTTP requests and JSON responses work
- How to keep configuration separate from source code
- How to validate and serialize data with Pydantic
- How to preserve conversational context and handle common errors

---

*Part of my hands-on journey into Generative AI engineering.*
