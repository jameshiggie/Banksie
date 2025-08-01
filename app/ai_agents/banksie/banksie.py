from agents import Agent, Runner
from ai_agents.banksie.ai_agents.analyst import analyst_agent
from ai_agents.banksie.hooks import BanksieRunHook
from ai_agents.utils.log import get_logger
from ai_agents.utils.state import StateContext

# Get configured logger for Banksie
logger = get_logger("banksie")

class BanksieAgent(Agent):
    """
    The BanksieAgent is a specialized agent to help the user with business banking needs.
    """

    def __init__(self):
        super().__init__(name="banksie")
        self.logger = logger  # Use the configured logger
        
    async def run(self, state_context: StateContext, prompt: str):
        output = None
        
        try:
            self.logger.info(f"[Banksie] Received prompt: {prompt}")
            # Agents SDK flow
            output = Runner.run_streamed(
                    analyst_agent(),
                    context=state_context,
                    input=prompt,
                    hooks=BanksieRunHook(),
                )
            
            return output
        
        except Exception as e:
            self.logger.error(f"[Banksie] Error: {e}")
        
        finally:
            return output

