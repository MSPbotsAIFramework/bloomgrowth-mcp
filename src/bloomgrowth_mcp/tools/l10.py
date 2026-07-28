import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_l10_meeting(title: str, add_self: bool | None = None) -> str:
        """Create a new L10 (Level 10) meeting.

        API: POST /api/v1/L10/create

        Args:
            title: Required meeting title.
            add_self: Optional — add the calling user as an attendee.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body = {"title": title}
        if add_self is not None:
            body["addSelf"] = add_self
        try:
            result = await client.post("/api/v1/L10/create", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_meetings() -> str:
        """List all L10 meetings.

        API: GET /api/v1/L10/list
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/L10/list")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_l10_meeting(meeting_id: int, title: str) -> str:
        """Rename an L10 meeting.

        API: PUT /api/v1/L10/{MEETING_ID}

        Args:
            meeting_id: Required meeting ID.
            title: Required new title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/L10/{meeting_id}", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_l10_meeting(meeting_id: int) -> str:
        """Delete an L10 meeting.

        API: DELETE /api/v1/L10/{MEETING_ID}

        Args:
            meeting_id: Required meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_meeting(meeting_id: int) -> str:
        """Get an L10 meeting by ID.

        API: GET /api/v1/L10/{MEETING_ID}

        Args:
            meeting_id: Required meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/L10/{meeting_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_attendees(meeting_id: int) -> str:
        """Get the attendees of an L10 meeting.

        API: GET /api/v1/L10/{MEETING_ID}/attendees

        Args:
            meeting_id: Required meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/L10/{meeting_id}/attendees")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_l10_attendee(meeting_id: int, user_id: int) -> str:
        """Add a user as an attendee of an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/attendees/{USER_ID}

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID to add.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/attendees/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_l10_headline(
        meeting_id: int, title: str, owner_id: int | None = None, notes: str | None = None
    ) -> str:
        """Create a headline under an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/headlines

        Args:
            meeting_id: Required meeting ID.
            title: Required headline title.
            owner_id: Optional owning user ID.
            notes: Optional notes text.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"title": title}
        if owner_id is not None:
            body["ownerId"] = owner_id
        if notes is not None:
            body["notes"] = notes
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/headlines", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_l10_headline(meeting_id: int, headline_id: int) -> str:
        """Delete a headline from an L10 meeting.

        API: DELETE /api/v1/L10/{MEETING_ID}/headlines/{HEADLINE_ID}

        Args:
            meeting_id: Required meeting ID.
            headline_id: Required headline ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}/headlines/{headline_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_l10_issue(
        meeting_id: int, title: str, owner_id: int | None = None, details: str | None = None
    ) -> str:
        """Create an issue under an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/issues

        Args:
            meeting_id: Required meeting ID.
            title: Required issue title.
            owner_id: Optional owning user ID.
            details: Optional details text.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"title": title}
        if owner_id is not None:
            body["ownerId"] = owner_id
        if details is not None:
            body["details"] = details
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/issues", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_l10_issue(meeting_id: int, issue_id: int) -> str:
        """Delete an issue from an L10 meeting.

        API: DELETE /api/v1/L10/{MEETING_ID}/issues/{ISSUE_ID}

        Args:
            meeting_id: Required meeting ID.
            issue_id: Required issue ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}/issues/{issue_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_l10_measurable(meeting_id: int, measurable_id: int) -> str:
        """Attach a measurable to an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/measurables/{MEASURABLE_ID}

        Args:
            meeting_id: Required meeting ID.
            measurable_id: Required measurable ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/measurables/{measurable_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_remove_l10_measurable(meeting_id: int, measurable_id: int) -> str:
        """Detach a measurable from an L10 meeting.

        API: DELETE /api/v1/L10/{MEETING_ID}/measurables/{MEASURABLE_ID}

        Args:
            meeting_id: Required meeting ID.
            measurable_id: Required measurable ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}/measurables/{measurable_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_l10_rock(
        meeting_id: int, title: str, accountable_user_id: int | None = None
    ) -> str:
        """Create a rock under an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/rocks

        Args:
            meeting_id: Required meeting ID.
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
            result = await client.post(f"/api/v1/L10/{meeting_id}/rocks", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_rocks(
        meeting_id: int,
        include_archive: bool | None = None,
        include_origin: bool | None = None,
    ) -> str:
        """Get the rocks attached to an L10 meeting.

        API: GET /api/v1/L10/{MEETING_ID}/rocks

        Args:
            meeting_id: Required meeting ID.
            include_archive: Optional — include archived rocks.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        params = {"INCLUDE_ARCHIVE": include_archive, "INCLUDE_ORIGIN": include_origin}
        try:
            result = await client.get(f"/api/v1/L10/{meeting_id}/rocks", params=params)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_l10_rock(meeting_id: int, rock_id: int) -> str:
        """Attach an existing rock to an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/rocks/{ROCK_ID}

        Args:
            meeting_id: Required meeting ID.
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/rocks/{rock_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_remove_l10_rock(meeting_id: int, rock_id: int) -> str:
        """Detach a rock from an L10 meeting.

        API: DELETE /api/v1/L10/{MEETING_ID}/rocks/{ROCK_ID}

        Args:
            meeting_id: Required meeting ID.
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}/rocks/{rock_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_add_l10_rock_to_business_plan(meeting_id: int, rock_id: int) -> str:
        """Add a rock (attached to an L10 meeting) to the business plan.

        API: POST /api/v1/L10/{MEETING_ID}/rocks/{ROCK_ID}/businessplan

        Args:
            meeting_id: Required meeting ID.
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/rocks/{rock_id}/businessplan")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_remove_l10_rock_from_business_plan(meeting_id: int, rock_id: int) -> str:
        """Remove a rock from the business plan.

        API: DELETE /api/v1/L10/{MEETING_ID}/rocks/{ROCK_ID}/businessplan

        Args:
            meeting_id: Required meeting ID.
            rock_id: Required rock ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/L10/{meeting_id}/rocks/{rock_id}/businessplan")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_create_l10_todo(
        meeting_id: int,
        title: str,
        details: str | None = None,
        accountable_user_id: int | None = None,
        due_date: str | None = None,
    ) -> str:
        """Create a to-do under an L10 meeting.

        API: POST /api/v1/L10/{MEETING_ID}/todos

        Args:
            meeting_id: Required meeting ID.
            title: Required to-do title.
            details: Optional details text.
            accountable_user_id: Optional accountable user ID.
            due_date: Optional due date (ISO date string).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"title": title}
        if details is not None:
            body["details"] = details
        if accountable_user_id is not None:
            body["accountableUserId"] = accountable_user_id
        if due_date is not None:
            body["dueDate"] = due_date
        try:
            result = await client.post(f"/api/v1/L10/{meeting_id}/todos", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_l10_meetings(user_id: int) -> str:
        """List L10 meetings a user attends.

        API: GET /api/v1/L10/{USER_ID}/list

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/L10/{user_id}/list")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_headlines(meeting_id: int, include_origin: bool | None = None) -> str:
        """Get all headlines for an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/headlines

        Args:
            meeting_id: Required meeting ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/l10/{meeting_id}/headlines", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_issues(meeting_id: int, include_resolved: bool | None = None) -> str:
        """Get all issues for an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/issues

        Args:
            meeting_id: Required meeting ID.
            include_resolved: Optional — include resolved issues.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/l10/{meeting_id}/issues", params={"INCLUDE_RESOLVED": include_resolved}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_measurables(meeting_id: int) -> str:
        """Get all measurables for an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/measurables

        Args:
            meeting_id: Required meeting ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/l10/{meeting_id}/measurables")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_todos(meeting_id: int, include_closed: bool | None = None) -> str:
        """Get all to-dos for an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/todos

        Args:
            meeting_id: Required meeting ID.
            include_closed: Optional — include closed to-dos.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/l10/{meeting_id}/todos", params={"INCLUDE_CLOSED": include_closed}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_user_headlines(
        meeting_id: int, user_id: int, include_origin: bool | None = None
    ) -> str:
        """Get a specific user's headlines within an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/users/{USER_ID}/headlines

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/l10/{meeting_id}/users/{user_id}/headlines",
                params={"Include_Origin": include_origin},
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_user_issues(meeting_id: int, user_id: int) -> str:
        """Get a specific user's issues within an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/users/{USER_ID}/issues

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/l10/{meeting_id}/users/{user_id}/issues")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_user_measurables(meeting_id: int, user_id: int) -> str:
        """Get a specific user's measurables within an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/users/{USER_ID}/measurables

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/l10/{meeting_id}/users/{user_id}/measurables")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_user_rocks(
        meeting_id: int, user_id: int, include_origin: bool | None = None
    ) -> str:
        """Get a specific user's rocks within an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/users/{USER_ID}/rocks

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/l10/{meeting_id}/users/{user_id}/rocks", params={"INCLUDE_ORIGIN": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_l10_user_todos(meeting_id: int, user_id: int) -> str:
        """Get a specific user's to-dos within an L10 meeting.

        API: GET /api/v1/l10/{MEETING_ID}/users/{USER_ID}/todos

        Args:
            meeting_id: Required meeting ID.
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/l10/{meeting_id}/users/{user_id}/todos")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
