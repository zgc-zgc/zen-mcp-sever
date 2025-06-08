# Gemini MCP Server

A Model Context Protocol (MCP) server that enables integration with Google's Gemini models, optimized for Gemini 2.5 Pro Preview with 1M token context window.

## How It Works with Claude

Once configured, Claude automatically discovers this server's capabilities. You can use natural language to invoke Gemini:
- "Ask Gemini about..."
- "Use Gemini to analyze this file..."
- "Have Gemini review this code..."

See [MCP_DISCOVERY.md](MCP_DISCOVERY.md) for detailed information about how Claude discovers and uses MCP servers.

## Features

- **Chat with Gemini**: Send prompts to Gemini 2.5 Pro Preview by default
- **Analyze Code**: Process large codebases with Gemini's 1M token context window
- **File Reading**: Automatically read and analyze multiple files
- **List Models**: View all available Gemini models
- **Configurable Parameters**: Adjust temperature, max tokens, and model selection
- **System Prompts**: Support for system prompts to set context
- **Developer Context**: Automatically uses developer-focused system prompt for Claude Code integration

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
- `max_tokens` (optional): Maximum tokens in response (default: 8192)
- `temperature` (optional): Temperature for randomness 0-1 (default: 0.7)
- `model` (optional): Model to use (default: gemini-2.5-pro-preview-06-05)

### analyze_code
Analyze code files or snippets with Gemini's massive context window. Perfect for when Claude hits token limits.

Parameters:
- `files` (optional): List of file paths to analyze
- `code` (optional): Direct code content to analyze
- `question` (required): Question or analysis request about the code
- `system_prompt` (optional): System prompt for context
- `max_tokens` (optional): Maximum tokens in response (default: 8192)
- `temperature` (optional): Temperature for randomness 0-1 (default: 0.3 for code)
- `model` (optional): Model to use (default: gemini-2.5-pro-preview-06-05)

Note: You must provide either `files` or `code` (or both).

### list_models
List all available Gemini models that support content generation.

## Usage Examples

### From Claude Code

When working with large files in Claude Code, you can use the Gemini server like this:

1. **Analyze a large file**:
   ```
   Use the gemini tool to analyze this file: /path/to/large/file.py
   Question: What are the main design patterns used in this code?
   ```

2. **Analyze multiple files**:
   ```
   Use gemini to analyze these files together:
   - /path/to/file1.py
   - /path/to/file2.py
   - /path/to/file3.py
   Question: How do these components interact with each other?
   ```

3. **Extended thinking with Gemini**:
   When Claude hits token limits, you can pass the entire context to Gemini for analysis.

## Models

The server defaults to `gemini-2.5-pro-preview-06-05` (the latest and most capable model) which supports:
- 1 million token context window
- Advanced reasoning capabilities
- Code understanding and analysis

Other available models:
- `gemini-1.5-pro-latest` - Stable Gemini 1.5 Pro
- `gemini-1.5-flash` - Fast Gemini 1.5 Flash model
- `gemini-2.0-flash` - Gemini 2.0 Flash
- And many more (use `list_models` to see all available)

## Requirements

- Python 3.8+
- Valid Google Gemini API key

## Notes

- The Gemini 2.5 Pro preview models may have safety restrictions that block certain prompts
- If a model returns a blocked response, the server will indicate the finish reason
- The server estimates tokens as ~4 characters per token
- Maximum context window is 1 million tokens (~4 million characters)
- When no system prompt is provided, the server automatically uses a developer-focused prompt similar to Claude Code

## Tips for Claude Code Users

1. When Claude says a file is too large, use the `analyze_code` tool with the file path
2. For architectural questions spanning multiple files, pass all relevant files to `analyze_code`
3. Use lower temperatures (0.1-0.3) for code analysis and higher (0.7-0.9) for creative tasks
4. The default model (2.5 Pro Preview) is optimized for large context understanding