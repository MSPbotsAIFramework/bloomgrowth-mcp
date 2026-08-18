"""tools/list snapshot + error-envelope mapping tests.

No network calls: tool enumeration goes through FastMCP's in-process
list_tools(), and the error-code mapping is tested directly against
BloomGrowthError, independent of any real HTTP request.
"""

import pytest

from bloomgrowth_mcp.api_client import BloomGrowthError
from bloomgrowth_mcp.config import Settings
from bloomgrowth_mcp.server import create_mcp_server

EXPECTED_TOOLS = {
    "bloomgrowth_create_measurable": set(),
    "bloomgrowth_get_my_measurables": set(),
    "bloomgrowth_get_user_measurables": {"user_id"},
    "bloomgrowth_update_measurable": {"measurable_id"},
    "bloomgrowth_get_measurable": {"measurable_id"},
    "bloomgrowth_get_measurable_scores": {"measurable_id"},
    "bloomgrowth_set_measurable_week_value": {"measurable_id", "week_id"},
    "bloomgrowth_get_meeting_scorecard": {"meeting_id"},
    "bloomgrowth_get_my_scorecard": set(),
    "bloomgrowth_get_user_scorecard": {"user_id"},
}

# Tools that read data without side effects.
READ_ONLY_TOOLS = {
    "bloomgrowth_get_my_measurables",
    "bloomgrowth_get_user_measurables",
    "bloomgrowth_get_measurable",
    "bloomgrowth_get_measurable_scores",
    "bloomgrowth_get_meeting_scorecard",
    "bloomgrowth_get_my_scorecard",
    "bloomgrowth_get_user_scorecard",
}

# PUT-style tools that overwrite a definition/value but are safely
# re-callable with the same arguments (not delete/irreversible actions).
IDEMPOTENT_TOOLS = {
    "bloomgrowth_update_measurable",
    "bloomgrowth_set_measurable_week_value",
}


@pytest.mark.asyncio
async def test_tools_list_snapshot():
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert names == set(EXPECTED_TOOLS), f"unexpected tool set: {names}"

    by_name = {t.name: t for t in tools}
    for name, expected_required in EXPECTED_TOOLS.items():
        tool = by_name[name]
        required = set(tool.inputSchema.get("required", []))
        assert required == expected_required, f"{name}: required={required}"


@pytest.mark.asyncio
async def test_tool_annotations_and_description_limits():
    """Loop over every registered tool (rather than hand-writing a giant
    per-tool assertion block) and check the SOP's Agent-facing constraints:
    description <= 500 chars, first line <= 100 chars, and the expected
    readOnlyHint / idempotentHint semantics.
    """
    mcp = create_mcp_server(Settings())
    tools = await mcp.list_tools()
    assert len(tools) == 10

    for tool in tools:
        description = tool.description or ""
        assert len(description) <= 500, f"{tool.name}: description too long ({len(description)})"
        first_line = description.strip().splitlines()[0] if description.strip() else ""
        assert len(first_line) <= 100, f"{tool.name}: first line too long: {first_line!r}"
        assert "API:" not in description, f"{tool.name}: leaked implementation-detail line"

        if tool.name in READ_ONLY_TOOLS:
            assert tool.annotations is not None and tool.annotations.readOnlyHint is True, (
                f"{tool.name}: expected readOnlyHint=True"
            )
        if tool.name in IDEMPOTENT_TOOLS:
            assert tool.annotations is not None and tool.annotations.idempotentHint is True, (
                f"{tool.name}: expected idempotentHint=True"
            )


@pytest.mark.asyncio
async def test_service_instructions_present_and_bounded():
    mcp = create_mcp_server(Settings())
    assert mcp.instructions
    assert len(mcp.instructions) <= 1500


@pytest.mark.parametrize(
    "status_code,expected_code,expected_retryable",
    [
        (0, "upstream_error", True),
        (400, "invalid_argument", False),
        (401, "unauthorized", False),
        (403, "unauthorized", False),
        (404, "not_found", False),
        (422, "invalid_argument", False),
        (429, "rate_limited", True),
        (500, "upstream_error", True),
        (503, "upstream_error", True),
    ],
)
def test_error_envelope_mapping(status_code, expected_code, expected_retryable):
    import json

    err = BloomGrowthError(status_code, "boom")
    envelope = json.loads(err.to_envelope())
    assert envelope["error"]["code"] == expected_code
    assert envelope["error"]["retryable"] is expected_retryable
    assert envelope["error"]["message"] == "boom"
