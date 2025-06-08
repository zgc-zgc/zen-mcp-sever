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
- "Ask gemini to think deeper about this architecture design"
- "Have gemini review this code for security issues"  
- "Get gemini to debug why this test is failing"
- "Ask gemini to analyze these files to understand the data flow"

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
**When Claude needs to go deeper on complex problems**

#### Example Prompts:

**Basic Usage:**
```
"Ask gemini to think deeper about my authentication design"
"Have gemini ultrathink on this distributed system architecture" 
"Get gemini to extend my analysis of this performance issue"
```

**With Focus Areas:**
```
"Ask gemini to think deeper about my caching strategy, focusing on performance and scalability"
"Have gemini extend my analysis of the payment system, focus on security and error handling"
"Get gemini to validate my microservices design focusing on fault tolerance and data consistency"
```

**With Reference Files:**
```
"Ask gemini to think deeper about my API design with reference to api/routes.py and api/models.py"
"Have gemini challenge my database schema design, reference schema.sql and models/"
"Get gemini to extend my optimization analysis with context from profiler_output.txt and metrics.log"
```

**Advanced Examples:**
```
"I've designed a real-time chat system using WebSockets. Ask gemini to think deeper about my approach, focusing on scalability and message ordering, with reference to chat/server.py and chat/client.js"

"Here's my plan for migrating from monolith to microservices. Have gemini extend this analysis focusing on data consistency and service boundaries, referencing current_architecture.md"

"I'm implementing a distributed cache. Get gemini to think deeper about edge cases like network partitions and cache invalidation strategies"
```

**Parameters Available:**
- `current_analysis`: Your current thinking (required)
- `problem_context`: Additional background information
- `focus_areas`: Specific aspects like ["security", "performance", "architecture"]
- `reference_files`: Files for additional context
- `temperature`: 0-1 (default 0.7 for creative thinking)
- `max_tokens`: Response length (default 8192)

**Key Capabilities:**
- Challenge assumptions constructively
- Identify overlooked edge cases
- Suggest alternative design patterns
- Evaluate scalability implications
- Consider security vulnerabilities
- Assess technical debt impact

**Triggers:** think deeper, ultrathink, extend my analysis, explore alternatives, validate my approach

### 2. `review_code` - Professional Code Review  
**Comprehensive code analysis with prioritized feedback**

#### Example Prompts:

**Basic Reviews:**
```
"Ask gemini to review auth.py for issues"
"Have gemini check the api/ directory for bugs"
"Get gemini to review my latest changes in main.py"
```

**Specialized Review Types:**
```
"Ask gemini to do a security review of auth/ focusing on authentication"
"Have gemini do a performance review of database/queries.py"
"Get gemini to do a quick review of utils.py - just critical issues"
"Ask gemini for a full review of the payment module"
```

**With Focus Areas:**
```
"Ask gemini to review api/endpoints.py focusing on input validation and error handling"
"Have gemini review models.py with focus on SQL injection vulnerabilities"
"Get gemini to check websocket.py focusing on memory leaks and connection handling"
```

**With Standards Enforcement:**
```
"Ask gemini to review src/ against PEP8 standards"
"Have gemini check frontend/ for ESLint rules and React best practices"
"Get gemini to review the Java code against Google Java Style Guide"
"Ask gemini to ensure api/ follows REST API design principles"
```

**With Severity Filtering:**
```
"Ask gemini to review the codebase but only show critical and high severity issues"
"Have gemini do a security review of auth/ - only report critical vulnerabilities"
"Get gemini to review database/ filtering for high severity performance issues"
```

**Advanced Examples:**
```
"Ask gemini to do a security review of auth/jwt.py focusing on token validation and OWASP top 10, enforce JWT best practices"

"Have gemini review the entire api/ directory for performance issues, focus on database queries and caching opportunities, only show high and critical issues"

"Get gemini to review payment/processor.py with focus on error handling and transaction safety, ensure PCI compliance standards"

"Ask gemini for a full review of user_management/ enforcing SOLID principles and clean code practices"
```

**Parameters Available:**
- `files`: Files or directories to review (required)
- `review_type`: "full", "security", "performance", "quick" (default: "full")
- `focus_on`: Specific aspects to emphasize
- `standards`: Coding standards to enforce
- `severity_filter`: "critical", "high", "medium", "all" (default: "all")
- `temperature`: 0-1 (default 0.2 for consistency)

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

### 3. `debug_issue` - Expert Debugging Assistant
**Root cause analysis for complex problems**

#### Example Prompts:

