from agents import Agent
from pathlib import Path

from ai_agents.utils.state import StateContext
from ai_agents.banksie.tools.perform_analysis import perform_analysis


def analyst_agent() -> Agent:
    """
    The analyst agent can access the user's transaction data using its tools and perform analysis on it.
    """
    #load the sys_msg from the md file
    sys_msg = Path("ai_agents/banksie/ai_agents/system_message/analyst.md").read_text(encoding="utf-8")
    
    agent = Agent[StateContext](
        name="analyst Agent",
        instructions=sys_msg,
        model="gpt-4.1",
        tool_use_behavior="run_llm_again",
        tools=[perform_analysis],
        handoffs=[],
    )
    
    return agent
