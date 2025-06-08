# Gemini MCP Server

The ultimate development partner for Claude - a Model Context Protocol server that gives Claude access to Google's Gemini 2.5 Pro for extended thinking, code analysis, and problem-solving.

## Why This Server?

Claude is brilliant, but sometimes you need:
- **A second opinion** on complex architectural decisions - augment Claude's extended thinking with Gemini's perspective
- **Massive context window** (1M tokens) - Gemini 2.5 Pro can analyze entire codebases, read hundreds of files at once, and provide comprehensive insights
- **Deep code analysis** across massive codebases that exceed Claude's context limits
- **Expert debugging** for tricky issues with full system context
- **Professional code reviews** with actionable feedback across entire repositories
- **A senior developer partner** to validate and extend ideas

This server makes Gemini your development sidekick, handling what Claude can't or extending what Claude starts.

## Quickstart (5 minutes)

### 1. Get a Gemini API Key
Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and generate an API key. For best results with Gemini 2.5 Pro, use a paid API key as the free tier has limited access to the latest models.

### 2. Install via Claude Desktop Config

Add to your `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gemini": {
      "command": "python",
      "args": ["/absolute/path/to/gemini-mcp-server/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-gemini-api-key-here"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

### 4. Connect to Claude Code

To use the server in Claude Code, run:
```bash
claude mcp add-from-claude-desktop -s user
```

### 5. Start Using It!

Just ask Claude naturally:
- "Use gemini to think deeper about this architecture design"
- "Get gemini to review this code for security issues"  
- "Get gemini to debug why this test is failing"
- "Use gemini to analyze these files to understand the data flow"

## Available Tools

**Quick Tool Selection Guide:**
- **Need deeper thinking?** → `think_deeper` (extends Claude's analysis, finds edge cases)
- **Code needs review?** → `review_code` (bugs, security, performance issues)
- **Something's broken?** → `debug_issue` (root cause analysis, error tracing)
- **Want to understand code?** → `analyze` (architecture, patterns, dependencies)
- **General questions?** → `chat` (explanations, comparisons, advice)
- **Check models?** → `list_models` (see available Gemini models)
- **Server info?** → `get_version` (version and configuration details)

**Tools Overview:**
1. [`think_deeper`](#1-think_deeper---extended-reasoning-partner) - Extended reasoning and problem-solving
2. [`review_code`](#2-review_code---professional-code-review) - Professional code review with severity levels
3. [`debug_issue`](#3-debug_issue---expert-debugging-assistant) - Root cause analysis and debugging
4. [`analyze`](#4-analyze---smart-file-analysis) - General-purpose file and code analysis
5. [`chat`](#5-chat---general-development-chat) - General development conversations
6. [`list_models`](#6-list_models---see-available-gemini-models) - List available Gemini models
7. [`get_version`](#7-get_version---server-information) - Get server version and configuration

### 1. `think_deeper` - Extended Reasoning Partner
**Get a second opinion to augment Claude's own extended thinking**

#### Example Prompts:

**Basic Usage:**
```
"Use gemini to think deeper about my authentication design"
"Use gemini to extend my analysis of this distributed system architecture"
```

**Collaborative Workflow:**
```
"Design an authentication system for our SaaS platform. Then use gemini to review your design for security vulnerabilities. After getting gemini's feedback, incorporate the suggestions and show me the final improved design."

"Create an event-driven architecture for our order processing system. Use gemini to think deeper about event ordering and failure scenarios. Then integrate gemini's insights and present the enhanced architecture."
```

**Key Features:**
- Provides a second opinion on Claude's analysis
- Challenges assumptions and identifies edge cases Claude might miss
- Offers alternative perspectives and approaches
- Validates architectural decisions and design patterns
- Can reference specific files for context: `"Use gemini to think deeper about my API design with reference to api/routes.py"`

**Triggers:** think deeper, ultrathink, extend my analysis, validate my approach

### 2. `review_code` - Professional Code Review  
**Comprehensive code analysis with prioritized feedback**

#### Example Prompts:

**Basic Usage:**
```
"Use gemini to review auth.py for issues"
"Use gemini to do a security review of auth/ focusing on authentication"
```

**Collaborative Workflow:**
```
"Refactor the authentication module to use dependency injection. Then use gemini to review your refactoring for any security vulnerabilities. Based on gemini's feedback, make any necessary adjustments and show me the final secure implementation."

