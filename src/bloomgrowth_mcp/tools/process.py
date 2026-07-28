import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from ..api_client import BloomGrowthClient, BloomGrowthError
from ._common import NO_TOKEN


def register(mcp: FastMCP, client_factory: Callable[[], BloomGrowthClient | None]) -> None:

    @mcp.tool()
    async def bloomgrowth_get_process_execution_steps(started_process_id: int) -> str:
        """Get the steps of a started (executed) process instance.

        API: GET /api/v1/process/execution/{STARTED_PROCESS_ID}/steps

        Args:
            started_process_id: Required started-process instance ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/process/execution/{started_process_id}/steps")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_process_folders() -> str:
        """List process folders.

        API: GET /api/v1/process/folder/list
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/process/folder/list")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_processes(folder_id: int | None = None) -> str:
        """List processes, optionally filtered by folder.

        API: GET /api/v1/process/list

        Args:
            folder_id: Optional folder ID to filter by.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get("/api/v1/process/list", params={"FOLDER_ID": folder_id})
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_complete_process_step(step_id: int, completion: bool) -> str:
        """Mark a process step's completion state on a started process.

        API: POST /api/v1/process/steps/{STEP_ID}

        Args:
            step_id: Required process step ID.
            completion: Required — true to mark complete, false to reopen.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(
                f"/api/v1/process/steps/{step_id}", json_body={"completion": completion}
            )
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_process(process_id: int) -> str:
        """Get a process definition by ID.

        API: GET /api/v1/process/{PROCESS_ID}

        Args:
            process_id: Required process ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/process/{process_id}")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_execute_process(process_id: int) -> str:
        """Start (execute) a new instance of a process.

        API: POST /api/v1/process/{PROCESS_ID}/execute

        Args:
            process_id: Required process ID to execute.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.post(f"/api/v1/process/{process_id}/execute")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"

    @mcp.tool()
    async def bloomgrowth_get_process_steps(process_id: int) -> str:
        """Get the step definitions of a process.

        API: GET /api/v1/process/{PROCESS_ID}/steps

        Args:
            process_id: Required process ID.
        """
        client = client_factory()
        if client is None:
            return NO_TOKEN
        try:
            result = await client.get(f"/api/v1/process/{process_id}/steps")
            return json.dumps(result, indent=2)
        except BloomGrowthError as e:
            return f"Error: {e}"
