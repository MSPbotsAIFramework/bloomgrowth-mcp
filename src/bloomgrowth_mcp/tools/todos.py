import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_todo(
        title: str, notes: str | None = None, due_date: str | None = None
    ) -> str:
        """Create a to-do.

        API: POST /api/v1/todo/create

        Args:
            title: Required to-do title.
            notes: Optional notes text.
            due_date: Optional due date (ISO date string).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {"title": title}
        if notes is not None:
            body["notes"] = notes
        if due_date is not None:
            body["dueDate"] = due_date
        try:
            result = await client.post("/api/v1/todo/create", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_todo_notes(
        todo_id: int, show_controls: bool | None = None, read_only: bool | None = None
    ) -> str:
        """Get the notes document for a to-do.

        API: GET /api/v1/todo/notes/{TODO_ID}

        Args:
            todo_id: Required to-do ID.
            show_controls: Optional — include editor controls in the response.
            read_only: Optional — render notes as read-only.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/todo/notes/{todo_id}",
                params={"showControls": show_controls, "readOnly": read_only},
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_todos(user_id: int) -> str:
        """Get a specific user's to-dos.

        API: GET /api/v1/todo/user/{USER_ID}

        Args:
            user_id: Required user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/todo/user/{user_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_todos() -> str:
        """Get the calling user's to-dos.

        API: GET /api/v1/todo/users/mine
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/todo/users/mine")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_todo(
        todo_id: int, title: str | None = None, due_date: str | None = None
    ) -> str:
        """Update a to-do's title and/or due date.

        API: PUT /api/v1/todo/{TODO_ID}

        Args:
            todo_id: Required to-do ID.
            title: Optional new title.
            due_date: Optional new due date (ISO date string).
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if title is not None:
            body["title"] = title
        if due_date is not None:
            body["dueDate"] = due_date
        try:
            result = await client.put(f"/api/v1/todo/{todo_id}", json_body=body)
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_todo(todo_id: int) -> str:
        """Get a to-do by ID.

        API: GET /api/v1/todo/{TODO_ID}

        Args:
            todo_id: Required to-do ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/todo/{todo_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_complete_todo(todo_id: int, status: bool | None = None) -> str:
        """Mark a to-do complete or incomplete.

        API: POST /api/v1/todo/{TODO_ID}/complete

        Args:
            todo_id: Required to-do ID.
            status: Optional — true to mark complete, false to reopen.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/todo/{todo_id}/complete", params={"status": status})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
