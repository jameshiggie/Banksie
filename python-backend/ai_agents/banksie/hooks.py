from agents import RunHooks, RunContextWrapper, Agent, Tool
from ai_agents.utils.state import StateContext
from typing import Any

class BanksieRunHook(RunHooks):
    """
    The main hook on the Banksie Agent.
    """

    async def on_tool_start(self, context: RunContextWrapper[StateContext], agent: Agent, tool: Tool) -> None:
        """
        placeholder for ui updates for what the tool the agent is using and what its doing
        """
        pass
    
    async def on_tool_end(self, context: RunContextWrapper[StateContext], agent: Agent, tool: Tool, result: Any) -> None:
        pass