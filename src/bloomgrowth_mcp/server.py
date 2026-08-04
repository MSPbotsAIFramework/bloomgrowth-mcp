import contextvars
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .api_client import BloomGrowthClient
from .config import Settings

# Per-request credential isolation via contextvars.
# GatewayTokenMiddleware sets this before the MCP handler runs.
# Python asyncio copies context per task, so concurrent SSE connections are isolated.
_gateway_token_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "bloomgrowth_gateway_token", default=None
)


def get_client_from_context(settings: Settings) -> BloomGrowthClient | None:
    """Resolve the active BloomGrowthClient for the current request context."""
    token = _gateway_token_var.get()
    if not token:
        return None
    return BloomGrowthClient(token, settings.bloomgrowth_base_url)


class GatewayTokenMiddleware:
    """ASGI middleware.

    Reads X-BloomGrowth-Token (required) from request headers and stores it
    in the contextvar. Returns 401 if missing on /mcp requests.
    """

    def __init__(self, app: ASGIApp, settings: Settings):
        self.app = app
        self.settings = settings

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if not path.startswith("/mcp"):
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        token = request.headers.get("x-bloomgrowth-token")
        if not token:
            response = JSONResponse(
                {
                    "error": "Missing credentials",
                    "message": (
                        "This server requires the X-BloomGrowth-Token header "
                        "containing a valid OAuth2 bearer access token"
                    ),
                    "required_headers": ["X-BloomGrowth-Token"],
                    "optional_headers": [],
                },
                status_code=401,
            )
            await response(scope, receive, send)
            return

        ctx_token = _gateway_token_var.set(token)
        try:
            await self.app(scope, receive, send)
        finally:
            _gateway_token_var.reset(ctx_token)


def create_mcp_server(settings: Settings) -> FastMCP:
    """Build the FastMCP server instance and register all Bloom Growth tools."""
    # DNS-rebinding protection is a browser-oriented safeguard that rejects
    # non-localhost Host headers with 421. Disable it so the server works
    # correctly behind a reverse proxy or docker network.
    mcp = FastMCP(
        name="bloomgrowth-mcp",
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )

    client_factory: Callable[[], BloomGrowthClient | None] = lambda: get_client_from_context(settings)

    from .tools import (
        measurables,
        scorecard,
    )

    measurables.register(mcp, client_factory)
    scorecard.register(mcp, client_factory)

    return mcp
