# Usage Guide for Claude Code Users

## Quick Start

When using this Gemini MCP server from Claude Code, you can interact with it naturally. Here are the most common patterns:

## Basic Chat

Simply ask Claude to use the Gemini tool:

```
Ask Gemini: What are the key differences between async and sync programming in Python?
```

## Analyzing Large Files

When Claude can't handle a large file due to token limits:

```
Use Gemini to analyze this file: /path/to/very/large/file.py
Question: What are the main components and their relationships?
```

## Multiple File Analysis

For architectural understanding across files:

```
Use Gemini to analyze these files together:
- /src/models/user.py
- /src/controllers/auth.py
- /src/services/database.py
Question: How do these components work together for user authentication?
```

## Code Review

For detailed code review:

```
Have Gemini review this code:
[paste your code here]
Question: What improvements would you suggest for performance and maintainability?
```

## Extended Thinking

When you need deep analysis:

```
Use Gemini for extended analysis of /path/to/complex/algorithm.py
Question: Can you trace through the algorithm step by step and identify any edge cases?
```

## Model Selection

To use a specific model (like 2.5 Pro Preview):

```
Use Gemini with model gemini-2.5-pro-preview-06-05 to analyze...
```

## Tips

1. **File Paths**: Always use absolute paths when specifying files
2. **Questions**: Be specific about what you want to know
3. **Temperature**: Lower values (0.1-0.3) for factual analysis, higher (0.7-0.9) for creative tasks
4. **Context**: Gemini can handle up to 1M tokens (~4M characters)

## Common Commands

- "Use Gemini to analyze..."
- "Ask Gemini about..."
- "Have Gemini review..."
- "Get Gemini's opinion on..."
- "Use Gemini for extended thinking about..."

## Integration with Claude

The MCP server integrates seamlessly with Claude. When Claude recognizes you want to use Gemini (through phrases like "use gemini", "ask gemini", etc.), it will automatically invoke the appropriate tool with the right parameters.