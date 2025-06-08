# Gemini MCP Server

A Model Context Protocol (MCP) server that enables integration with Google's Gemini models, including Gemini 1.5 Pro and Gemini 2.5 Pro preview.

## Features

- **Chat with Gemini**: Send prompts to any available Gemini model
- **List Models**: View all available Gemini models
- **Configurable Parameters**: Adjust temperature, max tokens, and model selection
- **System Prompts**: Support for system prompts to set context

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set your Gemini API key as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Direct Usage

Run the server:
```bash
source venv/bin/activate
export GEMINI_API_KEY="your-api-key-here"
python gemini_server.py
```

## Available Tools

### chat
Send a prompt to Gemini and receive a response.

Parameters:
- `prompt` (required): The prompt to send to Gemini
- `system_prompt` (optional): System prompt for context
- `max_tokens` (optional): Maximum tokens in response (default: 4096)
- `temperature` (optional): Temperature for randomness 0-1 (default: 0.7)
- `model` (optional): Model to use (default: gemini-1.5-pro-latest)

Available models include:
- `gemini-1.5-pro-latest` - Latest stable Gemini 1.5 Pro
- `gemini-1.5-flash` - Fast Gemini 1.5 Flash model
- `gemini-2.5-pro-preview-06-05` - Gemini 2.5 Pro preview (may have restrictions)
- `gemini-2.0-flash` - Gemini 2.0 Flash
- And many more (use `list_models` to see all available)

### list_models
List all available Gemini models that support content generation.

## Requirements

- Python 3.8+
- Valid Google Gemini API key

## Notes

- The Gemini 2.5 Pro preview models may have safety restrictions that block certain prompts
- If a model returns a blocked response, the server will indicate the finish reason
- For most reliable results, use `gemini-1.5-pro-latest` or `gemini-1.5-flash`