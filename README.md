# Gemini MCP Server for Claude Code

A specialized Model Context Protocol (MCP) server that extends Claude Code's capabilities with Google's Gemini 2.5 Pro Preview, featuring a massive 1M token context window for handling large codebases and complex analysis tasks.

## 🎯 Purpose

This server acts as a developer assistant that augments Claude Code when you need:
- Analysis of files too large for Claude's context window
- Deep architectural reviews across multiple files
- Extended thinking and complex problem solving
- Performance analysis of large codebases
- Security audits requiring full codebase context

## 🚀 Quick Start for Claude Code

### 1. Configure in Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
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

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
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

### 2. Restart Claude Desktop

After adding the configuration, restart Claude Desktop. You'll see "gemini" in the MCP servers list.

### 3. Add to Claude Code

To make the server available in Claude Code, run:
```bash
claude mcp add-from-claude-desktop -s user
```

### 4. Start Using Natural Language

Just talk to Claude naturally:
- "Use Gemini to analyze this large file..."
- "Ask Gemini to review the architecture of these files..."
- "Have Gemini check this codebase for security issues..."

## 💻 Developer-Optimized Features

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

## 🛠️ Available Tools

### `chat`
General-purpose developer conversations with Gemini.

**Example uses:**
```
"Ask Gemini about the best approach for implementing a distributed cache"
"Use Gemini to explain the tradeoffs between different authentication strategies"
```

### `analyze_code`
Specialized tool for analyzing large files or multiple files that exceed Claude's limits.

**Example uses:**
```
"Use Gemini to analyze /src/core/engine.py and identify performance bottlenecks"
"Have Gemini review these files together: auth.py, users.py, permissions.py"
```

### `list_models`
Lists available Gemini models (defaults to 2.5 Pro Preview).

## 📋 Installation

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

## 🔧 Advanced Configuration

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

## 🎯 Claude Code Integration Examples

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

## 💡 Practical Usage Tips

### Effective Commands
Be specific about what you want from Gemini:
- ✅ "Ask Gemini to identify memory leaks in this code"
- ❌ "Ask Gemini about this"

### Common Workflows

#### 1. **Extended Code Review**
```
You: "Implement feature X"
Claude: [implements]
You: "Use Gemini to review this implementation for scalability issues"
Gemini: [provides detailed feedback]
You: "Based on Gemini's feedback, improve the implementation"
Claude: [refines based on feedback]
```

#### 2. **Large File Analysis**
```
"Use Gemini to analyze /path/to/large/file.py and summarize its architecture"
"Have Gemini trace all function calls in this module"
"Ask Gemini to identify unused code in this file"
```

#### 3. **Multi-File Context**
```
"Use Gemini to analyze how auth.py, users.py, and permissions.py work together"
"Have Gemini map the data flow between these components"
"Ask Gemini to find all circular dependencies in /src"
```

#### 4. **Second Opinion & Validation**
```
"I'm planning to refactor using pattern X. Ask Gemini for potential issues"
"Use Gemini to validate my database schema design"
"Have Gemini suggest alternative approaches to this algorithm"
```

#### 5. **Security & Performance Audits**
```
"Use Gemini to security audit this authentication flow"
"Have Gemini identify performance bottlenecks in this codebase"
"Ask Gemini to check for common security vulnerabilities"
```

### Best Practices
- Use Gemini when you need analysis beyond Claude's context window
- Leverage Gemini's 1M token limit for whole-codebase analysis
- Combine both assistants: Claude for implementation, Gemini for review
- Be specific in your requests for more accurate responses

## 📝 Notes

- Gemini 2.5 Pro Preview may occasionally block certain prompts due to safety filters
- The server automatically falls back gracefully when this happens
- Token estimation: ~4 characters per token
- All file paths should be absolute paths

## 🧪 Testing

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

## 🤝 Contributing

This server is designed specifically for Claude Code users. Contributions that enhance the developer experience are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

MIT License - feel free to customize for your development workflow.