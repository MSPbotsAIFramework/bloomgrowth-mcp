# bloomgrowth-mcp

**Bloom Growth** MCP server — exposes the Bloom Growth REST API (EOS/Traction-style meetings, rocks, scorecards, to-dos, and org-chart management) as MCP tools.

> **Naming note:** app.mspbots.ai calls this integration **"Bloom Growth"** (`sys_integration.subject_code = BLOOMGROWTH`). MSPbots' own integration only calls one endpoint (`GET /api/v1/scorecard/user/mine`). Per a 2026-08-04 scope decision, this build was trimmed from an original full-API 123-tool build down to **10 tools** covering that endpoint's category (`scorecard`) plus `measurables` (the resource scorecards are a computed view over) — see **Tool List** below for the exact rationale.

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
# {"status": "ok", "service": "bloomgrowth-mcp", "transport": "http"}
```

No token is required for the health endpoint.

## 授权参数说明 (Authentication)

Every request to `/mcp` must include the following HTTP header:

| Header | 类型 | 是否必填 | 默认值 | 枚举值 | 字段描述 | Example |
|---|---|---|---|---|---|---|
| `X-BloomGrowth-Token` | string | 必填 | 无 | 无(自由文本) | OAuth2 bearer access token,由调用方(Agent Platform / 上游网关)通过 `POST https://app.bloomgrowth.com/Token`(form-urlencoded,`grant_type=password&userName=<email>&password=<password>`)预先换取,有效期约 2 周,过期后需重新换取。本服务从不接触 email/password,只转发已获取的 token。 | `X-BloomGrowth-Token: <access_token>` |

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

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_create_measurable` | 创建计分卡指标 | `name?`, `direction?`, `target?`, `unit_type?`, `accountable_user_id?` |
| `bloomgrowth_get_my_measurables` | 查我的 measurables | `include_origin?` |
| `bloomgrowth_get_user_measurables` | 查指定用户的 measurables | `user_id`, `include_origin?` |
| `bloomgrowth_update_measurable` | 更新指标定义 | `measurable_id`, `name?`, `direction?`, `target?`, `unit_type?`, `alt_target?` |
| `bloomgrowth_get_measurable` | 查指标详情 | `measurable_id`, `include_origin?` |
| `bloomgrowth_get_measurable_scores` | 查指标的每周得分 | `measurable_id`, `include_origin?` |
| `bloomgrowth_set_measurable_week_value` | 设置指标某周的分值 | `measurable_id`, `week_id`, `value?` |

### Scorecard (3)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_meeting_scorecard` | 查会议计分卡 | `meeting_id` |
| `bloomgrowth_get_my_scorecard` | 查我的计分卡 | 无（MSPbots 现有集成实际使用的唯一接口） |
| `bloomgrowth_get_user_scorecard` | 查指定用户的计分卡 | `user_id` |

## 测试示例 (Test Example)

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
