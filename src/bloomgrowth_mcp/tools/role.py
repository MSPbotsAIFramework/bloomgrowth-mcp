import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_role(role_id: int) -> str:
        """Get a role by ID.

        API: GET /api/v1/role/{ROLE_ID}

        Args:
            role_id: Required role ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/role/{role_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_role(role_id: int, title: str) -> str:
        """Rename a role.

        API: PUT /api/v1/role/{ROLE_ID}

        Args:
            role_id: Required role ID.
            title: Required new title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/role/{role_id}", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_role(role_id: int) -> str:
        """Delete a role.

        API: DELETE /api/v1/role/{ROLE_ID}

        Args:
            role_id: Required role ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/role/{role_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_restore_role(role_id: int) -> str:
        """Restore a previously deleted role.

        API: PATCH /api/v1/role/{ROLE_ID}/restore

        Args:
            role_id: Required role ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.patch(f"/api/v1/role/{role_id}/restore")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
