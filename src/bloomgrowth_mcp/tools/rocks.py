import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_my_archived_rocks() -> str:
        """Get the calling user's archived rocks.

        API: GET /api/v1/archivedrocks/user/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/archivedrocks/user/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_archived_rocks(user_id: int) -> str:
        """Get a specific user's archived rocks.

        API: GET /api/v1/archivedrocks/user/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/archivedrocks/user/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_rock(title: str, accountable_user_id: int | None = None) -> str:
        """Create a rock (quarterly priority).

        API: POST /api/v1/rocks/create

        Args:
            title: Required rock title.
            accountable_user_id: Optional accountable user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"title": title}
        if accountable_user_id is not None:
            body["accountableUserId"] = accountable_user_id
        try:
            result = await client.post("/api/v1/rocks/create", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_rock_notes(
        rock_id: int, show_controls: bool | None = None, read_only: bool | None = None
    ) -> str:
        """Get the notes document for a rock.

        API: GET /api/v1/rocks/notes/{ROCK_ID}

        Args:
            rock_id: Required rock ID.
            show_controls: Optional — include editor controls in the response.
            read_only: Optional — render notes as read-only.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/rocks/notes/{rock_id}",
                params={"showControls": show_controls, "readOnly": read_only},
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_rocks(include_origin: bool | None = None) -> str:
        """Get the calling user's rocks.

        API: GET /api/v1/rocks/user/mine

        Args:
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/rocks/user/mine", params={"Include_Origin": include_origin})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_rocks(user_id: int, include_origin: bool | None = None) -> str:
        """Get a specific user's rocks.

        API: GET /api/v1/rocks/user/{USER_ID}

        Args:
            user_id: Required user ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/rocks/user/{user_id}", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_rock(
        rock_id: int,
        title: str | None = None,
        accountable_user_id: int | None = None,
        completion: str | None = None,
    ) -> str:
        """Update a rock's title, owner, and/or completion state.

        API: PUT /api/v1/rocks/{ROCK_ID}

        Args:
            rock_id: Required rock ID.
            title: Optional new title.
            accountable_user_id: Optional new accountable user ID.
            completion: Optional — one of "AtRisk", "OnTrack", "Complete",
                "Indeterminate".
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if title is not None:
            body["title"] = title
        if accountable_user_id is not None:
            body["accountableUserId"] = accountable_user_id
        if completion is not None:
            body["completion"] = completion
        try:
            result = await client.put(f"/api/v1/rocks/{rock_id}", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_rock(rock_id: int) -> str:
        """Delete a rock.

        API: DELETE /api/v1/rocks/{ROCK_ID}

        Args:
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/rocks/{rock_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_rock(rock_id: int, include_origin: bool | None = None) -> str:
        """Get a rock by ID.

        API: GET /api/v1/rocks/{ROCK_ID}

        Args:
            rock_id: Required rock ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/rocks/{rock_id}", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_archive_rock(rock_id: int) -> str:
        """Archive a rock.

        API: PUT /api/v1/rocks/{ROCK_ID}/archive

        Args:
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/rocks/{rock_id}/archive")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_rock_milestones(rock_id: int) -> str:
        """Get the milestones of a rock.

        API: GET /api/v1/rocks/{ROCK_ID}/milestones

        Args:
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/rocks/{rock_id}/milestones")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_rock_milestone(rock_id: int, title: str, due_date: str) -> str:
        """Create a milestone under a rock.

        API: POST /api/v1/rocks/{ROCK_ID}/milestones

        Args:
            rock_id: Required rock ID.
            title: Required milestone title.
            due_date: Required due date (ISO date string).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/v1/rocks/{rock_id}/milestones", json_body={"title": title, "dueDate": due_date}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_restore_rock(rock_id: int) -> str:
        """Restore a previously archived rock.

        API: PUT /api/v1/rocks/{ROCK_ID}/restore

        Args:
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/rocks/{rock_id}/restore")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
