import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_my_seats() -> str:
        """Get the calling user's seats (org-chart positions held).

        API: GET /api/v1/seats/user/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/seats/user/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_seats(user_id: int) -> str:
        """Get a specific user's seats.

        API: GET /api/v1/seats/user/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/seats/user/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_seat(seat_id: int) -> str:
        """Get an org-chart seat by ID.

        API: GET /api/v1/seats/{SEAT_ID}

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/seats/{seat_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_seat(seat_id: int) -> str:
        """Delete an org-chart seat.

        API: DELETE /api/v1/seats/{SEAT_ID}

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/seats/{seat_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_seat_direct_report(seat_id: int, user_id: int) -> str:
        """Assign a direct-report relationship from a seat to a user.

        API: POST /api/v1/seats/{SEAT_ID}/directreport/{USER_ID}

        Args:
            seat_id: Required seat ID.
            user_id: Required direct-report user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/seats/{seat_id}/directreport/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_seat_position(seat_id: int) -> str:
        """Get the position (job title) assigned to a seat.

        API: GET /api/v1/seats/{SEAT_ID}/position

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/seats/{seat_id}/position")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_set_seat_position(seat_id: int, title: str) -> str:
        """Set the position (job title) for a seat.

        API: PUT /api/v1/seats/{SEAT_ID}/position

        Args:
            seat_id: Required seat ID.
            title: Required position title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/seats/{seat_id}/position", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_seat_position(seat_id: int) -> str:
        """Remove the position from a seat.

        API: DELETE /api/v1/seats/{SEAT_ID}/position

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/seats/{seat_id}/position")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_seat_role(seat_id: int, name: str) -> str:
        """Add a role (by name) to a seat.

        API: PUT /api/v1/seats/{SEAT_ID}/role

        Args:
            seat_id: Required seat ID.
            name: Required role name.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/seats/{seat_id}/role", params={"name": name})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_seat_roles(seat_id: int) -> str:
        """Get the roles assigned to a seat.

        API: GET /api/v1/seats/{SEAT_ID}/roles

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/seats/{seat_id}/roles")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_remove_seat_user(seat_id: int, user_id: int | None = None) -> str:
        """Remove a user from a seat.

        API: DELETE /api/v1/seats/{SEAT_ID}/user

        Args:
            seat_id: Required seat ID.
            user_id: Optional user ID to remove (if the API supports removing
                a specific occupant vs. clearing the seat).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/seats/{seat_id}/user", params={"USER_ID": user_id})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_assign_seat_user(seat_id: int, user_id: int) -> str:
        """Assign a user to a seat.

        API: POST /api/v1/seats/{SEAT_ID}/user/{USER_ID}

        Args:
            seat_id: Required seat ID.
            user_id: Required user ID to assign.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/seats/{seat_id}/user/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_seat_users(seat_id: int) -> str:
        """Get the users occupying a seat.

        API: GET /api/v1/seats/{SEAT_ID}/users

        Args:
            seat_id: Required seat ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/seats/{seat_id}/users")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
