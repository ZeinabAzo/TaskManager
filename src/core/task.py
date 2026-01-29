from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    id : int
    start_time : int
    end_time : int
    value : int