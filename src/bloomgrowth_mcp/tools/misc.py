import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_quarterly_conversations() -> str:
        """List quarterly conversations.

        API: GET /api/v1/quarterlyconversations
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/quarterlyconversations")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_quarterly_conversation_data(quarterly_conversation_id: int) -> str:
        """Get the data for a specific quarterly conversation.

        API: GET /api/v1/quarterlyconversations/data/{QUARTERLY_CONVERSATION_ID}

        Args:
            quarterly_conversation_id: Required quarterly conversation ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/quarterlyconversations/data/{quarterly_conversation_id}"
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_score(score_id: int, value: float | None = None) -> str:
        """Update a single scorecard score value.

        API: PUT /api/v1/scores/{SCORE_ID}

        Args:
            score_id: Required score ID.
            value: Optional new score value.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if value is not None:
            body["value"] = value
        try:
            result = await client.put(f"/api/v1/scores/{score_id}", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_score(score_id: int, include_origin: bool | None = None) -> str:
        """Get a single scorecard score by ID.

        API: GET /api/v1/scores/{SCORE_ID}

        Args:
            score_id: Required score ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/scores/{score_id}", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_search_all(term: str | None = None) -> str:
        """Search across all Bloom Growth entities.

        API: GET /api/v1/search/all

        Args:
            term: Optional search term.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/search/all", params={"term": term})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_search_user(term: str | None = None) -> str:
        """Search for users.

        API: GET /api/v1/search/user

        Args:
            term: Optional search term.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/search/user", params={"term": term})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_position() -> str:
        """Get the calling user's position (job title).

        API: GET /api/v1/positions/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/positions/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_current_week() -> str:
        """Get the current Bloom Growth week (used to key measurable scores).

        API: GET /api/v1/weeks/current
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/weeks/current")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
