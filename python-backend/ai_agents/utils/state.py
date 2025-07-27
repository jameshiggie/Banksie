from dataclasses import dataclass, field
from typing import Literal


@dataclass
class StateContext:
    prompt: str = field(default="")
    transaction_data: str = field(default="")
    step: int = 0
    