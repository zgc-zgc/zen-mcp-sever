# Gemini MCP Server for Claude Code

A specialized Model Context Protocol (MCP) server that extends Claude Code's capabilities with Google's Gemini 2.5 Pro Preview, featuring a massive 1M token context window for handling large codebases and complex analysis tasks.

## Purpose

This server acts as a developer assistant that augments Claude Code when you need:
- Analysis of files too large for Claude's context window
- Deep architectural reviews across multiple files
- Extended thinking and complex problem solving
- Performance analysis of large codebases
- Security audits requiring full codebase context

## Prerequisites

Before you begin, ensure you have the following:

1. **Python:** Python 3.10 or newer. Check your version with `python3 --version`
2. **Claude Desktop:** A working installation of Claude Desktop and the `claude` command-line tool
3. **Gemini API Key:** An active API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Ensure your key is enabled for the `gemini-2.5-pro-preview` model
4. **Git:** The `git` command-line tool for cloning the repository

## Quick Start for Claude Code

### 1. Clone the Repository

First, clone this repository to your local machine:
```bash
git clone https://github.com/BeehiveInnovations/gemini-mcp-server.git
cd gemini-mcp-server

# macOS/Linux only: Make the script executable
chmod +x run_gemini.sh
```

Note the full path to this directory - you'll need it for the configuration.

### 2. Configure in Claude Desktop

You can access the configuration file in two ways:
- **Through Claude Desktop**: Open Claude Desktop → Settings → Developer → Edit Config
- **Direct file access**: 
  - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
  - **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the following configuration, replacing the path with your actual directory path:

