from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN

_ID_SOURCE_NOTE = (
    " This server has no tool that looks up or lists valid IDs for this "
    "parameter — it must be supplied from context you already have (e.g. "
    "the Bloom Growth web UI, a prior response from this same server, or "
    "another system)."
)


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_meeting_scorecard(
        meeting_id: Annotated[
            int, Field(description="ID of the L10 meeting whose scorecard to fetch." + _ID_SOURCE_NOTE)
        ],
    ) -> str:
        """Get the scorecard for an L10 meeting (its measurables and on/off-track status)."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/scorecard/meeting/{meeting_id}")
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_my_scorecard() -> str:
        """Get the calling user's scorecard.

Same scorecard shape as bloomgrowth_get_user_scorecard, scoped implicitly
to the caller instead of an explicit user_id."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/scorecard/user/mine")
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_user_scorecard(
        user_id: Annotated[
            int, Field(description="ID of the user whose scorecard to fetch." + _ID_SOURCE_NOTE)
        ],
    ) -> str:
        """Get a specific user's scorecard.

Same scorecard shape as bloomgrowth_get_my_scorecard, but for an explicitly
named user_id instead of the caller."""
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/scorecard/user/{user_id}")
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()
