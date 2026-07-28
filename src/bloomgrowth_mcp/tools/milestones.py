import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_milestone(milestone_id: int) -> str:
        """Get a rock milestone by ID.

        API: GET /api/v1/milestones/{MILESTONE_ID}

        Args:
            milestone_id: Required milestone ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/milestones/{milestone_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_milestone(
        milestone_id: int,
        title: str | None = None,
        due_date: str | None = None,
        status: str | None = None,
    ) -> str:
        """Update a rock milestone.

        API: PUT /api/v1/milestones/{MILESTONE_ID}

        Args:
            milestone_id: Required milestone ID.
            title: Optional new title.
            due_date: Optional new due date (ISO date string).
            status: Optional — "NotDone" or "Done".
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if title is not None:
            body["title"] = title
        if due_date is not None:
            body["dueDate"] = due_date
        if status is not None:
            body["status"] = status
        try:
            result = await client.put(f"/api/v1/milestones/{milestone_id}", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_milestone(milestone_id: int) -> str:
        """Delete a rock milestone.

        API: DELETE /api/v1/milestones/{MILESTONE_ID}

        Args:
            milestone_id: Required milestone ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/milestones/{milestone_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