**macOS**:
```json
{
  "mcpServers": {
    "gemini": {
      "command": "/path/to/gemini-mcp-server/run_gemini.sh",
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

**Windows**:
```json
{
  "mcpServers": {
    "gemini": {
      "command": "C:\\path\\to\\gemini-mcp-server\\run_gemini.bat",
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

**Linux**:
```json
{
  "mcpServers": {
    "gemini": {
      "command": "/path/to/gemini-mcp-server/run_gemini.sh",
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

**Important**: Replace the path with the actual absolute path where you cloned the repository:
- **macOS example**: `/Users/yourname/projects/gemini-mcp-server/run_gemini.sh`
- **Windows example**: `C:\\Users\\yourname\\projects\\gemini-mcp-server\\run_gemini.bat`
- **Linux example**: `/home/yourname/projects/gemini-mcp-server/run_gemini.sh`

### 3. Restart Claude Desktop

After adding the configuration, restart Claude Desktop. You'll see "gemini" in the MCP servers list.

### 4. Add to Claude Code

To make the server available in Claude Code, run:
```bash
# This command reads your Claude Desktop configuration and makes
# the "gemini" server available in your terminal
claude mcp add-from-claude-desktop -s user
```

### 5. Start Using Natural Language

Just talk to Claude naturally:
- "Use gemini analyze_file on main.py to find bugs"
- "Share your analysis with gemini extended_think for deeper insights"
- "Ask gemini to review the architecture using analyze_file"

**Key tools:**
- `analyze_file` - Clean file analysis without terminal clutter
- `extended_think` - Collaborative deep thinking with Claude's analysis
- `chat` - General conversations
- `analyze_code` - Legacy tool (prefer analyze_file for files)

## How It Works

This server acts as a local proxy between Claude Code and the Google Gemini API, following the Model Context Protocol (MCP):

1. You issue a command to Claude (e.g., "Ask Gemini to...")
2. Claude Code sends a request to the local MCP server defined in your configuration
3. This server receives the request, formats it for the Gemini API, and includes any file contents
4. The request is sent to the Google Gemini API using your API key
5. The server receives the response from Gemini
6. The response is formatted and streamed back to Claude, who presents it to you

All processing and API communication happens locally from your machine. Your API key is never exposed to Anthropic.

## Developer-Optimized Features

### Automatic Developer Context
When no custom system prompt is provided, Gemini automatically operates with deep developer expertise, focusing on:
- Clean code principles
- Performance optimization
- Security best practices
- Architectural patterns
- Testing strategies
- Modern development practices

### Optimized Temperature Settings
- **General chat**: 0.5 (balanced accuracy with some creativity)
- **Code analysis**: 0.2 (high precision for code review)

### Large Context Window
- Handles up to 1M tokens (~4M characters)
- Perfect for analyzing entire codebases
- Maintains context across multiple large files

## Available Tools

### `chat`
General-purpose developer conversations with Gemini.

**Example uses:**
```
"Ask Gemini about the best approach for implementing a distributed cache"
"Use Gemini to explain the tradeoffs between different authentication strategies"
```

### `analyze_code` (Legacy)
Analyzes code files or snippets. For better terminal output, use `analyze_file` instead.

### `analyze_file` (Recommended for Files)
Clean file analysis - always uses file paths, never shows content in terminal.

**Example uses:**
```
"Use gemini analyze_file on README.md to find issues"
"Ask gemini to analyze_file main.py for performance problems"
"Have gemini analyze_file on auth.py, users.py, and permissions.py together"
```

**Benefits:**
- Terminal always stays clean - only shows "Analyzing N file(s)"
- Server reads files directly and sends to Gemini
- No need to worry about prompt phrasing
- Supports multiple files in one request

### `extended_think`
Collaborate with Gemini on complex problems by sharing Claude's analysis for deeper insights.

**Example uses:**
```
"Share your analysis with gemini extended_think for deeper insights"
"Use gemini extended_think to validate and extend your architectural design"
"Ask gemini to extend your thinking on this security analysis"
```

**Advanced usage with focus areas:**
```
"Use gemini extended_think with focus='performance' to drill into scaling issues"
"Share your design with gemini extended_think focusing on security vulnerabilities"
"Get gemini to extend your analysis with focus on edge cases"
```

**Features:**
- Takes Claude's thoughts, plans, or analysis as input
- Optional file context for reference
- Configurable focus areas (architecture, bugs, performance, security)
- Higher temperature (0.7) for creative problem-solving
- Designed for collaborative thinking, not just code review

### `list_models`
Lists available Gemini models (defaults to 2.5 Pro Preview).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BeehiveInnovations/gemini-mcp-server.git
   cd gemini-mcp-server
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

## Advanced Configuration

### Custom System Prompts
Override the default developer prompt when needed:
```python
{
  "prompt": "Review this code",
  "system_prompt": "You are a security expert. Focus only on vulnerabilities."
}
```

### Temperature Control
Adjust for your use case:
- `0.1-0.3`: Maximum precision (debugging, security analysis)
- `0.4-0.6`: Balanced (general development tasks)
- `0.7-0.9`: Creative solutions (architecture design, brainstorming)

### Model Selection
While defaulting to `gemini-2.5-pro-preview-06-05`, you can specify other models:
- `gemini-1.5-pro-latest`: Stable alternative
- `gemini-1.5-flash`: Faster responses
- Use `list_models` to see all available options

## Claude Code Integration Examples

### When Claude hits token limits:
```
Claude: "This file is too large for me to analyze fully..."
You: "Use Gemini to analyze the entire file and identify the main components"
```

### For architecture reviews:
```
You: "Use Gemini to analyze all files in /src/core/ and create an architecture diagram"
```

### For performance optimization:
```
You: "Have Gemini profile this codebase and suggest the top 5 performance improvements"
```

## Practical Usage Tips

### Effective Commands
Be specific about what you want from Gemini:
- Good: "Ask Gemini to identify memory leaks in this code"
- Bad: "Ask Gemini about this"

### Clean Terminal Output
When analyzing files, explicitly mention the files parameter:
- "Use gemini analyze_code with files=['app.py'] to find bugs"
- "Analyze package.json using gemini's files parameter"
This prevents Claude from displaying the entire file content in your terminal.

### Common Workflows

#### 1. **Extended Thinking Partnership**
```
You: "Design a distributed task queue system"
Claude: [provides detailed architecture and implementation plan]
You: "Use gemini extended_think to validate and extend this design"
Gemini: [identifies gaps, suggests alternatives, finds edge cases]
You: "Address the issues Gemini found"
Claude: [updates design with improvements]
```

#### 2. **Clean File Analysis (No Terminal Clutter)**
```
"Use gemini analyze_file on engine.py to find performance issues"
"Ask gemini to analyze_file database.py and suggest optimizations"
"Have gemini analyze_file on all files in /src/core/"
```

#### 3. **Multi-File Architecture Review**
```
"Use gemini analyze_file on auth.py, users.py, permissions.py to map dependencies"
"Ask gemini to analyze_file the entire /src/api/ directory for security issues"
"Have gemini analyze_file all model files to check for N+1 queries"
```

#### 4. **Deep Collaborative Analysis**
```
Claude: "Here's my analysis of the memory leak: [detailed investigation]"
You: "Share this with gemini extended_think focusing on root causes"

Claude: "I've designed this caching strategy: [detailed design]"
You: "Use gemini extended_think with focus='performance' to stress-test this design"

Claude: "Here's my security assessment: [findings]"
You: "Get gemini to extended_think on this with files=['auth.py', 'crypto.py'] for context"
```

#### 4. **Claude-Driven Design with Gemini Validation**
```
Claude: "I've designed a caching strategy using Redis with TTL-based expiration..."
You: "Share my caching design with Gemini and ask for edge cases I might have missed"

Claude: "Here's my implementation plan for the authentication system: [detailed plan]"
You: "Use Gemini to analyze this plan and identify security vulnerabilities or scalability issues"

Claude: "I'm thinking of using this approach for the data pipeline: [approach details]"
You: "Have Gemini review my approach and check these 10 files for compatibility issues"
```

#### 5. **Security & Performance Audits**
```
"Use Gemini to security audit this authentication flow"
"Have Gemini identify performance bottlenecks in this codebase"
"Ask Gemini to check for common security vulnerabilities"
```

### Best Practices
- Let Claude do the primary thinking and design work
- Use Gemini as a validation layer for edge cases and extended context
- Share Claude's complete thoughts with Gemini for comprehensive review
- Have Gemini analyze files that are too large for Claude
- Use the feedback loop: Claude designs → Gemini validates → Claude refines

### Real-World Example Flow
```
1. You: "Create a microservices architecture for our e-commerce platform"
2. Claude: [Designs comprehensive architecture with service boundaries, APIs, data flow]
3. You: "Take my complete architecture design and have Gemini analyze it for:
   - Potential bottlenecks
   - Missing error handling
   - Security vulnerabilities
   - Scalability concerns"
4. Gemini: [Provides detailed analysis with specific concerns]
5. You: "Based on Gemini's analysis, update the architecture"
6. Claude: [Refines design addressing all concerns]
```

## Notes

- Gemini 2.5 Pro Preview may occasionally block certain prompts due to safety filters
- If a prompt is blocked by Google's safety filters, the server will return a clear error message to Claude explaining why the request could not be completed
- Token estimation: ~4 characters per token
- All file paths should be absolute paths

## Troubleshooting

### Server Not Appearing in Claude

- **Check JSON validity:** Ensure your `claude_desktop_config.json` file is valid JSON (no trailing commas, proper quotes)
- **Verify absolute paths:** The `command` path must be an absolute path to `run_gemini.sh` or `run_gemini.bat`
- **Restart Claude Desktop:** Always restart Claude Desktop completely after any configuration change

### Gemini Commands Fail

- **"API Key not valid" errors:** Verify your `GEMINI_API_KEY` is correct and active in [Google AI Studio](https://aistudio.google.com/app/apikey)
- **"Permission denied" errors:** 
  - Ensure your API key is enabled for the `gemini-2.5-pro-preview` model
  - On macOS/Linux, check that `run_gemini.sh` has execute permissions (`chmod +x run_gemini.sh`)
- **Network errors:** If behind a corporate firewall, ensure requests to `https://generativelanguage.googleapis.com` are allowed

### Common Setup Issues

- **"Module not found" errors:** The virtual environment may not be activated. See the Installation section
- **`chmod: command not found` (Windows):** The `chmod +x` command is for macOS/Linux only. Windows users can skip this step
- **Path not found errors:** Use absolute paths in all configurations, not relative paths like `./run_gemini.sh`

## Testing

### Running Tests Locally

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_gemini_server.py

# Generate HTML coverage report
pytest --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Continuous Integration

This project uses GitHub Actions for automated testing:
- Tests run on every push and pull request
- Supports Python 3.8 - 3.12
- Tests on Ubuntu, macOS, and Windows
- Includes linting with flake8, black, isort, and mypy
- Maintains 80%+ code coverage

## Contributing

This server is designed specifically for Claude Code users. Contributions that enhance the developer experience are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License - feel free to customize for your development workflow.