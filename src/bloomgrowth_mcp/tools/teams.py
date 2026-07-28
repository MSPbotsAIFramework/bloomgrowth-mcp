import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_team(title: str) -> str:
        """Create a team.

        API: POST /api/v1/teams/create

        Args:
            title: Required team title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post("/api/v1/teams/create", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_team(team_id: int) -> str:
        """Get a team by ID.

        API: GET /api/v1/teams/{TEAM_ID}

        Args:
            team_id: Required team ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/teams/{team_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_team(team_id: int, title: str) -> str:
        """Rename a team.

        API: PUT /api/v1/teams/{TEAM_ID}

        Args:
            team_id: Required team ID.
            title: Required new title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/teams/{team_id}", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_team_member(team_id: int, user_id: int) -> str:
        """Add a user to a team.

        API: POST /api/v1/teams/{TEAM_ID}/member/{USER_ID}

        Args:
            team_id: Required team ID.
            user_id: Required user ID to add.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/teams/{team_id}/member/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_remove_team_member(team_id: int, user_id: int) -> str:
        """Remove a user from a team.

        API: DELETE /api/v1/teams/{TEAM_ID}/member/{USER_ID}

        Args:
            team_id: Required team ID.
            user_id: Required user ID to remove.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/teams/{team_id}/member/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_team_members(team_id: int) -> str:
        """Get the members of a team.

        API: GET /api/v1/teams/{TEAM_ID}/members

        Args:
            team_id: Required team ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/teams/{team_id}/members")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
