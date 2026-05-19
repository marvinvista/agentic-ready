Agentic readiness: Discoverable
Target: https://developer.zendesk.com
Score: 2/5

Why agents drop you:
1. No machine-readable API, MCP, SDK, auth, or sandbox path was found.
2. Buying and usage friction require a human to interpret.
3. The defensible output layer is not visible.

Next best fix:
Publish OpenAPI or MCP, auth docs, and a sandbox/test-mode example.

Evidence:
- Find: pass - docs (index.html), api reference (index.html)
- Call: fail - none
- Trust: pass - versioning (index.html), status/security (index.html)
- Buy: fail - none
- Defend: partial - integrations (index.html)

Warnings:
- Could not fetch https://developer.zendesk.com/llms.txt: HTTP Error 404: Not Found
- Could not fetch https://developer.zendesk.com/robots.txt: HTTP Error 404: Not Found
- Could not fetch https://developer.zendesk.com/sitemap.xml: HTTP Error 404: Not Found
- Could not fetch https://developer.zendesk.com/agentic-ready.json: HTTP Error 404: Not Found
- Could not fetch https://developer.zendesk.com/.well-known/agentic-ready.json: HTTP Error 404: Not Found