**Basic Debugging:**
```
"Ask gemini to debug this TypeError: 'NoneType' object has no attribute 'split'"
"Have gemini figure out why my API returns 500 errors"
"Get gemini to debug why this test is failing"
```

**With Error Context:**
```
"Ask gemini to debug this error with the full stack trace: [paste traceback]"
"Have gemini debug why the app crashes with this error log: [paste logs]"
"Get gemini to trace this exception with the context from debug.log"
```

**With Relevant Files:**
```
"Ask gemini to debug why user login fails, check auth/login.py and models/user.py"
"Have gemini debug this import error with context from app.py and requirements.txt"
"Get gemini to find why the API timeout occurs, relevant files: api/client.py and config.yaml"
```

**With Runtime Information:**
```
"Ask gemini to debug this memory leak. Runtime: Python 3.9, Django 4.2, PostgreSQL 14"
"Have gemini debug WebSocket drops. Environment: Node.js 18, Socket.io 4.5, behind nginx proxy"
"Get gemini to debug this deadlock. Stack: Java 17, Spring Boot, MySQL with connection pool size 10"
```

**With Previous Attempts:**
```
"Ask gemini to debug this race condition. I've tried adding locks but it still happens intermittently"
"Have gemini debug why migrations fail. Already tried: resetting db, checking permissions, updating drivers"
"Get gemini to find why tests fail on CI but pass locally. Tried: matching environments, clearing caches"
```

**Advanced Examples:**
```
"Ask gemini to debug this error: 'ConnectionPool limit exceeded'. Context: happens under load with 100+ concurrent users. Runtime: FastAPI with asyncpg, PostgreSQL 14. Relevant files: db/pool.py, api/handlers.py. Already tried increasing pool size to 50"

"Have gemini debug intermittent test failures in test_payment.py. Error: 'AssertionError: Transaction not found'. Only fails in parallel test runs. Previous attempts: added delays, used locks, isolated database"

"Get gemini to trace why the background job processor hangs. No error messages, just stops processing. Runtime: Celery 5.2 with Redis broker. Check: tasks/processor.py, celery_config.py. Tried: increasing timeout, adding logging"

"Ask gemini to debug this memory leak in the image processing service. Memory usage grows to 4GB after 1000 images. Stack: Python with Pillow, running in Docker. Files: image_processor.py, dockerfile"
```

**Parameters Available:**
- `error_description`: Error message or symptoms (required)
- `error_context`: Stack traces, logs, additional context
- `relevant_files`: Files that might be related to the issue
- `runtime_info`: Environment, versions, configuration details
- `previous_attempts`: What solutions have been tried already
- `temperature`: 0-1 (default 0.2 for accuracy)

**Triggers:** debug, error, failing, root cause, trace, not working, why is

### 4. `analyze` - Smart File Analysis
**General-purpose code understanding and exploration**

#### Example Prompts:

**Basic Analysis:**
```
"Ask gemini to analyze main.py to understand how it works"
"Have gemini examine the database models to explain the schema"
"Get gemini to analyze app.py and tell me what this application does"
```

**Multiple File Analysis:**
```
"Ask gemini to analyze main.py, config.py, and utils.py to understand the architecture"
"Have gemini examine all files in models/ to map out the data relationships"
"Get gemini to analyze api/ and services/ directories to understand the API structure"
```

**Specialized Analysis Types:**
```
"Ask gemini to do an architecture analysis of the src/ directory"
"Have gemini perform a security analysis on auth/ focusing on vulnerabilities"
"Get gemini to do a performance analysis of database/queries.py"
"Ask gemini for a quality analysis of the codebase looking for tech debt"
```

**With Custom Questions:**
```
"Ask gemini to analyze models.py and explain how the inheritance hierarchy works"
"Have gemini examine api/routes.py and identify all the endpoints and their purposes"
"Get gemini to analyze the middleware/ directory and explain the request flow"
"Ask gemini to look at tests/ and tell me what's not being tested"
```

**With Output Formats:**
```
"Ask gemini to analyze the project structure and give me a summary"
"Have gemini examine the codebase for anti-patterns - actionable format"
"Get gemini to analyze main.py in detail to understand every function"
```

**Advanced Examples:**
```
"Ask gemini to perform an architecture analysis of the entire project, examining main.py, app/, models/, and services/. Focus on identifying design patterns and potential circular dependencies"

"Have gemini do a security analysis of auth/, api/, and middleware/ to identify potential vulnerabilities and suggest improvements"

"Get gemini to analyze the data flow through pipeline/, processors/, and output/ directories. Question: How does data transformation work and where are the bottlenecks?"

"Ask gemini to analyze tests/, src/, and coverage.xml for a quality analysis. Give me actionable recommendations for improving test coverage"

"Have gemini examine the microservices in services/ directory for an architecture analysis. Focus on service boundaries and communication patterns. Output format: summary"
```

