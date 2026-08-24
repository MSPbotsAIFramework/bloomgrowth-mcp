from collections.abc import Callable
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .._json import dump_json_capped
from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN

_DIRECTION_VALUES = (
    '"EqualTo", "GreaterThan", "GreaterThanNotEqual", "Between", '
    '"LessThanOrEqual", "LessThan"'
)
_UNIT_TYPE_VALUES = (
    '"None", "Dollar", "Percent", "Pound", "Euros", "Pesos", "Yen", '
    '"YesNo", "INR", "Dirham", "Rand", "XCG"'
)
_INCLUDE_ORIGIN_DESC = (
    "If true, forwards Include_Origin=true to the Bloom Growth API so the "
    "response includes whatever origin/provenance data that endpoint adds "
    "for each record. This server does not parse or reshape that data — it "
    "returns the upstream JSON verbatim, and neither this codebase nor Bloom "
    "Growth's own published OpenAPI spec (https://dev-api.bloomgrowth.com/"
    "swagger/v1/swagger.json) documents which fields appear or what they "
    "mean (the spec's schema component definitions aren't published, and "
    "the word \"origin\" appears nowhere except this parameter's name). "
    "Defaults to false (omitted) if not set. If you need to know exactly "
    "what this adds, call the same tool once with it true and once false "
    "and diff the results."
)
_ID_SOURCE_NOTE = (
    " This server has no tool that looks up or lists valid IDs for this "
    "parameter — it must be supplied from context you already have (e.g. "
    "the Bloom Growth web UI, a prior response from this same server, or "
    "another system)."
)


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_create_measurable(
        name: Annotated[str | None, Field(description="Name of the new measurable.")] = None,
        direction: Annotated[
            str | None,
            Field(description=f"Comparison operator — one of {_DIRECTION_VALUES}."),
        ] = None,
        target: Annotated[
            float | None, Field(description="Target value the weekly score is compared against.")
        ] = None,
        unit_type: Annotated[
            str | None, Field(description=f"Unit of the value — one of {_UNIT_TYPE_VALUES}.")
        ] = None,
        accountable_user_id: Annotated[
            int | None,
            Field(
                description=(
                    "ID of the user accountable for this measurable."
                    + _ID_SOURCE_NOTE
                )
            ),
        ] = None,
    ) -> str:
        """Create a scorecard measurable (KPI definition).

All fields are optional; an all-omitted call still POSTs an empty body,
whatever Bloom Growth does with that. On success the response is a
Measurable object — take its id and pass it as measurable_id to
bloomgrowth_update_measurable / bloomgrowth_get_measurable /
bloomgrowth_get_measurable_scores / bloomgrowth_set_measurable_week_value."""
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
    async def bloomgrowth_get_my_measurables(
        include_origin: Annotated[bool | None, Field(description=_INCLUDE_ORIGIN_DESC)] = None,
    ) -> str:
        """Get the calling user's measurables.

Same list-of-Measurable response shape as bloomgrowth_get_user_measurables,
scoped implicitly to the caller instead of an explicit user_id."""
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
    async def bloomgrowth_get_user_measurables(
        user_id: Annotated[
            int, Field(description="ID of the user whose measurables to list." + _ID_SOURCE_NOTE)
        ],
        include_origin: Annotated[bool | None, Field(description=_INCLUDE_ORIGIN_DESC)] = None,
    ) -> str:
        """Get a specific user's measurables.

Same list-of-Measurable response shape as bloomgrowth_get_my_measurables,
but for an explicitly named user_id instead of the caller."""
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
        measurable_id: Annotated[
            int, Field(description="ID of the measurable to update." + _ID_SOURCE_NOTE)
        ],
        name: Annotated[str | None, Field(description="New name for the measurable.")] = None,
        direction: Annotated[
            str | None,
            Field(
                description=(
                    "New comparison operator — one of "
                    f"{_DIRECTION_VALUES} (see bloomgrowth_create_measurable)."
                )
            ),
        ] = None,
        target: Annotated[float | None, Field(description="New target value.")] = None,
        unit_type: Annotated[
            str | None,
            Field(
                description=(
                    f"New unit type — one of {_UNIT_TYPE_VALUES} (see "
                    "bloomgrowth_create_measurable)."
                )
            ),
        ] = None,
        alt_target: Annotated[
            float | None,
            Field(description='Alternate target value, used when direction is "Between".'),
        ] = None,
    ) -> str:
        """Update an existing measurable's definition (name, target, direction, unit, etc).

Only the fields you pass are sent; omitted fields are left unchanged."""
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
    async def bloomgrowth_get_measurable(
        measurable_id: Annotated[
            int, Field(description="ID of the measurable to fetch." + _ID_SOURCE_NOTE)
        ],
        include_origin: Annotated[bool | None, Field(description=_INCLUDE_ORIGIN_DESC)] = None,
    ) -> str:
        """Get a single measurable's definition by ID.

Same Measurable object shape as one entry in bloomgrowth_get_my_measurables
/ bloomgrowth_get_user_measurables, fetched directly by ID instead of listed."""
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
        measurable_id: Annotated[
            int,
            Field(description="ID of the measurable whose weekly scores to fetch." + _ID_SOURCE_NOTE),
        ],
        include_origin: Annotated[bool | None, Field(description=_INCLUDE_ORIGIN_DESC)] = None,
    ) -> str:
        """Get the weekly scores recorded for a measurable."""
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
        measurable_id: Annotated[
            int, Field(description="ID of the measurable to record a score for." + _ID_SOURCE_NOTE)
        ],
        week_id: Annotated[
            int, Field(description="ID of the week to record the score against." + _ID_SOURCE_NOTE)
        ],
        value: Annotated[
            float | None,
            Field(
                description=(
                    "Score value to set for this week. If omitted, this server "
                    "sends the PUT with an empty JSON body (no \"value\" key at "
                    "all) rather than a null or zero value. What the Bloom "
                    "Growth API then does with a missing value — leave the "
                    "existing score untouched, clear it, default it to 0, or "
                    "reject the request — is not documented in this "
                    "codebase or in Bloom Growth's published OpenAPI spec, "
                    "and this server has not been verified against a live "
                    "account (see README Known Gaps). Pass an explicit value "
                    "if you need a guaranteed outcome."
                )
            ),
        ] = None,
    ) -> str:
        """Set a measurable's score value for a specific week."""
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
