from dataclasses import dataclass, field
from typing import Literal


@dataclass
class StateContext:
    #user prompt
    prompt: str = field(default="")
    #step number
    step: int = 0
    #transaction data
    transaction_data: list[dict] = field(default_factory=list)
    