**Parameters Available:**
- `files`: Files or directories to analyze (required)
- `question`: What to analyze or look for (required)
- `analysis_type`: "architecture", "performance", "security", "quality", "general" (default: "general")
- `output_format`: "detailed", "summary", "actionable" (default: "detailed")
- `temperature`: 0-1 (default 0.2 for analytical accuracy)

**Special Features:**
- Always uses file paths (not content) = clean terminal output!
- Can analyze multiple files to understand relationships
- Identifies patterns and anti-patterns
- Suggests refactoring opportunities
- Maps dependencies and data flows

**Triggers:** analyze, examine, look at, understand, inspect, check

### 5. `chat` - General Development Chat
**For everything else - explanations, comparisons, brainstorming**

#### Example Prompts:

**Basic Questions:**
```
"Ask gemini to explain how async/await works in Python"
"Have gemini describe the differences between REST and GraphQL"
"Get gemini to explain SOLID principles with examples"
```

**Technology Comparisons:**
```
"Ask gemini to compare Redis vs Memcached for session storage"
"Have gemini explain when to use PostgreSQL vs MongoDB"
"Get gemini to compare React, Vue, and Angular for our use case"
```

**Best Practices:**
```
"Ask gemini about best practices for API versioning"
"Have gemini explain how to properly handle timezone data in Python"
"Get gemini's recommendations for microservice communication patterns"
```

**With Context Files:**
```
"Ask gemini to explain this algorithm with context from algorithm.py"
"Have gemini suggest improvements for this config, reference: config.yaml"
"Get gemini to explain how this library works, check package.json and main.js"
```

**Architecture & Design:**
```
"Ask gemini about the tradeoffs of event sourcing vs traditional CRUD"
"Have gemini explain when to use CQRS pattern and when to avoid it"
"Get gemini to suggest a caching strategy for our read-heavy API"
```

**Advanced Examples:**
```
"Ask gemini to explain the CAP theorem and how it applies to our distributed system design with context from architecture.md"

"Have gemini suggest a testing strategy for our microservices, considering both unit and integration tests"

"Get gemini to explain the pros and cons of using Kubernetes vs Docker Swarm for our deployment needs"

"Ask gemini about implementing zero-downtime deployments with our current stack: Node.js, PostgreSQL, Redis"
```

**Parameters Available:**
- `prompt`: Your question or topic (required)
- `context_files`: Optional files to provide context
- `temperature`: 0-1 (default 0.5 for balanced responses)

### 6. `list_models` - See Available Gemini Models
```
"Ask gemini to list available models"
"Have gemini show me what models I can use"
```

### 7. `get_version` - Server Information
```
"Ask gemini for its version"
"Have gemini show server configuration"
```

## Real-World Examples

### Example 1: Comprehensive Security Review
```
You: "Ask gemini to do a security review of auth/ directory focusing on JWT handling and session management, enforce OWASP standards, only show critical and high severity issues"

Gemini: 
SECURITY REVIEW (auth/)
Focus: JWT handling, session management | Standards: OWASP
==================================================

🔴 CRITICAL auth/jwt.py:45 - Hardcoded Secret Key
OWASP: A02:2021 - Cryptographic Failures
→ Impact: Anyone with code access can forge tokens
→ Fix: 
  import os
  SECRET_KEY = os.environ.get('JWT_SECRET')
  if not SECRET_KEY:
      raise ValueError("JWT_SECRET environment variable required")

🔴 CRITICAL auth/session.py:78 - No CSRF Protection
OWASP: A01:2021 - Broken Access Control  
→ Impact: Cross-site request forgery attacks possible
→ Fix: Implement double-submit cookie pattern
  csrf_token = secrets.token_urlsafe(32)
  response.set_cookie('csrf', csrf_token, httponly=True, samesite='Strict')

🟠 HIGH auth/validate.py:23 - Missing Token Expiration Check
→ Impact: Tokens valid forever, can't revoke access
→ Fix:
  import time
  if decoded.get('exp', 0) < time.time():
      raise TokenExpiredError("Token has expired")

SUMMARY: 2 critical, 1 high severity issues found
Priority: Fix hardcoded secret immediately in production
```

