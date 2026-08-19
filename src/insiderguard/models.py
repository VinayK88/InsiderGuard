from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    event_id: str
    ts: str
    user: str
    department: str
    event_type: str
    bytes_mb: float = 0.0
    external: bool = False
    after_hours: bool = False
    new_country: bool = False
    privileged: bool = False
    label: str = "benign"
