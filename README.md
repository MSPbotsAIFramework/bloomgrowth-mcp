# bloomgrowth-mcp

**Bloom Growth** MCP server — exposes the Bloom Growth REST API (EOS/Traction-style meetings, rocks, scorecards, to-dos, and org-chart management) as MCP tools.

> **Naming note:** app.mspbots.ai calls this integration **"Bloom Growth"** (`sys_integration.subject_code = BLOOMGROWTH`). MSPbots' own integration only calls one endpoint (`GET /api/v1/scorecard/user/mine`); this MCP server covers the vendor's **full public API** (all 123 operations across 18 tag categories) per explicit scope decision, not just MSPbots' current usage.

## Overview

This server implements the [Model Context Protocol](https://modelcontextprotocol.io/) (Streamable HTTP/SSE transport) and wraps the [Bloom Growth REST API v1](https://dev-api.bloomgrowth.com/swagger/index.html) — **123 tools** across 14 files / 18 API tag categories, including write operations (create/update/delete). It follows the MSPbots **Vendor MCP Service SOP**: stateless, no stored credentials, per-request header authentication.

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

**123 tools** — full coverage of the official Bloom Growth v1 API (`https://dev-api.bloomgrowth.com/swagger/v1/swagger.json`).

### L10 Meetings (30)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_create_l10_meeting` | 创建 L10 会议 | `title`, `add_self?` |
| `bloomgrowth_get_l10_meetings` | 列出全部 L10 会议 | 无 |
| `bloomgrowth_update_l10_meeting` | 重命名会议 | `meeting_id`, `title` |
| `bloomgrowth_delete_l10_meeting` | 删除会议 | `meeting_id` |
| `bloomgrowth_get_l10_meeting` | 查会议详情 | `meeting_id` |
| `bloomgrowth_get_l10_attendees` | 查会议参会人 | `meeting_id` |
| `bloomgrowth_add_l10_attendee` | 添加参会人 | `meeting_id`, `user_id` |
| `bloomgrowth_create_l10_headline` | 在会议下创建 headline | `meeting_id`, `title`, `owner_id?`, `notes?` |
| `bloomgrowth_delete_l10_headline` | 删除会议 headline | `meeting_id`, `headline_id` |
| `bloomgrowth_create_l10_issue` | 在会议下创建 issue | `meeting_id`, `title`, `owner_id?`, `details?` |
| `bloomgrowth_delete_l10_issue` | 删除会议 issue | `meeting_id`, `issue_id` |
| `bloomgrowth_add_l10_measurable` | 挂载 measurable 到会议 | `meeting_id`, `measurable_id` |
| `bloomgrowth_remove_l10_measurable` | 移除会议上的 measurable | `meeting_id`, `measurable_id` |
| `bloomgrowth_create_l10_rock` | 在会议下创建 rock | `meeting_id`, `title`, `accountable_user_id?` |
| `bloomgrowth_get_l10_rocks` | 查会议下的 rock 列表 | `meeting_id`, `include_archive?`, `include_origin?` |
| `bloomgrowth_add_l10_rock` | 挂载已有 rock 到会议 | `meeting_id`, `rock_id` |
| `bloomgrowth_remove_l10_rock` | 从会议移除 rock | `meeting_id`, `rock_id` |
| `bloomgrowth_add_l10_rock_to_business_plan` | 把 rock 加入 business plan | `meeting_id`, `rock_id` |
| `bloomgrowth_remove_l10_rock_from_business_plan` | 把 rock 移出 business plan | `meeting_id`, `rock_id` |
| `bloomgrowth_create_l10_todo` | 在会议下创建 to-do | `meeting_id`, `title`, `details?`, `accountable_user_id?`, `due_date?` |
| `bloomgrowth_get_user_l10_meetings` | 查用户参加的会议列表 | `user_id` |
| `bloomgrowth_get_l10_headlines` | 查会议全部 headlines | `meeting_id`, `include_origin?` |
| `bloomgrowth_get_l10_issues` | 查会议全部 issues | `meeting_id`, `include_resolved?` |
| `bloomgrowth_get_l10_measurables` | 查会议全部 measurables | `meeting_id` |
| `bloomgrowth_get_l10_todos` | 查会议全部 to-dos | `meeting_id`, `include_closed?` |
| `bloomgrowth_get_l10_user_headlines` | 查会议内某用户的 headlines | `meeting_id`, `user_id`, `include_origin?` |
| `bloomgrowth_get_l10_user_issues` | 查会议内某用户的 issues | `meeting_id`, `user_id` |
| `bloomgrowth_get_l10_user_measurables` | 查会议内某用户的 measurables | `meeting_id`, `user_id` |
| `bloomgrowth_get_l10_user_rocks` | 查会议内某用户的 rocks | `meeting_id`, `user_id`, `include_origin?` |
| `bloomgrowth_get_l10_user_todos` | 查会议内某用户的 to-dos | `meeting_id`, `user_id` |

### Headlines (6)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_headline_notes` | 查 headline 备注文档 | `headline_id`, `show_controls?`, `read_only?` |
| `bloomgrowth_get_my_headlines` | 查我的 headlines | `include_origin?` |
| `bloomgrowth_get_user_headlines` | 查指定用户的 headlines | `user_id`, `include_origin?` |
| `bloomgrowth_get_headline` | 查 headline 详情 | `headline_id`, `include_origin?` |
| `bloomgrowth_update_headline` | 重命名 headline | `headline_id`, `title` |
| `bloomgrowth_delete_headline` | 删除 headline | `headline_id` |

### Issues (10)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_create_issue` | 创建 issue | `meeting_id`, `title`, `owner_id?`, `notes?` |
| `bloomgrowth_get_issue_notes` | 查 issue 备注文档 | `issue_id`, `show_controls?`, `read_only?` |
| `bloomgrowth_get_my_issues` | 查我的 issues | 无 |
| `bloomgrowth_get_user_issues` | 查指定用户的 issues | `user_id` |
| `bloomgrowth_update_issue` | 更新 issue | `issue_id`, `title?`, `owner_id?`, `compartment?`(ShortTerm/LongTerm) |
| `bloomgrowth_get_issue` | 查 issue 详情 | `issue_id` |
| `bloomgrowth_complete_issue` | 标记 issue 完成/未完成 | `issue_id`, `complete?` |
| `bloomgrowth_move_issue_from_vto` | 把 issue 移出 VTO | `issue_id` |
| `bloomgrowth_move_issue_to_meeting` | 把 issue 转移到另一个会议 | `issue_id`, `meeting_id` |
| `bloomgrowth_move_issue_to_vto` | 把 issue 移入 VTO | `issue_id` |

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

### Milestones (3)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_milestone` | 查 rock 里程碑详情 | `milestone_id` |
| `bloomgrowth_update_milestone` | 更新里程碑 | `milestone_id`, `title?`, `due_date?`, `status?`(NotDone/Done) |
| `bloomgrowth_delete_milestone` | 删除里程碑 | `milestone_id` |

### Process (7)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_process_execution_steps` | 查已启动流程实例的步骤 | `started_process_id` |
| `bloomgrowth_get_process_folders` | 列出流程文件夹 | 无 |
| `bloomgrowth_get_processes` | 列出流程(可按文件夹过滤) | `folder_id?` |
| `bloomgrowth_complete_process_step` | 标记流程步骤完成状态 | `step_id`, `completion` |
| `bloomgrowth_get_process` | 查流程定义详情 | `process_id` |
| `bloomgrowth_execute_process` | 启动一次流程执行 | `process_id` |
| `bloomgrowth_get_process_steps` | 查流程的步骤定义 | `process_id` |

### Rocks (13)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_my_archived_rocks` | 查我已归档的 rocks | 无 |
| `bloomgrowth_get_user_archived_rocks` | 查指定用户已归档的 rocks | `user_id` |
| `bloomgrowth_create_rock` | 创建 rock | `title`, `accountable_user_id?` |
| `bloomgrowth_get_rock_notes` | 查 rock 备注文档 | `rock_id`, `show_controls?`, `read_only?` |
| `bloomgrowth_get_my_rocks` | 查我的 rocks | `include_origin?` |
| `bloomgrowth_get_user_rocks` | 查指定用户的 rocks | `user_id`, `include_origin?` |
| `bloomgrowth_update_rock` | 更新 rock | `rock_id`, `title?`, `accountable_user_id?`, `completion?`(AtRisk/OnTrack/Complete/Indeterminate) |
| `bloomgrowth_delete_rock` | 删除 rock | `rock_id` |
| `bloomgrowth_get_rock` | 查 rock 详情 | `rock_id`, `include_origin?` |
| `bloomgrowth_archive_rock` | 归档 rock | `rock_id` |
| `bloomgrowth_get_rock_milestones` | 查 rock 的里程碑列表 | `rock_id` |
| `bloomgrowth_create_rock_milestone` | 给 rock 创建里程碑 | `rock_id`, `title`, `due_date` |
| `bloomgrowth_restore_rock` | 恢复已归档的 rock | `rock_id` |

### Role (4)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_role` | 查角色详情 | `role_id` |
| `bloomgrowth_update_role` | 重命名角色 | `role_id`, `title` |
| `bloomgrowth_delete_role` | 删除角色 | `role_id` |
| `bloomgrowth_restore_role` | 恢复已删除角色 | `role_id` |

### Scorecard (3)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_meeting_scorecard` | 查会议计分卡 | `meeting_id` |
| `bloomgrowth_get_my_scorecard` | 查我的计分卡 | 无(MSPbots 现有集成实际使用的唯一接口) |
| `bloomgrowth_get_user_scorecard` | 查指定用户的计分卡 | `user_id` |

### Seats (13)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_my_seats` | 查我持有的组织架构席位 | 无 |
| `bloomgrowth_get_user_seats` | 查指定用户持有的席位 | `user_id` |
| `bloomgrowth_get_seat` | 查席位详情 | `seat_id` |
| `bloomgrowth_delete_seat` | 删除席位 | `seat_id` |
| `bloomgrowth_add_seat_direct_report` | 给席位指定下属关系 | `seat_id`, `user_id` |
| `bloomgrowth_get_seat_position` | 查席位的职位 | `seat_id` |
| `bloomgrowth_set_seat_position` | 设置席位职位 | `seat_id`, `title` |
| `bloomgrowth_delete_seat_position` | 移除席位职位 | `seat_id` |
| `bloomgrowth_add_seat_role` | 给席位添加角色 | `seat_id`, `name` |
| `bloomgrowth_get_seat_roles` | 查席位的角色列表 | `seat_id` |
| `bloomgrowth_remove_seat_user` | 从席位移除用户 | `seat_id`, `user_id?` |
| `bloomgrowth_assign_seat_user` | 给席位指派用户 | `seat_id`, `user_id` |
| `bloomgrowth_get_seat_users` | 查席位上的用户 | `seat_id` |

### Teams (6)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_create_team` | 创建团队 | `title` |
| `bloomgrowth_get_team` | 查团队详情 | `team_id` |
| `bloomgrowth_update_team` | 重命名团队 | `team_id`, `title` |
| `bloomgrowth_add_team_member` | 添加团队成员 | `team_id`, `user_id` |
| `bloomgrowth_remove_team_member` | 移除团队成员 | `team_id`, `user_id` |
| `bloomgrowth_get_team_members` | 查团队成员列表 | `team_id` |

### Todos (7)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_create_todo` | 创建 to-do | `title`, `notes?`, `due_date?` |
| `bloomgrowth_get_todo_notes` | 查 to-do 备注文档 | `todo_id`, `show_controls?`, `read_only?` |
| `bloomgrowth_get_user_todos` | 查指定用户的 to-dos | `user_id` |
| `bloomgrowth_get_my_todos` | 查我的 to-dos | 无 |
| `bloomgrowth_update_todo` | 更新 to-do | `todo_id`, `title?`, `due_date?` |
| `bloomgrowth_get_todo` | 查 to-do 详情 | `todo_id` |
| `bloomgrowth_complete_todo` | 标记 to-do 完成/未完成 | `todo_id`, `status?` |

### Users (6)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_my_profile` | 查我的资料 | 无 |
| `bloomgrowth_get_my_direct_reports` | 查我的直接下属 | 无 |
| `bloomgrowth_get_my_viewable_users` | 查我可见的全部用户 | 无 |
| `bloomgrowth_get_user` | 查指定用户详情 | `user_id` |
| `bloomgrowth_get_user_direct_reports` | 查指定用户的直接下属 | `user_id` |
| `bloomgrowth_get_user_assigned_seats` | 查指定用户被指派的席位 | `user_id` |

### Misc — Quarterly Conversations / Scores / Search / Position / Week (8)

| Tool | 功能 | 参数 |
|---|---|---|
| `bloomgrowth_get_quarterly_conversations` | 列出季度对话 | 无 |
| `bloomgrowth_get_quarterly_conversation_data` | 查季度对话详情 | `quarterly_conversation_id` |
| `bloomgrowth_update_score` | 更新单条计分卡分值 | `score_id`, `value?` |
| `bloomgrowth_get_score` | 查单条计分卡分值 | `score_id`, `include_origin?` |
| `bloomgrowth_search_all` | 全站搜索 | `term?` |
| `bloomgrowth_search_user` | 搜索用户 | `term?` |
| `bloomgrowth_get_my_position` | 查我的职位 | 无 |
| `bloomgrowth_get_current_week` | 查当前 Bloom Growth 周 | 无 |

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

- Not yet tested against a live Bloom Growth account — only protocol-level verification (health check, 401 on missing token, `tools/list` returning all 123 tools, and JSON-schema validation confirming every array-type parameter has an `items` definition) has been done so far.
- Scope is the **full public API** (123 operations, all 18 tag categories, including writes), per explicit user decision — MSPbots' own integration currently uses only 1 of these endpoints (`bloomgrowth_get_my_scorecard`).
- Several request bodies with optional fields (e.g. `bloomgrowth_create_measurable`, `bloomgrowth_update_rock`) are exposed as named optional parameters rather than a generic `body: dict`, since the Bloom Growth schemas are shallow (no deep nesting) — this differs from the `body`/`extra_params` dict pattern used in larger/deeper-nested vendor APIs elsewhere in this MCP fleet.
- Endpoints whose exact request/response shape wasn't fully described by the OpenAPI spec (a few return simple 200 with no documented body) are implemented to match the spec's declared parameters; verify against a real account before relying on edge-case behavior.