### Example 2: Complex Performance Debugging
```
You: "Ask gemini to debug why our API is slow. Error: Response times spike to 5s under load. Runtime: FastAPI, PostgreSQL 14, running on AWS ECS. Relevant files: api/endpoints.py, db/models.py, db/connection.py. Previous attempts: Added indexes, increased connection pool to 50, still happens"

Gemini:
DEBUG ANALYSIS: API Performance Issues
=====================================

ROOT CAUSE IDENTIFIED:
The performance degradation is caused by a combination of:
1. Synchronous database operations blocking the async event loop
2. Missing connection pooling configuration for async operations
3. Inefficient ORM queries with unnecessary JOINs

EVIDENCE:
- In api/endpoints.py:134 - Using sync SQLAlchemy session in async endpoint
- In db/connection.py:45 - Pool configured for sync operations only
- In db/models.py:89 - Eager loading relationships even when not needed

IMMEDIATE FIXES:
1. Switch to async database operations:
   ```python
   # db/connection.py
   from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
   
   engine = create_async_engine(
       "postgresql+asyncpg://...",
       pool_size=20,
       max_overflow=10,
       pool_pre_ping=True
   )
   ```

2. Update endpoints to use async sessions:
   ```python
   # api/endpoints.py
   async def get_users(db: AsyncSession = Depends(get_async_db)):
       result = await db.execute(select(User))
       return result.scalars().all()
   ```

LONG-TERM SOLUTIONS:
1. Implement query result caching with Redis
2. Add APM monitoring (e.g., DataDog, New Relic)
3. Consider read replicas for heavy read operations
4. Implement database query optimization middleware

VALIDATION:
After implementing async operations, expect:
- 80% reduction in response times under load
- Better connection pool utilization
- Linear scaling with concurrent requests up to pool limit
```

### Example 3: Architecture Deep Dive
```
You: "Ask gemini to analyze our microservices in services/ directory for an architecture analysis. Question: Are the service boundaries correct and how can we improve inter-service communication? Output format: detailed"

Gemini:
ARCHITECTURE ANALYSIS: Microservices
===================================

CURRENT ARCHITECTURE:
```
services/
├── user-service/      (User management, authentication)
├── order-service/     (Order processing, inventory)
├── payment-service/   (Payment processing, billing)
├── notification-service/ (Email, SMS, push notifications)
└── analytics-service/ (Reporting, metrics)
```

SERVICE BOUNDARY ANALYSIS:

✅ WELL-DEFINED BOUNDARIES:
1. payment-service: Clear single responsibility
2. notification-service: Good abstraction of communication channels

❌ BOUNDARY VIOLATIONS FOUND:
1. order-service includes inventory management
   - Should be separate inventory-service
   - Orders should only reference inventory
   
2. user-service handles authentication
   - Authentication should be separate auth-service
   - Users and auth have different scaling needs

INTER-SERVICE COMMUNICATION ISSUES:

1. SYNCHRONOUS HTTP EVERYWHERE
   - Current: All services use REST APIs
   - Problem: Cascading failures, high latency
   - Solution: Event-driven for non-critical paths

2. NO SERVICE DISCOVERY
   - Current: Hardcoded service URLs
   - Problem: No resilience, manual updates
   - Solution: Implement Consul or Kubernetes services

3. MISSING CIRCUIT BREAKERS
   - Current: Direct HTTP calls with basic retry
   - Problem: Thundering herd, cascade failures
   - Solution: Hystrix or resilience4j patterns

RECOMMENDED ARCHITECTURE:
1. Split services:
   - order-service → order-service + inventory-service
   - user-service → user-service + auth-service

2. Implement event bus (Kafka/RabbitMQ):
   - Order events → Inventory updates (async)
   - Payment complete → Order fulfillment (async)
   - All services → Analytics (async)

3. Add API Gateway:
   - Single entry point
   - Request routing
   - Rate limiting
   - Authentication

4. Communication patterns:
   - Sync: API Gateway → Service (user queries)
   - Async: Service → Service (events)
   - Cache: Redis for read-heavy operations

MIGRATION PATH:
Phase 1: Add message bus, start publishing events
Phase 2: Services consume events alongside HTTP
Phase 3: Remove service-to-service HTTP calls
Phase 4: Extract inventory and auth services
```

## Power User Workflows

