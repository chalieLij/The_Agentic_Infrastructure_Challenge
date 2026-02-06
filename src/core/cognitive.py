from typing import List
from ..models import AgentPersona

class ContextAssembler:
    def build_system_prompt(self, persona: AgentPersona, memories: List[str]) -> str:
        """
        Constructs a structured system prompt for the agent.
        
        Args:
            persona: The AgentPersona object containing bio, traits, and directives.
            memories: A list of relevant memory strings to include.
            
        Returns:
            A formatted markdown string serving as the system prompt.
        """
        
        # Format traits list
        traits_list = "\n".join([f"- {trait}" for trait in persona.voice_traits])
        
        # Format directives list
        directives_list = "\n".join([f"- {directive}" for directive in persona.directives])
        
        # Format memories list
        memories_content = "\n".join([f"- {memory}" for memory in memories]) if memories else "No relevant memories found."
        
        return f"""# WHO YOU ARE
You are {persona.name}.

## Bio
{persona.bio}

## Voice & Tone Traits
{traits_list}

# YOUR DIRECTIVES
{directives_list}

# RELEVANT MEMORIES
The following are recalled memories relevant to the current situation:
{memories_content}
"""
