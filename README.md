# DimDom Agent

An AI-powered coding agent built with Google's Gemini API and function calling.
The agent can explore projects, read and modify files, and execute Python code safely through structured tools.

## Features

* 📂 List files and directories (`get_files_info.py`)
* 📖 Read file contents (`get_file_content.py`)
* ✏️ Create and edit files (`write_file.py`)
* ▶️ Execute Python scripts (`run_python_file.py`)
* 🧠 AI orchestration using Google Gemini function calling
* 🔑 Multi API-key rotation support

## Project Structure

```text
get_files_info.py      → Lists files and folders in a directory
get_file_content.py    → Reads content of a file
write_file.py          → Creates or modifies files
run_python_file.py     → Executes Python scripts safely
```

## Setup

### 1. Clone repository

```bash id="repo1"
git clone https://github.com/RushdiJa/dimdom_agent.git
cd dimdom_agent
```

### 2. Create `.env` file

```env id="env1"
GEMINI_API_KEY1=YOUR_API_KEY_1
GEMINI_API_KEY2=YOUR_API_KEY_2
TOTAL_API_KEYS=2
```

### 3. Install dependencies

```bash id="install1"
uv sync
```

### 4. Run agent

```bash id="run1"
uv run main.py
```

## How it works

The agent uses Google Gemini function calling to decide when to:

* inspect files
* read content
* create or modify code
* execute Python scripts

Each tool is implemented as a separate Python module and dynamically invoked by the AI.

## Tech Stack

* Python
* Google Gemini API (GenAI SDK)
* Function Calling
* UV package manager

## License

MIT
