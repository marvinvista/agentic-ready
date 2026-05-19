from __future__ import annotations

DIMENSIONS = (
    {
        "key": "find",
        "name": "Find",
        "drop_reason": "Agents cannot find a machine-readable product surface.",
        "fix": "Publish llms.txt, sitemap.xml, docs, and an API or agent manifest.",
        "strong": (
            ("llms.txt", r"(^|/)llms\.txt$"),
            ("sitemap", r"(^|/)sitemap\.xml$"),
            ("well-known manifest", r"(^|/)\.well-known/"),
            ("agent manifest", r"(^|/)agentic-ready\.json$"),
            ("docs", r"(^|/)docs?(/|\.|$)|\bdocumentation\b|\bquickstart\b"),
            ("api reference", r"\bapi reference\b|\bendpoints?\b|\bopenapi\b|\bswagger\b"),
        ),
    },
    {
        "key": "call",
        "name": "Call",
        "drop_reason": "No machine-readable API, MCP, SDK, auth, or sandbox path was found.",
        "fix": "Publish OpenAPI or MCP, auth docs, and a sandbox/test-mode example.",
        "strong": (
            ("openapi", r"(^|/)(openapi|swagger)\.(json|ya?ml)$|\bopenapi\b|\bswagger\b"),
            ("mcp", r"\bmcp\b|model context protocol|inputSchema|tool definitions?"),
            ("sdk", r"\bsdk\b|\bclient library\b"),
            ("auth", r"\bapi keys?\b|\boauth\b|\bbearer\b|\bservice accounts?\b|\bscopes?\b"),
            ("sandbox", r"\bsandbox\b|\btest mode\b|\bmock server\b|\bplayground\b"),
        ),
    },
    {
        "key": "trust",
        "name": "Trust",
        "drop_reason": "The output contract is not clear enough for automated use.",
        "fix": "Add schemas, structured examples, error docs, versioning, and status/security proof.",
        "strong": (
            ("schema", r"\bjson schema\b|\bresponse schema\b|\binputSchema\b|\bcomponents\b"),
            ("structured example", r"\bapplication/json\b|\bsample response\b|\bexample response\b"),
            ("errors", r"\berror codes?\b|\berror model\b|\bproblem\+json\b"),
            ("versioning", r"\bversioning\b|\bdeprecation\b|\bchangelog\b"),
            ("status/security", r"\bstatus\b|\buptime\b|\bsecurity\b|\bsoc\s*2\b|\bsla\b"),
        ),
    },
    {
        "key": "buy",
        "name": "Buy",
        "drop_reason": "Buying and usage friction require a human to interpret.",
        "fix": "Expose pricing, plan boundaries, usage limits, rate limits, and a free/sandbox path.",
        "strong": (
            ("pricing", r"(^|/)pricing(/|\.|$)|\bpricing\b|\bplans?\b"),
            ("usage limits", r"\brate limits?\b|\busage limits?\b|\boverage\b|\bcredits?\b|\bmeter(ed|ing)\b"),
            ("free/sandbox path", r"\bfree plan\b|\bfree trial\b|\bsandbox\b|\btest mode\b"),
        ),
    },
    {
        "key": "defend",
        "name": "Defend",
        "drop_reason": "The defensible output layer is not visible.",
        "fix": "State what agents cannot cheaply reproduce: proprietary data, systems of record, integrations, network effects, or trust.",
        "strong": (
            ("proprietary data", r"\bproprietary data\b|\bfirst-party data\b"),
            ("system of record", r"\bsystems? of record\b"),
            ("integrations", r"\bdeep integrations?\b|\bintegrations?\b"),
            ("network effects", r"\bnetwork effects?\b"),
            ("trust", r"\btrusted\b|\btrust layer\b|\bcompliance\b"),
            ("moat", r"\bmoat\b|\bdefensible\b|\bdifferentiation\b"),
        ),
    },
)
