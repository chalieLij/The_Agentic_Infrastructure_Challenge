import re
from enum import Enum
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class TaskType(str, Enum):
    GENERATE = "generate"
    REPLY = "reply"
    TRANSACT = "transact"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: TaskType
    payload: Dict[str, Any]
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    assigned_worker_id: Optional[UUID] = None

class AgentPersona(BaseModel):
    name: str
    voice_traits: List[str]
    bio: str
    directives: List[str]

    @classmethod
    def from_markdown(cls, content: str) -> "AgentPersona":
        """
        Parses a markdown string to create an AgentPersona.
        Expected format:
        # Name
        ## Voice Traits
        - Trait 1
        ## Bio
        Bio text...
        ## Directives
        - Directive 1
        """
        name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else "Unknown"

        voice_traits = []
        bio_lines = []
        directives = []
        
        current_section = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.lower().startswith('## voice traits'):
                current_section = 'voice'
                continue
            elif line.lower().startswith('## bio'):
                current_section = 'bio'
                continue
            elif line.lower().startswith('## directives'):
                current_section = 'directives'
                continue
            elif line.startswith('##'):
                current_section = None
                continue

            if current_section == 'voice':
                if line.startswith('- '):
                    voice_traits.append(line[2:].strip())
            elif current_section == 'bio':
                 bio_lines.append(line)
            elif current_section == 'directives':
                if line.startswith('- '):
                    directives.append(line[2:].strip())

        return cls(
            name=name,
            voice_traits=voice_traits,
            bio=" ".join(bio_lines).strip(),
            directives=directives
        )

class GlobalState(BaseModel):
    """
    GlobalState is used for synchronizing the swarm.
    It holds the current version for concurrency control, list of active agents,
    and the overarching campaign goals.
    """
    version: int = 0
    active_agents: List[UUID] = Field(default_factory=list, description="List of IDs of currently active agents")
    campaign_goals: Dict[str, Any] = Field(default_factory=dict)
