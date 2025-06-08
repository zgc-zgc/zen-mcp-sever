# How Claude Discovers and Uses MCP Servers

## MCP Server Discovery

When you configure an MCP server in Claude Desktop, Claude automatically discovers its capabilities through the MCP protocol:

1. **On Startup**: Claude connects to all configured MCP servers
2. **Tool Discovery**: Claude calls `list_tools()` to discover available tools
3. **Schema Understanding**: Each tool provides its input schema, which Claude uses to understand how to call it

## How This Gemini Server Appears in Claude

Once configured, this Gemini MCP server provides three tools that Claude can use:

### 1. `gemini_chat`
- Claude sees this as a way to chat with Gemini
- You can invoke it naturally: "Ask Gemini about...", "Use Gemini to..."

### 2. `gemini_analyze_code`
- Claude recognizes this for code analysis tasks
- Triggered by: "Use Gemini to analyze this file", "Have Gemini review this code"

### 3. `gemini_list_models`
- Lists available models
- Usually called automatically when needed

## Natural Language Usage

Claude is smart about understanding your intent. You don't need special syntax:

### Examples that work:
- "Ask Gemini what it thinks about quantum computing"
- "Use Gemini to analyze the file /path/to/large/file.py"
- "Have Gemini review this code for security issues"
- "Get Gemini's opinion on this architecture"
- "Pass this to Gemini for extended analysis"

### What happens behind the scenes:
1. Claude recognizes keywords like "Gemini", "analyze", "review"
2. Claude determines which tool to use based on context
3. Claude extracts parameters (files, questions, etc.) from your request
4. Claude calls the appropriate MCP tool
5. Claude presents the response back to you

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
3. Claude should list the Gemini tools

## Troubleshooting

If Claude doesn't recognize Gemini commands:
1. Check the MCP server icon shows "gemini" as connected
2. Verify your API key is set correctly
3. Check Claude's logs for connection errors
4. Try restarting Claude Desktop

## Integration with Claude Code

In Claude Code, the integration is even more seamless:
- Large file handling is automatic
- Claude will suggest using Gemini when hitting token limits
- File paths are resolved relative to your workspace