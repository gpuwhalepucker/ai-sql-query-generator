# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Do **not** open a public issue for security bugs. Email `security@aisqlgen.dev` with:

- A description of the issue
- Steps to reproduce
- Affected version and dialect backend
- Whether the issue allows SQL injection, credential leakage, or arbitrary file read

We aim to acknowledge within 72 hours and ship a patch within 14 days for confirmed issues.

## Threat model notes

`ai-sql-query-generator` executes **read-only** SQL by default. The `--allow-write` flag is opt-in and off in every shipped config. Generated SQL is passed through `aisqlgen/core/guard.py` before execution, which rejects stacked statements, `ATTACH`, `COPY ... FROM PROGRAM`, and dialect-specific file-read primitives. If you find a bypass, that's a security bug — report it.

Connection strings are stored via Windows DPAPI when `--store-credentials` is used. They are never written to logs. If you find a code path that logs a raw DSN, that's a bug.