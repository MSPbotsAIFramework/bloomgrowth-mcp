import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_meeting_scorecard(meeting_id: int) -> str:
        """Get the scorecard for an L10 meeting.

        API: GET /api/v1/scorecard/meeting/{MEETING_ID}

        Args:
            meeting_id: Required meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/scorecard/meeting/{meeting_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_scorecard() -> str:
        """Get the calling user's scorecard.

        API: GET /api/v1/scorecard/user/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/scorecard/user/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_scorecard(user_id: int) -> str:
        """Get a specific user's scorecard.

        API: GET /api/v1/scorecard/user/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/scorecard/user/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
