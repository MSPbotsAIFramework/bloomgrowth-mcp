import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_issue(
        meeting_id: int, title: str, owner_id: int | None = None, notes: str | None = None
    ) -> str:
        """Create a standalone issue (not scoped to a specific L10 meeting endpoint).

        API: POST /api/v1/issues/create

        Args:
            meeting_id: Required meeting ID this issue belongs to.
            title: Required issue title.
            owner_id: Optional owning user ID.
            notes: Optional notes text.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"meetingId": meeting_id, "title": title}
        if owner_id is not None:
            body["ownerId"] = owner_id
        if notes is not None:
            body["notes"] = notes
        try:
            result = await client.post("/api/v1/issues/create", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_issue_notes(
        issue_id: int, show_controls: bool | None = None, read_only: bool | None = None
    ) -> str:
        """Get the notes document for an issue.

        API: GET /api/v1/issues/notes/{ISSUE_ID}

        Args:
            issue_id: Required issue ID.
            show_controls: Optional — include editor controls in the response.
            read_only: Optional — render notes as read-only.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/issues/notes/{issue_id}",
                params={"showControls": show_controls, "readOnly": read_only},
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_issues() -> str:
        """Get the calling user's issues.

        API: GET /api/v1/issues/users/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/issues/users/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_issues(user_id: int) -> str:
        """Get a specific user's issues.

        API: GET /api/v1/issues/users/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/issues/users/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_issue(
        issue_id: int,
        title: str | None = None,
        owner_id: int | None = None,
        compartment: str | None = None,
    ) -> str:
        """Update an issue's title, owner, and/or compartment.

        API: PUT /api/v1/issues/{ISSUE_ID}

        Args:
            issue_id: Required issue ID.
            title: Optional new title.
            owner_id: Optional new owning user ID.
            compartment: Optional — "ShortTerm" or "LongTerm".
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if title is not None:
            body["title"] = title
        if owner_id is not None:
            body["ownerId"] = owner_id
        if compartment is not None:
            body["compartment"] = compartment
        try:
            result = await client.put(f"/api/v1/issues/{issue_id}", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_issue(issue_id: int) -> str:
        """Get an issue by ID.

        API: GET /api/v1/issues/{ISSUE_ID}

        Args:
            issue_id: Required issue ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/issues/{issue_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_complete_issue(issue_id: int, complete: bool | None = None) -> str:
        """Mark an issue as complete or incomplete.

        API: POST /api/v1/issues/{ISSUE_ID}/complete

        Args:
            issue_id: Required issue ID.
            complete: Optional — true to mark complete, false to reopen.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if complete is not None:
            body["complete"] = complete
        try:
            result = await client.post(f"/api/v1/issues/{issue_id}/complete", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_move_issue_from_vto(issue_id: int) -> str:
        """Move an issue out of the VTO (Vision/Traction Organizer) list.

        API: POST /api/v1/issues/{ISSUE_ID}/movefromvto

        Args:
            issue_id: Required issue ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/issues/{issue_id}/movefromvto")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_move_issue_to_meeting(issue_id: int, meeting_id: int) -> str:
        """Move an issue to a different L10 meeting.

        API: POST /api/v1/issues/{ISSUE_ID}/movetomeeting/{MEETING_ID}

        Args:
            issue_id: Required issue ID.
            meeting_id: Required destination meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/issues/{issue_id}/movetomeeting/{meeting_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_move_issue_to_vto(issue_id: int) -> str:
        """Move an issue to the VTO (Vision/Traction Organizer) list.

        API: POST /api/v1/issues/{ISSUE_ID}/movetovto

        Args:
            issue_id: Required issue ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/issues/{issue_id}/movetovto")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