"Optimize the slow database queries in user_service.py. Get gemini to review your optimizations for potential regressions or edge cases. Incorporate gemini's suggestions and present the final optimized queries."
```

**Key Features:**
- Issues prioritized by severity (🔴 CRITICAL → 🟢 LOW)
- Supports specialized reviews: security, performance, quick
- Can enforce coding standards: `"Use gemini to review src/ against PEP8 standards"`
- Filters by severity: `"Get gemini to review auth/ - only report critical vulnerabilities"`

**Triggers:** review code, check for issues, find bugs, security check

### 3. `debug_issue` - Expert Debugging Assistant
**Root cause analysis for complex problems**

#### Example Prompts:

**Basic Usage:**
```
"Use gemini to debug this TypeError: 'NoneType' object has no attribute 'split'"
"Get gemini to debug why my API returns 500 errors with the full stack trace: [paste traceback]"
```

**Collaborative Workflow:**
```
"I'm getting 'ConnectionPool limit exceeded' errors under load. Debug the issue and use gemini to analyze it deeper with context from db/pool.py. Based on gemini's root cause analysis, implement a fix and get gemini to validate the solution will scale."

"Debug why tests fail randomly on CI. Once you identify potential causes, share with gemini along with test logs and CI configuration. Apply gemini's debugging strategy, then use gemini to suggest preventive measures."
```

**Key Features:**
- Accepts error context, stack traces, and logs
- Can reference relevant files for investigation
- Supports runtime info and previous attempts
- Provides root cause analysis and solutions

**Triggers:** debug, error, failing, root cause, trace, not working

### 4. `analyze` - Smart File Analysis
**General-purpose code understanding and exploration**

#### Example Prompts:

**Basic Usage:**
```
"Use gemini to analyze main.py to understand how it works"
"Get gemini to do an architecture analysis of the src/ directory"
```

**Collaborative Workflow:**
```
"Analyze our project structure in src/ and identify architectural improvements. Share your analysis with gemini for a deeper review of design patterns and anti-patterns. Based on both analyses, create a refactoring roadmap."

"Perform a security analysis of our authentication system. Use gemini to analyze auth/, middleware/, and api/ for vulnerabilities. Combine your findings with gemini's to create a comprehensive security report."
```

**Key Features:**
- Analyzes single files or entire directories
- Supports specialized analysis types: architecture, performance, security, quality
- Uses file paths (not content) for clean terminal output
- Can identify patterns, anti-patterns, and refactoring opportunities

**Triggers:** analyze, examine, look at, understand, inspect

### 5. `chat` - General Development Chat
**For everything else - explanations, comparisons, brainstorming**

#### Example Prompts:

**Basic Usage:**
```
"Use gemini to explain how async/await works in Python"
"Get gemini to compare Redis vs Memcached for session storage"
```

**Collaborative Workflow:**
```
"Research the best message queue for our use case (high throughput, exactly-once delivery). Use gemini to compare RabbitMQ, Kafka, and AWS SQS. Based on gemini's analysis and your research, recommend the best option with implementation plan."

"Design a caching strategy for our API. Get gemini's input on Redis vs Memcached vs in-memory caching. Combine both perspectives to create a comprehensive caching implementation guide."
```

**Key Features:**
- General development questions and explanations
- Technology comparisons and best practices
- Architecture and design discussions
- Can reference files for context: `"Use gemini to explain this algorithm with context from algorithm.py"`

**Triggers:** ask, explain, compare, suggest, what about

### 6. `list_models` - See Available Gemini Models
```
"Use gemini to list available models"
"Get gemini to show me what models I can use"
```

### 7. `get_version` - Server Information
```
"Use gemini for its version"
"Get gemini to show server configuration"
```

## Collaborative Workflows

### Design → Review → Implement
```
"Design a real-time collaborative editor. Use gemini to think deeper about edge cases and scalability. Implement an improved version incorporating gemini's suggestions."
```

### Code → Review → Fix
```
"Implement JWT authentication. Get gemini to do a security review. Fix any issues gemini identifies and show me the secure implementation."
```

### Debug → Analyze → Solution
```
"Debug why our API crashes under load. Use gemini to analyze deeper with context from api/handlers/. Implement a fix based on gemini's root cause analysis."
```

## Pro Tips

### Natural Language Triggers
The server recognizes natural phrases. Just talk normally:
- ❌ "Use the think_deeper tool with current_analysis parameter..."
- ✅ "Use gemini to think deeper about this approach"

### Automatic Tool Selection
Claude will automatically pick the right tool based on your request:
- "review" → `review_code`
- "debug" → `debug_issue`
- "analyze" → `analyze`
- "think deeper" → `think_deeper`

### Clean Terminal Output
All file operations use paths, not content, so your terminal stays readable even with large files.

### Context Awareness
Tools can reference files for additional context:
```
"Use gemini to debug this error with context from app.py and config.py"
"Get gemini to think deeper about my design, reference the current architecture.md"
```

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

## Contributing

We welcome contributions! The modular architecture makes it easy to add new tools:

1. Create a new tool in `tools/`
2. Inherit from `BaseTool`
3. Implement required methods
4. Add to `TOOLS` in `server.py`

See existing tools for examples.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Built with [MCP](https://modelcontextprotocol.com) by Anthropic and powered by Google's Gemini API.