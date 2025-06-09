# How Claude Discovers and Uses MCP Servers

## MCP Server Discovery

When you configure an MCP server in Claude Desktop, Claude automatically discovers its capabilities through the MCP protocol:

1. **On Startup**: Claude connects to all configured MCP servers
2. **Tool Discovery**: Claude calls `list_tools()` to discover available tools
3. **Schema Understanding**: Each tool provides its input schema, which Claude uses to understand how to call it

## How This Gemini Server Appears in Claude

Once configured, this Gemini MCP server provides these powerful tools:

### 1. `chat` - Collaborative Thinking Partner
- Claude sees this as a way to collaborate with Gemini on thinking and problem-solving
- Perfect for: brainstorming, getting second opinions, validating approaches
- Triggered by: "Brainstorm with Gemini", "Share my thinking with Gemini", "Get Gemini's opinion"

### 2. `think_deeper` - Extended Reasoning
- Challenges assumptions and explores alternatives
- Triggered by: "Use Gemini to think deeper", "Extend my analysis with Gemini"

### 3. `analyze` - Code & File Analysis
- Analyzes files and directories for patterns, architecture, and insights
- Triggered by: "Use Gemini to analyze", "Get Gemini to examine this code"

### 4. `review_code` - Professional Code Review
- Provides prioritized feedback on code quality and issues
- Triggered by: "Use Gemini to review", "Get Gemini to check for bugs"

### 5. `debug_issue` - Expert Debugging
- Root cause analysis for complex problems
- Triggered by: "Use Gemini to debug", "Get Gemini to trace this error"

### 6. `list_models` & `get_version`
- Utility tools for configuration and model info

## Natural Language Usage

Claude is smart about understanding your intent. You don't need special syntax:

### Examples that work:

**Collaborative Thinking:**
- "Share my authentication design with Gemini and get their opinion"
- "Brainstorm with Gemini about scaling strategies"
- "I'm thinking of using microservices - discuss this with Gemini"
- "Get Gemini's perspective on my implementation plan"

**Deep Analysis:**
- "Use Gemini to think deeper about edge cases in my design"
- "Get Gemini to analyze the entire src/ directory architecture"
- "Have Gemini review this code for security issues"
- "Use Gemini to debug why this test is failing"

**General Development:**
- "Ask Gemini to explain async/await in Python"
- "Get Gemini to compare Redis vs Memcached"
- "Use Gemini to suggest optimization strategies"

### What happens behind the scenes:
1. Claude recognizes keywords like "Gemini", "brainstorm", "discuss", "opinion", "analyze", "review", "debug"
2. Claude determines which tool to use based on context:
   - Collaborative thinking → `chat`
   - Deep analysis → `think_deeper`
   - Code examination → `analyze` or `review_code`
   - Problem solving → `debug_issue`
3. Claude extracts parameters (files, questions, context) from your request
4. Claude calls the appropriate MCP tool with your context
5. Claude integrates Gemini's response into the conversation

## Configuration in Claude Desktop

### macOS
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "/path/to/gemini-mcp-server/venv/bin/python",
      "args": ["/path/to/gemini-mcp-server/gemini_server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Windows
Add to `%APPDATA%\Claude\claude_desktop_config.json`

### After Configuration
1. Restart Claude Desktop
2. Claude will automatically connect to the Gemini server
3. You'll see "gemini" in the MCP servers list (bottom of Claude interface)
4. Start using natural language to invoke Gemini!

## Verification

To verify the server is connected:
1. Look for the MCP icon in Claude's interface
2. Ask Claude: "What MCP tools are available?"
3. Claude should list the Gemini tools including:
   - `chat` for collaborative thinking
   - `think_deeper` for extended analysis
   - `analyze`, `review_code`, `debug_issue` for development tasks
4. Try: "Brainstorm with Gemini about improving code performance"

## Troubleshooting

If Claude doesn't recognize Gemini commands:
1. Check the MCP server icon shows "gemini" as connected
2. Verify your API key is set correctly
3. Check Claude's logs for connection errors
4. Try restarting Claude Desktop

## Integration with Claude Code

In Claude Code, the integration is even more seamless:
- Claude can use Gemini as a thinking partner during complex tasks
- Share your implementation plans with Gemini for validation
- Get second opinions on architectural decisions
- Collaborate on debugging tricky issues
- Large file handling is automatic
- Claude will suggest using Gemini when hitting token limits
- File paths are resolved relative to your workspace