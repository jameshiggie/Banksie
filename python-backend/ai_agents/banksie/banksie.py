
import logging

from agents import Agent, Runner

from ai_agents.banksie.ai_agents.analyst import analyst_agent
from ai_agents.banksie.hooks import BanksieRunHook
from ai_agents.utils.state import StateContext

# Optional: configure logging
logger = logging.getLogger("banksie")
logging.basicConfig(level=logging.INFO)

class BanksieAgent(Agent):
    """
    The BanksieAgent is a specialized agent to help the user with business banking needs.
    """

    def __init__(self):
        super().__init__(name="banksie")
        self.logger = logging.getLogger("banksie")
        
    async def run(self, input):
        output = None
        state_context = StateContext(prompt=input)
        
        try:
            prompt = input.input
            self.logger.info(f"[Banksie] Received prompt: {prompt}")
            
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

