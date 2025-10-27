from pydantic import BaseModel

# models.py (excerpt)
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    id: str
    name: str
    category: str = "household"
    pillar: str = "identification"    # or anticipation/decision/monitoring/emotional
    requires_children: bool = False
    requires_employment: bool = False
    requires_pets: bool = False  
    requires_vehicle: bool = False  

    # (all optional):
    definition: Optional[str] = None
    what_counts: Optional[List[str]] = field(default_factory=list)
    note: Optional[str] = None
    example: Optional[str] = None

class Response(BaseModel):
    task: Task
    responsibility: int          # 0..100 (0=A, 100=B)
    burden: int                  # 1..5
    fairness: int                # 1..5
    not_applicable: bool = False
