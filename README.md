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

## Installation

### Requirements
- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### 1. Clone repository
```bash
git clone https://github.com/RushdiJa/dimdom_agent.git
cd dimdom_agent
```

### 2. Install uv (if not installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies
```bash
uv sync
```

### 4. Create `.env` file
```env
GEMINI_API_KEY1=YOUR_API_KEY_HERE
TOTAL_API_KEYS=1
```
> For multiple keys: add `GEMINI_API_KEY2`, `GEMINI_API_KEY3`... and update `TOTAL_API_KEYS`

### 5. Run
```bash
uv run main.py "your prompt here"

# verbose mode
uv run main.py "your prompt here" --verbose
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
