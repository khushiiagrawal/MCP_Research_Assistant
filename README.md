# MCP Research Server

A Model Context Protocol (MCP) server that provides tools for searching and managing research papers from arXiv.

## Features

- **Search Papers**: Search for research papers on arXiv by topic
- **Extract Paper Info**: Retrieve detailed information about specific papers
- **Local Storage**: Automatically saves paper information to local JSON files organized by topic
- **Multiple LLM Support**: Works with both Claude (Anthropic) and Gemini (Google) APIs

## Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`
- API key for your chosen LLM provider

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd mcp_project
   ```

2. **Create a virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   uv pip install arxiv
   ```

## LLM Configuration

### Option 1: Using Claude (Anthropic) - Original Setup

1. **Get your Anthropic API key:**
   - Visit: https://console.anthropic.com/
   - Create an account and get your API key

2. **Set up environment variables:**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```
   
   Or create a `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Install Claude dependencies:**
   ```bash
   uv add anthropic
   ```

### Option 2: Using Gemini (Google) - New Setup

1. **Get your Google API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Create an account and get your API key

2. **Set up environment variables:**
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```
   
   Or create a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Install Gemini dependencies:**
   ```bash
   uv add google-generativeai python-dotenv
   ```

## Running the Server

### Method 1: Using MCP Inspector (Recommended for Testing)

1. **Start the server with MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector uv run research_server.py
   ```

2. **Access the Inspector:**
   - Open your browser and go to: `http://127.0.0.1:6274`
   - Use the provided session token for authentication

### Method 2: Direct Execution

1. **Run the server directly:**
   ```bash
   uv run research_server.py
   ```

### Method 3: Using the Chatbot

1. **Run the chatbot with your chosen LLM:**
   ```bash
   # For Claude (original)
   uv run mcp_chatbot.py
   
   # For Gemini (new)
   uv run mcp_chatbot.py
   ```

## Available Tools

### 1. `search_papers`
Searches for papers on arXiv based on a topic and stores their information locally.

**Parameters:**
- `topic` (str): The topic to search for
- `max_results` (int, optional): Maximum number of results (default: 5)

**Returns:** List of paper IDs found

**Example:**
```json
{
  "topic": "machine learning",
  "max_results": 10
}
```

### 2. `extract_info`
Retrieves detailed information about a specific paper from local storage.

**Parameters:**
- `paper_id` (str): The ID of the paper to look for

**Returns:** JSON string with paper information

**Example:**
```json
{
  "paper_id": "2301.12345"
}
```

## Project Structure

```
mcp_project/
├── research_server.py    # Main MCP server implementation
├── mcp_chatbot.py       # Chatbot with LLM integration
├── pyproject.toml        # Project configuration
├── uv.lock              # Dependency lock file
├── papers/              # Directory where paper data is stored
│   └── [topic_name]/    # Organized by topic
│       └── papers_info.json
└── README.md           # This file
```

## How It Works

1. **Paper Search**: When you search for papers, the server:
   - Queries arXiv using the provided topic
   - Downloads paper metadata (title, authors, summary, PDF URL, publication date)
   - Saves the information to a JSON file organized by topic
   - Returns the paper IDs for reference

2. **Paper Retrieval**: When you extract paper info, the server:
   - Searches through all topic directories
   - Finds the requested paper by ID
   - Returns the stored information in JSON format

3. **LLM Integration**: The chatbot:
   - Connects to your chosen LLM (Claude or Gemini)
   - Provides tools to the LLM for paper search and retrieval
   - Handles function calling and tool execution automatically

## Data Storage

Paper information is automatically saved to the `papers/` directory, organized by topic. Each topic gets its own subdirectory containing a `papers_info.json` file with all the papers found for that topic.

## Troubleshooting

- **Python Version**: Ensure you're using Python 3.13 or higher
- **Dependencies**: Make sure all dependencies are installed with `uv pip install arxiv`
- **Virtual Environment**: Always activate the virtual environment before running the server
- **Permissions**: Ensure you have write permissions in the project directory for creating the `papers/` folder
- **API Keys**: Make sure your API key is properly set in environment variables
- **LLM Selection**: The chatbot automatically detects which API key is available and uses the corresponding LLM

## Development

To modify or extend the server:

1. Edit `research_server.py` to add new tools or modify existing ones
2. Edit `mcp_chatbot.py` to customize LLM behavior
3. Use the MCP Inspector to test your changes
4. The server uses FastMCP for easy tool definition and management

## License

This project is open source. Feel free to modify and distribute as needed.
