from dataclasses import dataclass, field
from typing import Literal


@dataclass
class StateContext:
    prompt: str = field(default="")

    agent: Literal["Banksie", "Analyst", "biblioteca"] = field(default="Banksie")
    step: int = 0
    