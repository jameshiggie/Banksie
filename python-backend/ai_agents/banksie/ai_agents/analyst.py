from agents import Agent
from ai_agents.utils.state import StateContext
from ai_agents.banksie.tools.do import perform_analysis

sys_msg = """
You are a helpful assistant that can help the user with their business banking needs.
"""

def analyst_agent() -> Agent:
    """
    The analyst agent is responsible for performing analysis on the user's transaction data.
    """
    agent = Agent[StateContext](
        name="analyst Agent",
        instructions=sys_msg,
        model="gpt-4o-mini",
        tool_use_behavior="run_llm_again",
        tools=[perform_analysis],
        handoffs=[],
    )
    
    return agent
