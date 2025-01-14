# models.py
from dataclasses import dataclass

@dataclass
class WorkflowResults:
    """Data class to hold the results of the workflow."""
    OpenAI: str = ""
    Anthropic: str = ""
    xAI: str = ""
    Consensus_Analysis: str = ""
    Charts_Mindmaps: str = ""
    Analysis_Tools: str = ""
    Related_Questions: str = ""
    Meta_Analysis: str = ""