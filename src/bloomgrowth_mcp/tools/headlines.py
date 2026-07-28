import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_headline_notes(
        headline_id: int, show_controls: bool | None = None, read_only: bool | None = None
    ) -> str:
        """Get the notes document for a headline.

        API: GET /api/v1/headline/notes/{HEADLINE_ID}

        Args:
            headline_id: Required headline ID.
            show_controls: Optional — include editor controls in the response.
            read_only: Optional — render notes as read-only.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/headline/notes/{headline_id}",
                params={"showControls": show_controls, "readOnly": read_only},
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_my_headlines(include_origin: bool | None = None) -> str:
        """Get the calling user's headlines.

        API: GET /api/v1/headline/users/mine

        Args:
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/v1/headline/users/mine", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_user_headlines(user_id: int, include_origin: bool | None = None) -> str:
        """Get a specific user's headlines.

        API: GET /api/v1/headline/users/{USER_ID}

        Args:
            user_id: Required user ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/headline/users/{user_id}", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_headline(headline_id: int, include_origin: bool | None = None) -> str:
        """Get a headline by ID.

        API: GET /api/v1/headline/{HEADLINE_ID}

        Args:
            headline_id: Required headline ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/headline/{headline_id}", params={"Include_Origin": include_origin}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_update_headline(headline_id: int, title: str) -> str:
        """Rename a headline.

        API: PUT /api/v1/headline/{HEADLINE_ID}

        Args:
            headline_id: Required headline ID.
            title: Required new title.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.put(f"/api/v1/headline/{headline_id}", json_body={"title": title})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_delete_headline(headline_id: int) -> str:
        """Delete a headline.

        API: DELETE /api/v1/headline/{HEADLINE_ID}

        Args:
            headline_id: Required headline ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.delete(f"/api/v1/headline/{headline_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
