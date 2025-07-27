from dataclasses import dataclass, field
from typing import Literal


@dataclass
class StateContext:
    # User prompt
    prompt: str = field(default="")
    # Step number
    step: int = 0
    # Transaction data
    transaction_data: list[dict] = field(default_factory=list)
    