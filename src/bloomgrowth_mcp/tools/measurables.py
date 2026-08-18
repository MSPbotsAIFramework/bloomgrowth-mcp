from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .._json import dump_json_capped
from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_measurable(
        name: str | None = None,
        direction: str | None = None,
        target: float | None = None,
        unit_type: str | None = None,
        accountable_user_id: int | None = None,
    ) -> str:
        """Create a scorecard measurable.

        Args:
            name: Optional measurable name.
            direction: Optional comparison operator — one of "EqualTo",
                "GreaterThan", "GreaterThanNotEqual", "Between",
                "LessThanOrEqual", "LessThan".
            target: Optional target value.
            unit_type: Optional unit — one of "None", "Dollar", "Percent",
                "Pound", "Euros", "Pesos", "Yen", "YesNo", "INR", "Dirham",
                "Rand", "XCG".
            accountable_user_id: Optional accountable user ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if name is not None:
            body["name"] = name
        if direction is not None:
            body["direction"] = direction
        if target is not None:
            body["target"] = target
        if unit_type is not None:
            body["unitType"] = unit_type
        if accountable_user_id is not None:
            body["accountableUserId"] = accountable_user_id
        try:
            result = await client.post("/api/v1/measurables/create", json_body=body)
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_my_measurables(include_origin: bool | None = None) -> str:
        """Get the calling user's measurables.

        Args:
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                "/api/v1/measurables/user/mine", params={"Include_Origin": include_origin}
            )
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_user_measurables(user_id: int, include_origin: bool | None = None) -> str:
        """Get a specific user's measurables.

        Args:
            user_id: Required user ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/measurables/user/{user_id}", params={"Include_Origin": include_origin}
            )
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def bloomgrowth_update_measurable(
        measurable_id: int,
        name: str | None = None,
        direction: str | None = None,
        target: float | None = None,
        unit_type: str | None = None,
        alt_target: float | None = None,
    ) -> str:
        """Update a measurable's definition.

        Args:
            measurable_id: Required measurable ID.
            name: Optional new name.
            direction: Optional comparison operator (see
                bloomgrowth_create_measurable for allowed values).
            target: Optional new target value.
            unit_type: Optional new unit type (see bloomgrowth_create_measurable
                for allowed values).
            alt_target: Optional alternate target value (used with "Between").
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if name is not None:
            body["name"] = name
        if direction is not None:
            body["direction"] = direction
        if target is not None:
            body["target"] = target
        if unit_type is not None:
            body["unitType"] = unit_type
        if alt_target is not None:
            body["altTarget"] = alt_target
        try:
            result = await client.put(f"/api/v1/measurables/{measurable_id}", json_body=body)
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_measurable(measurable_id: int, include_origin: bool | None = None) -> str:
        """Get a measurable by ID.

        Args:
            measurable_id: Required measurable ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/measurables/{measurable_id}", params={"Include_Origin": include_origin}
            )
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    async def bloomgrowth_get_measurable_scores(
        measurable_id: int, include_origin: bool | None = None
    ) -> str:
        """Get the weekly scores recorded for a measurable.

        Args:
            measurable_id: Required measurable ID.
            include_origin: Optional — include origin metadata.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(
                f"/api/v1/measurables/{measurable_id}/scores", params={"Include_Origin": include_origin}
            )
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()

    @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
    async def bloomgrowth_set_measurable_week_value(
        measurable_id: int, week_id: int, value: float | None = None
    ) -> str:
        """Set a measurable's score value for a specific week.

        Args:
            measurable_id: Required measurable ID.
            week_id: Required week ID.
            value: Optional score value to set.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        body: dict = {}
        if value is not None:
            body["value"] = value
        try:
            result = await client.put(
                f"/api/v1/measurables/{measurable_id}/week/{week_id}", json_body=body
            )
            return dump_json_capped(result)
        except BloomGrowthError as e:
            return e.to_envelope()
