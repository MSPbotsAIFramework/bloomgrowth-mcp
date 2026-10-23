# bloomgrowth-mcp

**Bloom Growth** MCP server — exposes the Bloom Growth REST API (EOS/Traction-style meetings, rocks, scorecards, to-dos, and org-chart management) as MCP tools.

> **Naming note:** app.mspbots.ai calls this integration **"Bloom Growth"** (`sys_integration.subject_code = BLOOMGROWTH`). MSPbots' own integration only calls one endpoint (`GET /api/v1/scorecard/user/mine`). Per a 2026-08-04 scope decision, this build was trimmed from an original full-API 123-tool build down to **10 tools** covering that endpoint's category (`scorecard`) plus `measurables` (the resource scorecards are a computed view over) — see **Tool List** below for the exact rationale.

<div align="center">

## MSPbots Connector

**The MCP Gateway built for MSPs: visible, controlled, and your data stays where it belongs.**

[**Get started at connect.mspbots.ai →**](https://connect.mspbots.ai)

</div>

---

MSPbots Connector gives your AI clients one MCP URL to reach your entire MSP stack (RMM, PSA, documentation, security, finance), and gives you control over who can call which tool and a record of everything that was called.

**Hosted service: [connect.mspbots.ai](https://connect.mspbots.ai)** · Free to use.

### Why Connector

![MSPbots Connector](https://stgoss.mspbots.ai/files/mcp/mspbots-mcp.png)

| | |
|---|---|
| **Visible** | Every tool call is logged: who, which vendor, when. Usage dashboard, CSV export, SIEM streaming. |
| **Controlled** | Role-based, per-tool allowlist. Deny by default. |
| **Protected** | Credentials encrypted per record. AI clients never see your vendor passwords or tokens. |
| **MSP-native** | Built for the MSP stack only: RMM, PSA, documentation, security, finance. |

### Quick start

1. **Sign up** at [connect.mspbots.ai](https://connect.mspbots.ai).
2. **Connect your vendors.** Pick from 150+ connectors and authorize each one on the vendor's own page, or bring your own API keys. No extra vendor accounts needed.
3. **Set access.** Create roles and decide which tools each role may call. Nothing is allowed until you allow it.
4. **Add your MCP URL to your AI client.** Copy the URL from your Connector dashboard into Claude, ChatGPT, Cursor, VS Code, Gemini, Codex, or any MCP-capable client.
5. **Ask your AI to do real work**, and watch every call appear in the audit log.

### Features

**Unified gateway**
- One MCP URL for all your AI clients
- 150+ connectors across the MSP stack
- Custom MCP servers supported, free
- Authorization happens on each vendor's own page; the AI never sees passwords or tokens
- Bring your own credentials: use the vendor API keys you already have
- Multiple accounts per app; connect once, reuse across AI clients
- Tool search: finds the right action for the task
- One sign-in; vendor credentials are injected behind the scenes and OAuth tokens refresh automatically

**Visibility**
- Audit log for every tool call (who, which vendor, when)
- Usage dashboard: call volume, top vendors, error rate, per-user activity
- Export audit logs to CSV, or stream to Loki, Graylog, or LogScale (SIEM)
- Optional recording of tool arguments and result summaries (off by default, enabled per organization)

**Control**
- Per-role, per-tool allowlist, deny by default
- owner / admin / member roles
- SCIM provisioning with Entra ID, Okta, JumpCloud, and Google Workspace

**Security**
- Credentials encrypted one record at a time (AES-256-GCM, per-record key)
- AI clients authenticate with OAuth 2.1 + PKCE
- Vendor responses are scanned for prompt-injection patterns and returned as structured data. This is one layer of defense, not a guarantee against every attack.
- Static egress IP for customer firewall and API allowlisting

### Pricing

**Free.**

Links: [connect.mspbots.ai](https://connect.mspbots.ai) · [mspbots.ai](https://mspbots.ai)

---

## Overview

This server implements the [Model Context Protocol](https://modelcontextprotocol.io/) (Streamable HTTP/SSE transport) and wraps the [Bloom Growth REST API v1](https://dev-api.bloomgrowth.com/swagger/index.html) — **10 tools** across 2 files / 2 API tag categories (`scorecard`, `measurables`), including write operations (create/update). It follows the MSPbots **Vendor MCP Service SOP**: stateless, no stored credentials, per-request header authentication.

The underlying API authenticates via **OAuth2 Resource-Owner-Password-Credentials grant**: `POST https://app.bloomgrowth.com/Token` with form-urlencoded body `grant_type=password&userName=<email>&password=<password>`, returning a bearer access token valid for ~2 weeks. This server does not perform that token exchange itself — it receives an already-obtained bearer access token per request; the caller (Agent Platform / upstream gateway) obtains and refreshes the token from the account's email/password, and only the resulting token reaches this server (same pattern as bizratings-mcp, connectwise-asio-mcp, and acronis-mcp in this MCP fleet).

## Quick Start

### Docker (recommended)

```bash
docker compose up --build
```

The server starts on `http://localhost:8080`.

### Local (uv)

```bash
uv sync
python -m bloomgrowth_mcp
```

## Health Check

```bash
curl http://localhost:8080/health
# {"status": "ok"}
```

No token is required for the health endpoint.

## Authentication

Every request to `/mcp` must include the following HTTP header:

| Header | Type | Required | Default | Allowed values | Description | Example |
|---|---|---|---|---|---|---|
| `X-BloomGrowth-Token` | string | Required | None | None (free text) | OAuth2 bearer access token, obtained in advance by the caller (Agent Platform / upstream gateway) via `POST https://app.bloomgrowth.com/Token` (form-urlencoded, `grant_type=password&userName=<email>&password=<password>`); valid for about 2 weeks and must be re-obtained after it expires. This service never touches the email/password and only forwards the token already obtained. | `X-BloomGrowth-Token: <access_token>` |

Missing the header returns `401 Unauthorized`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MCP_HTTP_PORT` | `8080` | Listening port |
| `MCP_HTTP_HOST` | `0.0.0.0` | Listening host |
| `BLOOMGROWTH_BASE_URL` | `https://app.bloomgrowth.com` | Bloom Growth API base URL |

## MCP Endpoint

```
POST http://localhost:8080/mcp
```

Connect your MCP client with:
- Transport: `http` (Streamable HTTP / SSE)
- Headers: `X-BloomGrowth-Token: <access_token>` (required)

## Tool List

**10 tools**, trimmed down from an original 123-tool full-API build (2026-08-04). MSPbots' own integration only calls one endpoint (`GET /api/v1/scorecard/user/mine` -> `bloomgrowth_get_my_scorecard`); per the "actual usage + same-category core CRUD" scope decision, this build keeps the `scorecard` category plus `measurables` (the underlying resource a scorecard is a computed view over — Bloom Growth scorecards are tables of measurables and their weekly values, so there is no separate "scorecard" CRUD to speak of). Everything else from the original 123-tool build (L10 Meetings, Headlines, Issues, Milestones, Process, Rocks, Role, Seats, Teams, Todos, Users, Misc — 12 categories, ~113 tools) was removed as unused by MSPbots and out of scope for this server's purpose. If a removed category is needed later, the vendor's own OpenAPI/Swagger spec (linked below) still documents its exact operations and they can be re-added the same way the kept tools were generated.

### Measurables (7)

| Tool | Description | Parameters |
|---|---|---|
| `bloomgrowth_create_measurable` | Create a scorecard measurable | `name?`, `direction?`, `target?`, `unit_type?`, `accountable_user_id?` |
| `bloomgrowth_get_my_measurables` | Get my measurables | `include_origin?` |
| `bloomgrowth_get_user_measurables` | Get a given user's measurables | `user_id`, `include_origin?` |
| `bloomgrowth_update_measurable` | Update a measurable's definition | `measurable_id`, `name?`, `direction?`, `target?`, `unit_type?`, `alt_target?` |
| `bloomgrowth_get_measurable` | Get measurable details | `measurable_id`, `include_origin?` |
| `bloomgrowth_get_measurable_scores` | Get a measurable's weekly scores | `measurable_id`, `include_origin?` |
| `bloomgrowth_set_measurable_week_value` | Set a measurable's value for a given week | `measurable_id`, `week_id`, `value?` |

### Scorecard (3)

| Tool | Description | Parameters |
|---|---|---|
| `bloomgrowth_get_meeting_scorecard` | Get a meeting scorecard | `meeting_id` |
| `bloomgrowth_get_my_scorecard` | Get my scorecard | None (the only endpoint actually used by the existing MSPbots integration) |
| `bloomgrowth_get_user_scorecard` | Get a given user's scorecard | `user_id` |

## Test Example

Get the calling user's scorecard (matches MSPbots' existing integration usage):

```json
{
  "method": "tools/call",
  "params": { "name": "bloomgrowth_get_my_scorecard", "arguments": {} }
}
```

Equivalent `curl` against the running server (streamable HTTP MCP endpoint):

```bash
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "X-BloomGrowth-Token: <access_token>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": { "name": "bloomgrowth_get_my_scorecard", "arguments": {} }
  }'
```

A parameterized call:

```json
{
  "method": "tools/call",
  "params": {
    "name": "bloomgrowth_get_rock",
    "arguments": { "rock_id": 12345 }
  }
}
```

## API Reference

- Swagger UI: https://dev-api.bloomgrowth.com/swagger/index.html
- OpenAPI spec (v1): https://dev-api.bloomgrowth.com/swagger/v1/swagger.json
- Token endpoint guide: shown on the Swagger UI page ("Generating a Token")

## Known Gaps / Implementation Notes

- **Trimmed from 123 to 10 tools on 2026-08-04.** The original build covered
  the full public API across 18 tag categories per an earlier scope
  decision. A later scope decision cut this back to MSPbots' actually-used
  category (`scorecard`) plus `measurables` — see the Naming note and Tool
  List above for the exact rationale. If a removed category (L10 Meetings,
  Headlines, Issues, Milestones, Process, Rocks, Role, Seats, Teams, Todos,
  Users, Misc — ~113 tools total) is needed later, the vendor's OpenAPI/
  Swagger spec (linked below) still documents its exact operations and they
  can be re-added the same way the kept tools were generated.
- Not yet tested against a live Bloom Growth account — only protocol-level
  verification (health check, 401 on missing token, `tools/list` returning
  all 10 tools, and JSON-schema validation) has been done so far.
- `bloomgrowth_create_measurable` and `bloomgrowth_update_measurable` expose
  their request bodies as named optional parameters rather than a generic
  `body: dict`, since the Bloom Growth schemas are shallow (no deep
  nesting) — this differs from the `body`/`extra_params` dict pattern used
  in larger/deeper-nested vendor APIs elsewhere in this MCP fleet.
- Endpoints whose exact request/response shape wasn't fully described by the OpenAPI spec (a few return simple 200 with no documented body) are implemented to match the spec's declared parameters; verify against a real account before relying on edge-case behavior.
