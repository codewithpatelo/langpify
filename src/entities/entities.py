from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union


class LangpifyEvent(TypedDict):
    type: str
    source: str  # Agent ID that emitted the event
    timestamp: float
    data: Dict[str, Any]  # Event payload


class LangpifyRole(TypedDict):
    name: str
    content: str


class LangpifyGoal(TypedDict):
    name: str
    content: str


class LangpifyAgentState(ABC):
    """
    Clase abstracta
    Represents the agent's state, which can be generalized to different frameworks:
    - For standard use: Basic key-value state with utterance and response
    - For langgraph: Can be used as a base for StateGraph nodes

    When using with langgraph, this can be used directly with StateGraph.
    See: https://deepwiki.com/langchain-ai/langgraphjs/2.1-stategraph
    """


class LangpifyConfig(TypedDict):
    framework: Literal["langchain", "langgraph", "llamaindex"]


class LangpifyStatus(str, Enum):
    """Agent lifecycle status based on FIPA specifications.

    References:
    - http://fipa.org/specs/fipa00023/SC00023K.html (5.1)
    - https://www.researchgate.net/figure/Agent-life-cycle-as-defined-by-FIPA_fig1_332959107
    """

    ACTIVE = "active"  # Agent is actively performing tasks
    INITIATED = "initiated"  # Agent has been created but not fully activated
    SUSPENDED = "suspended"  # Agent is temporarily paused
    DELETED = "deleted"  # Agent has been terminated
    WAITING = "waiting"  # Agent is waiting for an event or resource


class LangpifyLanguage(TypedDict, total=False):
    """Represents a language model configuration for an agent.

    This class defines the language model that an agent will use for communication,
    including the provider (e.g., OpenAI, Anthropic), model name, and optionally
    the actual model instance if already instantiated.
    """

    model_provider: (
        str  # Provider of the language model (e.g., 'openai', 'anthropic', 'local')
    )
    model_name: str  # Name of the specific model (e.g., 'gpt-4', 'claude-3')
    model: Optional[Any]  # The actual model instance, if already instantiated
