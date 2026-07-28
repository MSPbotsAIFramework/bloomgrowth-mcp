import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_my_profile() -> str:
        """Get the calling user's own profile.

        API: GET /api/v1/users/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/users/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_direct_reports() -> str:
        """Get the calling user's direct reports.

        API: GET /api/v1/users/minedirectreports
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/users/minedirectreports")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_viewable_users() -> str:
        """Get all users visible to the calling user.

        API: GET /api/v1/users/mineviewable
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/users/mineviewable")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user(user_id: int) -> str:
        """Get a user by ID.

        API: GET /api/v1/users/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/users/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_direct_reports(user_id: int) -> str:
        """Get a specific user's direct reports.

        API: GET /api/v1/users/{userId}/directreports

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/users/{user_id}/directreports")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_assigned_seats(user_id: int) -> str:
        """Get the seats assigned to a specific user.

        API: GET /api/v1/users/{userId}/seats

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/users/{user_id}/seats")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