### 1. **Claude + Gemini Deep Architecture Design**
```
You: "I need to design a real-time collaborative editor like Google Docs"
Claude: [provides initial architecture with WebSockets and operational transforms]

You: "Ask gemini to think deeper about the conflict resolution system, focusing on 
scalability and edge cases like network partitions, with reference to my design above"

Gemini: "Extended Analysis: Your operational transform approach is solid but consider:
1. CRDT Alternative: For better partition tolerance, use Yjs or Automerge
2. Edge Case: Simultaneous edits at same position during network split
3. Scale Issue: OT server becomes bottleneck at 10K+ concurrent users
4. Solution: Hybrid approach - CRDTs for text, OT for formatting..."

You: "Based on Gemini's insights, implement the hybrid CRDT/OT system"
Claude: [implements improved architecture with both approaches]
```

### 2. **Multi-Stage Security Audit**
```
You: "We're launching our payment system next week. Need a thorough security check"

You: "Ask gemini to do a security review of payment/, auth/, and api/ enforcing 
PCI compliance standards, focus on payment processing and data handling"

Gemini: [identifies 3 critical issues: plain text card storage, missing rate limiting, 
vulnerable to timing attacks]

You: "Fix the critical issues Gemini found, especially the card storage"
Claude: [implements tokenization, adds rate limiting, constant-time comparisons]

You: "Ask gemini to review the fixes I just made and check for any remaining issues"
Gemini: "Fixes look good. Additional recommendations: Add audit logging, implement 
fraud detection webhooks, consider 3D Secure for high-risk transactions"
```

### 3. **Production Issue Debugging Flow**
```
Situation: Production API crashing under load

You: "Our API keeps crashing. Here's the error log: [OOM killed, memory usage graph]"

You: "Ask gemini to debug this out-of-memory issue. Runtime: Node.js 18, Express, 
MongoDB. Relevant files: api/handlers/, db/queries.js. Previous attempts: Increased 
memory to 4GB, added pm2 clustering, still crashes at 500 concurrent users"

Gemini: "ROOT CAUSE: Memory leak from unclosed MongoDB cursors
- handlers/search.js:145 creates cursor but never closes on error
- Cursor timeout is 10 minutes, accumulating during high load
IMMEDIATE FIX: Add try-finally blocks to ensure cursor.close()
LONG-TERM: Implement connection pooling with automatic cleanup"

You: "Implement the cursor cleanup fix Gemini identified"
Claude: [adds proper cursor management with try-finally blocks]

You: "Ask gemini to think deeper about our MongoDB connection strategy to prevent 
this in the future, reference the current db/connection.js"

Gemini: [provides connection pool architecture with automatic cleanup, monitoring, 
and circuit breakers]
```

### 4. **Code Quality Evolution**
```
You: "Our codebase is becoming hard to maintain. Let's do a quality assessment"

You: "Ask gemini to analyze src/ for a quality analysis, identify technical debt 
and give actionable improvements"

Gemini: [identifies: inconsistent error handling, mixed async patterns, 
circular dependencies, missing tests for critical paths]

You: "Create a refactoring plan based on Gemini's analysis"
Claude: [creates phased refactoring plan with priority order]

You: "Ask gemini to review phase 1 of our refactoring in refactor/phase1/, 
ensure we're following SOLID principles"

Gemini: "Phase 1 Review: Good progress on SRP, but found issues:
- UserService still has multiple responsibilities
- Missing dependency injection in 3 places
- Suggest extracting UserAuthenticationService"

You: "Apply Gemini's suggestions to complete phase 1"
Claude: [refactors following the feedback]
```

### 5. **Performance Optimization Pipeline**
```
You: "The data processing pipeline is too slow, need to optimize"

You: "Ask gemini to do a performance analysis of pipeline/, processors/, and 
workers/, identify bottlenecks"

Gemini: "Performance Analysis:
BOTTLENECKS:
1. Single-threaded JSON parsing in processors/transform.js
2. Synchronous file I/O blocking event loop
3. No batching - processing records one at a time

IMPACT: 
- Current: 100 records/sec
- Potential: 10,000 records/sec"

You: "Ask gemini to think deeper about the batching strategy, considering memory 
constraints and error handling"

Gemini: [provides detailed batching implementation with backpressure, memory limits, 
and partial batch retry logic]

You: "Implement the optimizations following Gemini's design"
Claude: [implements multi-threaded processing, async I/O, intelligent batching]
```

## Pro Tips

### Natural Language Triggers
The server recognizes natural phrases. Just talk normally:
- ❌ "Use the think_deeper tool with current_analysis parameter..."
- ✅ "Ask gemini to think deeper about this approach"

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
"Ask gemini to debug this error with context from app.py and config.py"
"Have gemini think deeper about my design, reference the current architecture.md"
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