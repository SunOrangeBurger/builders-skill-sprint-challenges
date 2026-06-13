"""
Cerberus - A three-headed static analysis tool for code security, logic, and architecture.

Named after the mythological guardian of the underworld, Cerberus watches over
your codebase through three lenses:

    Head 1 - Security Sentinel
        Detects vulnerabilities, exposed secrets, and injection flaws.

    Head 2 - Logic Analyzer
        Identifies logical errors, anti-patterns, and flawed assumptions.

    Head 3 - Architecture Auditor
        Reviews system design, AWS best practices, and scalability concerns.

Powered by:
    - AWS Documentation MCP for real-time best practices
    - Pattern-based static analysis across all three heads
    - Conversational memory for session continuity
    - Amazon Nova Pro for AI-assisted reasoning
"""

import os
import re
from pathlib import Path

from strands import Agent, tool
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client
from strands_tools import mem0_memory

os.environ["BYPASS_TOOL_CONSENT"] = "true"

MODEL = "us.amazon.nova-pro-v1:0"
SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php"}


# ---------------------------------------------------------------------------
# Head 1: Security patterns
# ---------------------------------------------------------------------------

SECURITY_PATTERNS = {
    "hardcoded_secrets": [
        (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'(?i)(api[_-]?key|apikey)\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'(?i)(secret|token)\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded secret or token"),
        (r'(?i)aws_access_key_id\s*=\s*["\']AKIA[0-9A-Z]{16}["\']', "Exposed AWS access key"),
        (r'(?i)(private[_-]?key|privatekey)\s*=', "Private key embedded in source"),
        (r'mongodb://.+:.+@', "Database credentials in connection string"),
    ],
    "sql_injection": [
        (r'execute\s*\(\s*["\'].*%s.*["\']', "SQL injection via string formatting"),
        (r'cursor\.execute\s*\([^?]*\+', "SQL injection via string concatenation"),
        (r'SELECT.*FROM.*WHERE.*\+', "String concatenation in SQL WHERE clause"),
        (r'\.raw\s*\(.*\+', "Raw SQL with concatenated input"),
    ],
    "command_injection": [
        (r'os\.system\s*\(.*\+', "Command injection risk via os.system"),
        (r'subprocess\.(call|run|Popen)\s*\(.*shell\s*=\s*True', "Shell injection risk with shell=True"),
        (r'eval\s*\(', "Arbitrary code execution via eval()"),
        (r'exec\s*\(', "Arbitrary code execution via exec()"),
        (r'__import__\s*\(', "Dynamic import with __import__"),
    ],
    "insecure_deserialization": [
        (r'pickle\.loads?\s*\(', "Insecure deserialization via pickle"),
        (r'yaml\.load\s*\((?!.*Loader=)', "Unsafe YAML load — use yaml.safe_load()"),
        (r'marshal\.loads?\s*\(', "Insecure deserialization via marshal"),
    ],
    "weak_crypto": [
        (r'hashlib\.md5\s*\(', "MD5 is cryptographically broken"),
        (r'hashlib\.sha1\s*\(', "SHA-1 is cryptographically weak"),
        (r'random\.random\s*\(', "random module is not cryptographically secure — use secrets"),
        (r'DES|RC4|Blowfish', "Deprecated or weak cipher algorithm"),
    ],
    "path_traversal": [
        (r'open\s*\(.*\+.*["\']\.\.', "Potential path traversal via open()"),
        (r'os\.path\.join\s*\(.*user', "User-controlled path component — validate for traversal"),
        (r'send_file\s*\(.*\+', "Potential path traversal in file serving"),
    ],
    "authentication_issues": [
        (r'jwt\.decode\s*\(.*verify\s*=\s*False', "JWT signature verification disabled"),
        (r'ssl\._create_unverified_context', "SSL certificate verification disabled"),
        (r'requests\.(get|post).*verify\s*=\s*False', "TLS certificate verification disabled"),
    ],
    "xxe_vulnerability": [
        (r'XMLParser\s*\(.*resolve_entities\s*=\s*True', "XXE vulnerability in XML parser"),
        (r'parse\s*\(.*\.xml', "Unguarded XML parse — potential XXE"),
    ],
}

# ---------------------------------------------------------------------------
# Head 2: Logic patterns
# ---------------------------------------------------------------------------

LOGIC_PATTERNS = {
    "race_conditions": [
        (r'if\s+os\.path\.exists.*:\s*\n\s*open', "TOCTOU race condition — check then open"),
        (r'if\s+not\s+.*\.exists\(\):.*\n\s*.*\.create', "Race condition in existence check before create"),
    ],
    "null_pointer_risks": [
        (r'\.get\s*\([^)]+\)(?!\s*or\s)(?!\s*\|\|)', "No None check after .get() call"),
        (r'\[.*\](?!\s+if\s)', "Unguarded dictionary access"),
    ],
    "infinite_loops": [
        (r'while\s+True:(?!.*break)(?!.*return)', "while True loop with no exit path"),
        (r'for.*in.*:(?!.*break)(?!.*return).*while.*:', "Nested loop with no break or return"),
    ],
    "resource_leaks": [
        (r'open\s*\([^)]+\)(?!.*with\s)', "File opened outside a context manager"),
        (r'socket\s*\((?!.*with\s)', "Socket created without guaranteed cleanup"),
        (r'requests\.(get|post)\s*\(.*stream\s*=\s*True(?!.*close)', "Streaming response never closed"),
    ],
    "logic_errors": [
        (r'if\s+.*==\s*True:', "Redundant comparison to True"),
        (r'if\s+len\s*\(.*\)\s*>\s*0:', "Use 'if container:' instead of len() > 0"),
        (r'if\s+.*\s+is\s+(True|False):', "Use == not 'is' for boolean comparison"),
        (r'except\s*:', "Bare except clause — catches SystemExit and KeyboardInterrupt"),
    ],
    "type_confusion": [
        (r'if\s+type\s*\(.*\)\s*==', "Use isinstance() instead of type() =="),
        (r'\+.*str\(', "Implicit type coercion in concatenation"),
    ],
    "algorithmic_inefficiency": [
        (r'for.*in.*:\s*if.*in\s+list', "O(n^2) membership test — use a set"),
        (r'\.append\(.*\).*sort\(\)', "Sort after every append is O(n^2 log n) — sort once"),
        (r'for.*range\(len\(', "Use enumerate() instead of range(len())"),
    ],
    "technical_debt": [
        (r'assert\s+(?!.*,\s*["\'])', "Assert without an explanatory message"),
        (r'TODO|FIXME|HACK|XXX', "Unresolved technical debt marker"),
        (r'pass\s*#.*implement', "Unimplemented stub left in place"),
    ],
}

# ---------------------------------------------------------------------------
# Head 3: Architecture patterns
# ---------------------------------------------------------------------------

ARCHITECTURE_PATTERNS = {
    "aws_anti_patterns": [
        (r'time\.sleep\s*\(\s*[0-9]+\s*\)', "Polling with sleep — prefer EventBridge or SQS"),
        (r'while.*requests\.get.*status', "Polling an API — prefer webhooks or event-driven design"),
        (r'for.*in.*:\s*.*boto3\.client', "boto3 client instantiated inside a loop"),
        (r'boto3\.client\(.*region.*=.*us-east-1', "Hardcoded AWS region — use config or environment"),
    ],
    "scalability_issues": [
        (r'global\s+\w+\s*=', "Global mutable state — not safe across threads or workers"),
        (r'cache\s*=\s*\{\}', "In-process dict cache — use ElastiCache for distributed caching"),
        (r'sqlite3\.connect', "SQLite is not suitable for production scale — use RDS or Aurora"),
    ],
    "coupling_issues": [
        (r'from\s+\.\.\..+import', "Deep relative import — signals tight coupling"),
        (r'import\s+\*', "Wildcard import obscures dependencies"),
        (r'hardcode.*url\s*=\s*["\']http', "Hardcoded URL — use environment config"),
    ],
    "error_handling": [
        (r'except.*pass', "Exception silently swallowed"),
        (r'except.*print\(', "Exception printed rather than logged"),
        (r'raise\s+Exception\(', "Generic Exception raised — use a more specific type"),
    ],
    "observability_gaps": [
        (r'def\s+\w+\(.*\):(?!.*log)(?!.*print)', "Function body has no logging"),
        (r'try:(?!.*finally)', "Try block without a finally for guaranteed cleanup"),
    ],
}

# Severity by category
SECURITY_CRITICAL = {"hardcoded_secrets", "sql_injection", "command_injection", "authentication_issues"}
LOGIC_HIGH = {"race_conditions", "infinite_loops", "resource_leaks"}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def cerberus_scan(file_path: str, scan_type: str = "all") -> str:
    """
    Run a Cerberus analysis on a single source file.

    Applies up to three analysis passes depending on scan_type:
        all          - Security, Logic, and Architecture (default)
        security     - Head 1 only
        logic        - Head 2 only
        architecture - Head 3 only

    Args:
        file_path: Path to the source file.
        scan_type: Which heads to activate. One of: all, security, logic, architecture.

    Returns:
        A structured report of all findings, or a clean bill of health.
    """
    try:
        path = Path(file_path)

        if not path.exists():
            return f"Error: '{file_path}' does not exist."

        if path.suffix not in SUPPORTED_EXTENSIONS:
            return (
                f"Warning: '{path.suffix}' files are not fully supported. "
                f"Best results with: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        code = path.read_text(encoding="utf-8")
        lines = code.splitlines()

        findings = {"security": [], "logic": [], "architecture": []}

        def _scan(lines, patterns, head_label, severity_fn, bucket):
            for line_num, line in enumerate(lines, 1):
                for category, category_patterns in patterns.items():
                    for pattern, description in category_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            findings[bucket].append({
                                "line": line_num,
                                "severity": severity_fn(category),
                                "head": head_label,
                                "category": category.replace("_", " ").title(),
                                "description": description,
                                "code": line.strip()[:120],
                            })

        if scan_type in ("all", "security"):
            _scan(
                lines,
                SECURITY_PATTERNS,
                "Head 1 - Security",
                lambda cat: "CRITICAL" if cat in SECURITY_CRITICAL else "HIGH",
                "security",
            )

        if scan_type in ("all", "logic"):
            _scan(
                lines,
                LOGIC_PATTERNS,
                "Head 2 - Logic",
                lambda cat: "HIGH" if cat in LOGIC_HIGH else "MEDIUM",
                "logic",
            )

        if scan_type in ("all", "architecture"):
            _scan(
                lines,
                ARCHITECTURE_PATTERNS,
                "Head 3 - Architecture",
                lambda _: "MEDIUM",
                "architecture",
            )

        total = sum(len(v) for v in findings.values())

        if total == 0:
            return (
                f"Clean: '{file_path}' passed all active analysis heads.\n"
                f"{len(lines)} lines scanned."
            )

        # Build report
        sep = "-" * 72
        report_lines = [
            "CERBERUS - STATIC ANALYSIS REPORT",
            "=" * 72,
            f"File      : {file_path}",
            f"Lines     : {len(lines)}",
            f"Scan type : {scan_type}",
            f"Findings  : {total}",
            "=" * 72,
        ]

        for bucket, bucket_findings in findings.items():
            if not bucket_findings:
                continue
            report_lines.append(f"\n{sep}")
            report_lines.append(f"{bucket.upper()} ({len(bucket_findings)} finding(s))")
            report_lines.append(sep)
            for i, f in enumerate(bucket_findings, 1):
                report_lines.append(
                    f"\n  [{i}] {f['severity']} | Line {f['line']} | {f['head']}"
                )
                report_lines.append(f"      Category : {f['category']}")
                report_lines.append(f"      Issue    : {f['description']}")
                report_lines.append(f"      Code     : {f['code']}")

        report_lines.append(f"\n{'=' * 72}")
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("=" * 72)
        if findings["security"]:
            report_lines.append(
                f"  [!] Resolve {len(findings['security'])} security issue(s) before next deployment."
            )
        if findings["logic"]:
            report_lines.append(
                f"  [*] Address {len(findings['logic'])} logic issue(s) to reduce bug risk."
            )
        if findings["architecture"]:
            report_lines.append(
                f"  [~] Consider {len(findings['architecture'])} architectural improvement(s)."
            )
        report_lines.append(
            "\n  Use cerberus_best_practices('<topic>') for remediation guidance."
        )

        return "\n".join(report_lines)

    except OSError as e:
        return f"Error reading '{file_path}': {e}"
    except Exception as e:
        return f"Unexpected error during scan: {e}"


@tool
def cerberus_directory_scan(
    directory_path: str, scan_type: str = "all", max_files: int = 20
) -> str:
    """
    Run Cerberus analysis across all supported source files in a directory.

    Args:
        directory_path: Root directory to scan (searched recursively).
        scan_type: Which heads to activate. One of: all, security, logic, architecture.
        max_files: Maximum number of files to process (default 20).

    Returns:
        A summary report with per-file issue counts and aggregate totals.
    """
    try:
        path = Path(directory_path)

        if not path.exists():
            return f"Error: '{directory_path}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."

        code_files = []
        for ext in SUPPORTED_EXTENSIONS:
            code_files.extend(path.rglob(f"*{ext}"))
        code_files = sorted(code_files)[:max_files]

        if not code_files:
            return f"No supported source files found in '{directory_path}'."

        aggregate = {"security": 0, "logic": 0, "architecture": 0}
        file_summaries = []   # list of (filename, security, logic, architecture, has_critical)
        sep = "-" * 72

        for code_file in code_files:
            result = cerberus_scan(str(code_file), scan_type)
            file_security = file_logic = file_arch = 0
            has_critical = False

            for line in result.splitlines():
                m = re.search(r"SECURITY \((\d+)", line)
                if m:
                    file_security = int(m.group(1))
                m = re.search(r"LOGIC \((\d+)", line)
                if m:
                    file_logic = int(m.group(1))
                m = re.search(r"ARCHITECTURE \((\d+)", line)
                if m:
                    file_arch = int(m.group(1))
                if "CRITICAL" in line:
                    has_critical = True

            aggregate["security"] += file_security
            aggregate["logic"] += file_logic
            aggregate["architecture"] += file_arch

            total_for_file = file_security + file_logic + file_arch
            if total_for_file > 0:
                file_summaries.append(
                    (code_file.name, file_security, file_logic, file_arch, has_critical)
                )

        total_all = sum(aggregate.values())

        report_lines = [
            "CERBERUS - DIRECTORY SCAN REPORT",
            "=" * 72,
            f"Directory : {directory_path}",
            f"Files     : {len(code_files)} scanned",
            f"Scan type : {scan_type}",
            f"Findings  : {total_all}",
            "=" * 72,
        ]

        if total_all == 0:
            report_lines.append("\nAll files passed Cerberus inspection.")
            return "\n".join(report_lines)

        report_lines += [
            "",
            "AGGREGATE TOTALS",
            sep,
            f"  Security     : {aggregate['security']}",
            f"  Logic        : {aggregate['logic']}",
            f"  Architecture : {aggregate['architecture']}",
            f"  Total        : {total_all}",
        ]

        # Sort by total descending
        file_summaries.sort(key=lambda r: r[1] + r[2] + r[3], reverse=True)

        critical_files = [r[0] for r in file_summaries if r[4]]
        if critical_files:
            report_lines.append("")
            report_lines.append("FILES WITH CRITICAL SECURITY FINDINGS")
            report_lines.append(sep)
            for name in critical_files:
                report_lines.append(f"  {name}")

        report_lines.append("")
        report_lines.append("PER-FILE BREAKDOWN  (security / logic / architecture)")
        report_lines.append(sep)
        for name, sec, log, arch, _ in file_summaries:
            report_lines.append(f"  {name:<40}  {sec:>3}  {log:>3}  {arch:>3}")

        report_lines += [
            "",
            "Run cerberus_scan('<file>') for the full report on any file.",
            "Run cerberus_best_practices('<topic>') for remediation guidance.",
        ]

        return "\n".join(report_lines)

    except Exception as e:
        return f"Unexpected error during directory scan: {e}"


@tool
def cerberus_best_practices(topic: str) -> str:
    """
    Return detailed remediation guidance for a specific vulnerability or anti-pattern.

    Supported topics: sql_injection, hardcoded_secrets, race_conditions,
    resource_leaks, aws_lambda_best_practices, algorithmic_inefficiency,
    error_handling, coupling_issues.

    Args:
        topic: The topic to look up (underscores or spaces both accepted).

    Returns:
        Step-by-step guidance with secure code examples.
    """
    guides = {
        "sql_injection": """
HEAD 1 - SQL INJECTION PREVENTION
==================================

Root cause: Untrusted input is interpolated directly into SQL strings.

1. Parameterized queries (the baseline fix)

    # Wrong
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

    # Right
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    cursor.execute("SELECT * FROM users WHERE id = ?",  (user_id,))  # sqlite3

2. ORM query builders

    # Django
    User.objects.filter(username=user_input)

    # SQLAlchemy
    session.query(User).filter(User.name == name)

3. Input validation (defense in depth)
    - Whitelist expected characters; reject everything else.
    - Validate type before the query: int(user_id), is_valid_email(email).

4. Least-privilege database accounts
    - Application accounts should only have SELECT/INSERT/UPDATE on the
      tables they need. Never connect as a superuser.

AWS note: Use RDS with IAM database authentication and store the
connection string in Secrets Manager, not in environment variables or code.
""",
        "hardcoded_secrets": """
HEAD 1 - SECRETS MANAGEMENT
=============================

Root cause: Credentials committed to source control are permanently exposed,
even after deletion, because version history preserves them.

1. Environment variables (minimum viable fix)

    password = os.environ["DB_PASSWORD"]   # raises KeyError if missing — good
    api_key  = os.getenv("API_KEY")        # returns None — check the value

2. AWS Secrets Manager (preferred for production)

    import boto3, json
    client = boto3.client("secretsmanager")
    raw    = client.get_secret_value(SecretId="prod/db/credentials")
    secret = json.loads(raw["SecretString"])
    DB_PASS = secret["password"]

3. AWS Systems Manager Parameter Store (suitable for non-secret config too)

    ssm   = boto3.client("ssm")
    param = ssm.get_parameter(Name="/prod/api/key", WithDecryption=True)
    key   = param["Parameter"]["Value"]

4. IAM roles instead of long-term credentials
    Lambda functions, EC2 instances, and ECS tasks can assume an IAM role
    that grants S3/DynamoDB/etc. access — no access key needed at all.

Never commit: .env files, credentials.json, any file containing a key or password.
Add a pre-commit hook (e.g. detect-secrets) to catch this before it reaches Git.
""",
        "race_conditions": """
HEAD 2 - RACE CONDITION PREVENTION
=====================================

Root cause: TOCTOU (Time-of-Check, Time-of-Use). The state checked in a
condition can change before the subsequent action executes.

Vulnerable pattern:
    if os.path.exists(path):    # Check
        with open(path) as f:   # Use — file may be gone or replaced by now
            data = f.read()

Fix 1 — ask forgiveness, not permission:
    try:
        with open(path) as f:
            data = f.read()
    except FileNotFoundError:
        handle_missing()

Fix 2 — file locking for writers:
    import fcntl
    with open(path, "r") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        data = f.read()

Fix 3 — database row locking:
    SELECT ... FOR UPDATE            -- holds a row lock until transaction ends
    -- or use SERIALIZABLE isolation for critical sections

Fix 4 — DynamoDB conditional writes:
    table.put_item(
        Item=item,
        ConditionExpression="attribute_not_exists(pk)"
    )
    # Raises ConditionalCheckFailedException on conflict — handle it.
""",
        "resource_leaks": """
HEAD 2 - RESOURCE LEAK PREVENTION
====================================

Root cause: Resources acquired without a guaranteed release path will be
held until the process exits or the OS reclaims them — or never.

Vulnerable pattern:
    f = open("data.txt")       # exception here or below = leak
    data = f.read()
    f.close()                  # may never execute

Fix 1 — context managers (preferred):
    with open("data.txt") as f:
        data = f.read()         # f is closed on any exit, including exceptions

    with psycopg2.connect(...) as conn:
        with conn.cursor() as cur:
            cur.execute(query)

Fix 2 — try/finally for objects that don't support "with":
    resource = acquire()
    try:
        use(resource)
    finally:
        resource.release()

Fix 3 — connection pooling for databases:
    from sqlalchemy.pool import QueuePool
    # or use RDS Proxy, which handles connection pooling outside the application

AWS note: Lambda execution environments are reused across invocations.
A connection leaked in one invocation may resurface (or fail) in the next.
Always close connections inside the handler, or use a pooling library.
""",
        "aws_lambda_best_practices": """
HEAD 3 - AWS LAMBDA ARCHITECTURE
==================================

1. Initialize clients outside the handler (reuse across warm invocations)

    # Wrong — creates a new client on every call
    def handler(event, ctx):
        s3 = boto3.client("s3")

    # Right — client is reused while the execution environment is warm
    s3 = boto3.client("s3")
    def handler(event, ctx):
        s3.get_object(Bucket="...", Key="...")

2. Event-driven over polling

    # Wrong — burns execution time and money
    while not task_done():
        time.sleep(5)

    # Right — use Step Functions, SQS, or EventBridge to drive progress

3. Keep deployment packages small
    - Move heavy dependencies into a Lambda Layer.
    - Smaller packages mean faster cold starts.

4. Fan-out for parallel work

    # Wrong — sequential
    for item in items:
        process(item)

    # Right — write to SQS; separate Lambda instances process in parallel

5. Defensive event access

    # Wrong
    record = event["Records"][0]

    # Right
    records = event.get("Records", [])
    if not records:
        logger.warning("Invoked with no Records")
        return {"statusCode": 400, "body": "No records"}
    record = records[0]

6. Configuration
    - Store all config in environment variables or Parameter Store.
    - Never hardcode region, account IDs, or resource names.
    - Enable AWS X-Ray for distributed tracing.
    - Set a Dead Letter Queue on async invocations.
""",
        "algorithmic_inefficiency": """
HEAD 2 - ALGORITHMIC EFFICIENCY
==================================

1. O(n^2) membership test

    # Wrong — list lookup is O(n), done n times
    for item in items:
        if item in my_list:
            process(item)

    # Right — set lookup is O(1)
    my_set = set(my_list)
    for item in items:
        if item in my_set:
            process(item)

2. Sort after every append

    # Wrong — O(n^2 log n) overall
    for item in items:
        my_list.append(item)
        my_list.sort()

    # Right — O(n log n) overall
    my_list.extend(items)
    my_list.sort()

    # Right for streaming top-K — O(n log k)
    import heapq
    heap = []
    for item in items:
        heapq.heappush(heap, item)

3. range(len()) antipattern

    # Wrong
    for i in range(len(items)):
        print(i, items[i])

    # Right
    for i, item in enumerate(items):
        print(i, item)

4. String concatenation in a loop

    # Wrong — creates a new string object each iteration: O(n^2) memory
    result = ""
    for s in strings:
        result += s

    # Right — O(n)
    result = "".join(strings)

Lambda cost is proportional to execution time, so algorithmic choices
have a direct dollar impact at scale.
""",
        "error_handling": """
HEAD 3 - ERROR HANDLING PATTERNS
===================================

1. Don't swallow exceptions silently

    # Wrong — error disappears; debugging is impossible
    try:
        critical_operation()
    except Exception:
        pass

    # Right
    try:
        critical_operation()
    except SomeSpecificError as e:
        logger.error("Operation failed: %s", e, exc_info=True)
        raise   # or handle and return an appropriate response

2. Avoid bare except

    # Wrong — catches SystemExit, KeyboardInterrupt, etc.
    except:

    # Right — catch only what you can handle
    except (ValueError, KeyError) as e:

3. Use specific exception types

    # Wrong
    raise Exception("something broke")

    # Right
    raise ValueError(f"Expected positive integer, got: {value!r}")
    raise FileNotFoundError(f"Config not found: {config_path}")

4. Use a logger, not print

    # Wrong
    except Exception as e:
        print(e)

    # Right
    import logging
    logger = logging.getLogger(__name__)
    logger.exception("Operation failed", extra={"user_id": user_id})

AWS best practices:
    - Emit structured JSON logs so CloudWatch Insights can query them.
    - Create a CloudWatch Alarm on error rate metrics.
    - Attach a Dead Letter Queue to Lambda functions invoked asynchronously.
    - Use AWS X-Ray to trace failures across service boundaries.
""",
        "coupling_issues": """
HEAD 3 - LOOSE COUPLING PATTERNS
===================================

1. Deep relative imports signal tight coupling

    # Fragile — breaks if you move any module
    from ...parent.grandparent.service import do_thing

    # Better — inject dependencies rather than importing deeply
    class MyService:
        def __init__(self, dependency):
            self.dep = dependency

2. Wildcard imports hide dependencies

    # Wrong — what exactly did we import?
    from module import *

    # Right — explicit and searchable
    from module import SpecificClass, helper_function

3. Hardcoded URLs block environment parity

    # Wrong — can't test locally without modifying code
    API_URL = "https://prod.api.example.com"

    # Right
    API_URL = os.environ.get("API_URL", "http://localhost:8000")

4. God classes — split by responsibility

    # Wrong — one class does everything
    class Application:
        def handle_http(self): ...
        def query_db(self): ...
        def send_email(self): ...
        def charge_card(self): ...

    # Right — one class, one concern
    class HttpHandler: ...
    class DatabaseService: ...
    class EmailService: ...
    class PaymentProcessor: ...

AWS microservices pattern:
    - Each Lambda has one responsibility.
    - Services communicate via SQS, SNS, or EventBridge (decoupled).
    - Use API Gateway as the external boundary.
    - Store shared config in Parameter Store or Secrets Manager.
""",
    }

    key = topic.lower().replace(" ", "_").replace("-", "_")
    for guide_key, guide_text in guides.items():
        if key in guide_key or guide_key in key:
            return guide_text.strip()

    available = "\n  ".join(sorted(guides.keys()))
    return (
        f"No guide found for '{topic}'.\n\n"
        f"Available topics:\n  {available}\n\n"
        f"Usage: cerberus_best_practices('sql_injection')\n"
        f"       cerberus_best_practices('aws lambda best practices')"
    )


# ---------------------------------------------------------------------------
# Agent setup
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are Cerberus, a static analysis assistant for code security, logic correctness,
and architectural quality.

You analyze code through three lenses:

    Head 1 - Security
        SQL injection, command injection, hardcoded secrets, weak cryptography,
        path traversal, insecure deserialization, authentication bypasses.

    Head 2 - Logic
        Race conditions, resource leaks, infinite loops, null pointer risks,
        algorithmic inefficiencies, type confusion, unhandled assumptions.

    Head 3 - Architecture
        AWS anti-patterns, scalability issues, tight coupling, silent error
        handling, observability gaps.

Tools available to you:
    cerberus_scan('<file>')                   - Analyze a single file.
    cerberus_directory_scan('<dir>')          - Analyze all files in a directory.
    cerberus_best_practices('<topic>')        - Return remediation guidance.
    mem0_memory(...)                          - Persist findings across sessions.
    AWS Documentation MCP tools              - Fetch current AWS best practices.

When you report a finding, explain the root cause — not just what the pattern
matched, but why it represents a real risk and what false assumption it encodes.
Prioritize by severity: CRITICAL before HIGH before MEDIUM.

Where relevant, reference the AWS Well-Architected Framework and provide
corrected code examples, not just warnings.
""".strip()


def _init_mcp_client():
    """Attempt to connect to the AWS Documentation MCP server and return its tools."""
    client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command="awslabs.aws-documentation-mcp-server")
        )
    )
    try:
        with client:
            tools = client.list_tools_sync()
        return client, tools
    except Exception as exc:
        print(f"Warning: could not connect to AWS Docs MCP server: {exc}")
        print("Continuing without live AWS documentation access.")
        return None, []


def build_agent():
    """Construct and return the Cerberus agent."""
    print("Initializing Cerberus...")
    print("Connecting to AWS Documentation MCP server...")

    _, mcp_tools = _init_mcp_client()

    if mcp_tools:
        print(
            f"AWS MCP connected — {len(mcp_tools)} tool(s) available: "
            + ", ".join(t.name for t in mcp_tools)
        )
    else:
        print("Running with built-in analysis only.")

    all_tools = [
        cerberus_scan,
        cerberus_directory_scan,
        cerberus_best_practices,
        mem0_memory,
    ] + mcp_tools

    print(f"Total tools loaded: {len(all_tools)}")

    return Agent(model=MODEL, tools=all_tools, system_prompt=SYSTEM_PROMPT)


HELP_TEXT = """
Cerberus - commands
-------------------
  scan <file>                     Full analysis (security + logic + architecture)
  scan <file> security            Security head only
  scan <file> logic               Logic head only
  scan <file> architecture        Architecture head only
  scan directory <path>           Scan an entire directory
  how to fix <topic>              Remediation guidance
  search aws docs for <query>     Query live AWS documentation
  help                            Show this message
  quit                            Exit
"""


def main():
    agent = build_agent()

    print("\n" + "=" * 72)
    print("Cerberus - Code Security, Logic, and Architecture Analyzer")
    print("=" * 72)
    print(HELP_TEXT)

    while True:
        try:
            user_input = input("cerberus> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if user_input.lower() == "help":
            print(HELP_TEXT)
            continue

        try:
            response = agent(user_input)
            print(f"\n{response}\n")
        except Exception as exc:
            print(f"\nError: {exc}\nTry rephrasing your request.\n")


if __name__ == "__main__":
    main()