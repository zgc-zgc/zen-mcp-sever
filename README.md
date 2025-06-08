# Gemini MCP Server

The ultimate development partner for Claude - a Model Context Protocol server that gives Claude access to Google's Gemini 2.5 Pro for extended thinking, code analysis, and problem-solving.

## Why This Server?

Claude is brilliant, but sometimes you need:
- **Extended thinking** on complex architectural decisions
- **Deep code analysis** across massive codebases  
- **Expert debugging** for tricky issues
- **Professional code reviews** with actionable feedback
- **A senior developer partner** to validate and extend ideas

This server makes Gemini your development sidekick, handling what Claude can't or extending what Claude starts.

## Quickstart (5 minutes)

### 1. Get a Gemini API Key
Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and generate a free API key.

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
- "Think deeper about this architecture design"
- "Review this code for security issues"  
- "Debug why this test is failing"
- "Analyze these files to understand the data flow"

## Available Tools

**Quick Overview:**
1. [`think_deeper`](#think_deeper---extended-reasoning-partner) - Extended reasoning and problem-solving
2. [`review_code`](#review_code---professional-code-review) - Professional code review with severity levels
3. [`debug_issue`](#debug_issue---expert-debugging-assistant) - Root cause analysis and debugging
4. [`analyze`](#analyze---smart-file-analysis) - General-purpose file and code analysis
5. [`chat`](#chat---general-development-chat) - General development conversations
6. [`list_models`](#list_models---see-available-gemini-models) - List available Gemini models
7. [`get_version`](#get_version---server-information) - Get server version and configuration

### `think_deeper` - Extended Reasoning Partner
**When Claude needs to go deeper on complex problems**

#### Example Prompts:
```
"Think deeper about my authentication design"
"Ultrathink on this distributed system architecture" 
"Extend my analysis of this performance issue"
"Challenge my assumptions about this approach"
"Explore alternative solutions for this caching strategy"
"Validate my microservices communication approach"
```

**Features:**
- Extends Claude's analysis with alternative approaches
- Finds edge cases and failure modes
- Validates architectural decisions  
- Suggests concrete implementations
- Temperature: 0.7 (creative problem-solving)

**Key Capabilities:**
- Challenge assumptions constructively
- Identify overlooked edge cases
- Suggest alternative design patterns
- Evaluate scalability implications
- Consider security vulnerabilities
- Assess technical debt impact

**Triggers:** think deeper, ultrathink, extend my analysis, explore alternatives, validate my approach

### `review_code` - Professional Code Review  
**Comprehensive code analysis with prioritized feedback**

#### Example Prompts:
```
"Review this code for issues"
"Security audit of auth.py"
"Quick review of my changes"
"Check this code against PEP8 standards"
"Review the authentication module focusing on OWASP top 10"
"Performance review of the database queries in models.py"
"Review api/ directory for REST API best practices"
```

**Review Types:**
- `full` - Complete review (default)
- `security` - Security-focused analysis
- `performance` - Performance optimization  
- `quick` - Critical issues only

**Output includes:**
- Issues by severity with color coding:
  - 🔴 CRITICAL: Security vulnerabilities, data loss risks
  - 🟠 HIGH: Bugs, performance issues, bad practices
  - 🟡 MEDIUM: Code smells, maintainability issues
  - 🟢 LOW: Style issues, minor improvements
- Specific fixes with code examples
- Overall quality assessment
- Top 3 priority improvements
- Positive aspects worth preserving

**Customization Options:**
- `focus_on`: Specific aspects to emphasize
- `standards`: Coding standards to enforce (PEP8, ESLint, etc.)
- `severity_filter`: Minimum severity to report

**Triggers:** review code, check for issues, find bugs, security check, code audit

### `debug_issue` - Expert Debugging Assistant
**Root cause analysis for complex problems**

#### Example Prompts:
```
"Debug this TypeError in my async function"
"Why is this test failing intermittently?"
"Trace the root cause of this memory leak"
"Debug this race condition"
"Help me understand why the API returns 500 errors under load"
"Debug why my WebSocket connections are dropping"
"Find the root cause of this deadlock in my threading code"
```

**Provides:**
- Root cause identification
- Step-by-step debugging approach
- Immediate fixes
- Long-term solutions
- Prevention strategies

**Input Options:**
- `error_description`: The error or symptom
- `error_context`: Stack traces, logs, error messages
- `relevant_files`: Files that might be involved
- `runtime_info`: Environment, versions, configuration
- `previous_attempts`: What you've already tried

**Triggers:** debug, error, failing, root cause, trace, not working, why is

### `analyze` - Smart File Analysis
**General-purpose code understanding and exploration**

#### Example Prompts:
```
"Analyze main.py to understand the architecture"
"Examine these files for circular dependencies"
"Look for performance bottlenecks in this module"
"Understand how these components interact"
"Analyze the data flow through the pipeline modules"
"Check if this module follows SOLID principles"
"Analyze the API endpoints to create documentation"
"Examine the test coverage and suggest missing tests"
```

**Analysis Types:**
- `architecture` - Design patterns, structure, dependencies
- `performance` - Bottlenecks, optimization opportunities
- `security` - Vulnerability assessment, security patterns
- `quality` - Code metrics, maintainability, test coverage
- `general` - Comprehensive analysis (default)

**Output Formats:**
- `detailed` - Comprehensive analysis (default)
- `summary` - High-level overview
- `actionable` - Focused on specific improvements

**Special Features:**
- Always uses file paths (not content) = clean terminal output!
- Can analyze multiple files to understand relationships
- Identifies patterns and anti-patterns
- Suggests refactoring opportunities

**Triggers:** analyze, examine, look at, understand, inspect, check

### `chat` - General Development Chat
**For everything else**

#### Example Prompts:
```
"Ask Gemini about the best caching strategy"
"Explain how async generators work"
"What's the difference between these design patterns?"
"Compare Redis vs Memcached for my use case"
"Explain the tradeoffs of microservices vs monolith"
"Best practices for handling timezone data in Python"
```

### `list_models` - See Available Gemini Models
```
"List available Gemini models"
"Show me what models I can use"
```

### `get_version` - Server Information
```
"Get Gemini server version"
"Show server configuration"
```

## Real-World Examples

### Example 1: Comprehensive Security Review
```
You: "Review the auth/ directory for security issues, focus on JWT handling"
Gemini: 
🔴 CRITICAL auth/jwt.py:45 - Secret key hardcoded
→ Fix: Use environment variable
  SECRET_KEY = os.environ.get('JWT_SECRET')

🟠 HIGH auth/validate.py:23 - No token expiration check
→ Fix: Add expiration validation
  if decoded['exp'] < time.time():
      raise TokenExpiredError()
```

### Example 2: Performance Debugging
```
You: "Debug why the API endpoint /users/search is slow"
Gemini:
ROOT CAUSE: N+1 query problem in user search
- Each user triggers separate query for roles
- 100 users = 101 database queries

IMMEDIATE FIX:
Add eager loading: User.query.options(joinedload('roles'))

LONG-TERM SOLUTION:
Implement query result caching with Redis
```

### Example 3: Architecture Analysis
```
You: "Analyze src/ to understand the architecture and identify improvements"
Gemini:
ARCHITECTURE OVERVIEW:
- Layered architecture: Controllers → Services → Repositories
- Good separation of concerns
- Dependency injection pattern used

ISSUES FOUND:
1. Circular dependency: UserService ↔ AuthService
2. Missing abstraction for external APIs
3. Business logic leaked into controllers

RECOMMENDATIONS:
1. Extract shared logic to UserAuthService
2. Add adapter pattern for external APIs
3. Move validation to service layer
```

## Power User Workflows

### 1. **Claude + Gemini Deep Thinking**
```
You: "Design a real-time collaborative editor"
Claude: [provides initial design]
You: "Think deeper about the conflict resolution"
Gemini: [explores CRDTs, operational transforms, edge cases]
You: "Update the design based on Gemini's insights"
Claude: [refines with deeper understanding]
```

### 2. **Comprehensive Code Review**
```
You: "Review api/auth.py focusing on security"
Gemini: [identifies SQL injection risk, suggests prepared statements]
You: "Fix the critical issues Gemini found"
Claude: [implements secure solution]
```

### 3. **Complex Debugging**
```
Claude: "I see the error but the root cause isn't clear..."
You: "Debug this with the error context and relevant files"
Gemini: [traces execution, identifies race condition]
You: "Implement Gemini's suggested fix"
```

### 4. **Architecture Validation**
```
You: "I've designed a microservices architecture [details]"
You: "Think deeper about scalability and failure modes"
Gemini: [analyzes bottlenecks, suggests circuit breakers, identifies edge cases]
```

## Pro Tips

### Natural Language Triggers
The server recognizes natural phrases. Just talk normally:
- ❌ "Use the think_deeper tool with current_analysis parameter..."
- ✅ "Think deeper about this approach"

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
"Debug this error with context from app.py and config.py"
"Think deeper about my design, reference the current architecture.md"
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