# MCP Research Assistant 🧠

A comprehensive Model Context Protocol (MCP) setup that provides powerful tools for research, file management, and web content fetching. This project integrates multiple MCP servers to enhance your AI assistant capabilities.

## ✨ Features

- **📚 Research Tool**: Search and manage academic papers from arXiv
- **📁 Filesystem Tool**: Browse, read, and manage project files
- **🌐 Fetch Tool**: Retrieve content from websites and APIs
- **🤖 Multi-LLM Support**: Works with Claude, Gemini, and other AI models
- **💾 Local Storage**: Automatically saves research data organized by topics

## 🛠️ Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`
- API keys for your chosen LLM providers
- Claude Desktop (for MCP integration)

## 💻 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd mcp_project
```

### 2. Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in your project root:

```env
# Choose one or both depending on your needs
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Configure Claude Desktop

Create or update your Claude Desktop configuration file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ],
      "cwd": "/path/to/your/mcp_project"
    },
    "research": {
      "command": "/path/to/your/mcp_project/.venv/bin/python",
      "args": [
        "/path/to/your/mcp_project/research_server.py"
      ],
      "cwd": "/path/to/your/mcp_project"
    },
    "fetch": {
      "command": "/path/to/your/.local/bin/uvx",
      "args": ["mcp-server-fetch"],
      "cwd": "/path/to/your/mcp_project"
    }
  }
}
```

**Important**: Replace `/path/to/your/mcp_project` with your actual project path.

### 5. Restart Claude Desktop

Restart Claude Desktop completely to load the new configuration.

## 🎯 How to Use

### Research Tool 🔬

**Search for Papers:**
```
Search for 5 papers about machine learning
```

**Get Paper Details:**
```
Show me information about paper ID 1234.5678
```

**Browse Saved Papers:**
```
What papers do I have saved on physics?
```

### Filesystem Tool 📁

**Browse Files:**
```
List all files in my project directory
```

**Read Files:**
```
Show me the contents of research_server.py
```

**Create Files:**
```
Create a new Python script for data analysis
```

### Fetch Tool 🌐

**Get Web Content:**
```
Fetch the latest Python documentation
```

**API Calls:**
```
Get current weather data from an API
```

## 📋 Available Tools

### Research Server Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_papers` | Search arXiv for papers | `topic`, `max_results` |
| `extract_info` | Get paper details | `paper_id` |
| `get_available_folders` | List saved topics | None |

### Filesystem Server Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write to files |
| `list_dir` | List directory contents |
| `delete_file` | Delete files |

### Fetch Server Tools

| Tool | Description |
|------|-------------|
| `fetch` | Fetch content from URLs |

## 📁 Project Structure

```
mcp_project/
├── research_server.py          # Main research MCP server
├── mcp_chatbot_L7.py          # Chatbot with LLM integration
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── uv.lock                   # Dependency lock file
├── papers/                   # Research data storage
│   └── [topic_name]/         # Organized by topic
│       └── papers_info.json  # Paper metadata
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🔧 Configuration Details

### Research Server Configuration

The research server automatically:
- Creates topic-based directories in `papers/`
- Saves paper metadata as JSON files
- Provides search and retrieval functions
- Integrates with arXiv API

### Filesystem Server Configuration

The filesystem server:
- Operates within your project directory
- Provides full file management capabilities
- Uses relative paths for portability

### Fetch Server Configuration

The fetch server:
- Handles web requests and API calls
- Supports custom user agents
- Can ignore robots.txt restrictions


## 🔄 Updating Dependencies

```bash
# Add new dependencies
uv add package_name

# Update requirements.txt
uv pip freeze > requirements.txt

# Sync all dependencies
uv sync
```

## 📝 Development

### Adding New Tools

1. Edit `research_server.py` to add new functions
2. Use the `@mcp.tool()` decorator
3. Test with MCP Inspector
4. Update documentation

### Customizing LLM Behavior

1. Edit `mcp_chatbot_L7.py`
2. Modify tool descriptions and parameters
3. Add custom prompts and resources

