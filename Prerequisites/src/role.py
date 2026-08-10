from enum import Enum

class Role(Enum):
    """Roles used in a chat transcript."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"