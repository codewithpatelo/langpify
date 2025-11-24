from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph


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


class LangpifyAgentType(Enum):
    """Inspired in the Viable System Model from Management Cybernetics"""

    OPS_AGENT = "OpsAgent"
    COORDINATOR_AGENT = "CoordinatorAgent"
    CONTROL_AGENT = "ControlAgent"
    INTEL_AGENT = "IntelAgent"
    STRAT_AGENT = "StratAgent"


class Framework(str, Enum):
    """Supported AI Frameworks."""

    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    LLAMAINDEX = "llamaindex"


class LangpifyStatus(str, Enum):
    """Agent lifecycle status inspired on FIPA and ACP specifications.

    References:
    - http://fipa.org/specs/fipa00023/SC00023K.html (5.1)
    - https://www.researchgate.net/figure/Agent-life-cycle-as-defined-by-FIPA_fig1_332959107
    - https://agentcommunicationprotocol.dev/core-concepts/agent-run-lifecycle
    """

    ACTIVE = "active"  # Agent is sensoring stimuli and computing needs  - Recommended visual feedback:  Glowing Green
    INITIATED = "initiated"  # Agent has been created but not fully activated - Recommended visual feedback:  Smooth Glowing Green
    SUSPENDED = "suspended"  # Agent is temporarily paused - Recommended visual feedback:  Static Grey
    WORKING = "working"  # Agent is actively performing tasks - Recommended visual feedback:  Flashing Green
    DELETED = "deleted"  # Agent has been terminated - Recommended visual feedback:  Static Black
    WAITING = "waiting"  # Agent is waiting for an event or resource - Recommended visual feedback:  Flashing Yellow
    ERROR = "error"  # Agent has encountered an error - Recommended visual feedback: Glowing Red


class LangpifyDynamicPrompt(BaseModel):
    role: Optional[str] = None
    goal: Optional[str] = None
    instructions: Optional[str] = None
    extras: Optional[str] = None
    examples: Optional[str] = None
    output: Optional[str] = None
    guardrails: Optional[str] = None


class AISettings(TypedDict):
    """Settings for the AI framework
    Langpify works as a meta-framework, allowing higher-level generalization
    in a framework-agnostic way.

    Note that in productive environments default values would be set by environment variables
    """

    _framework: Optional[Framework]
    # Another possible params are _embedding_model,_vector_db: and a global default settings for _llm


class LangpifyAuthorizations(TypedDict, total=False):
    """Basic schema for authorizations and AI governance
    with BYOK approach (Bring Your Own Key)"""

    access_token: Optional[str]
    organizations: Optional[List[str]]
    applications: Optional[List[str]]
    projects: Optional[List[str]]
    roles: Optional[List[str]]
    permissions: Optional[List[str]]
    risk_tier: Optional[str]
    compliance_docs_url: Optional[List[str]]
    allowed_tools: Optional[List[str]]
    allowed_models: Optional[List[str]]


class LangpifyGuardrails(TypedDict):
    prompt: str


class LangpifySafety(TypedDict):
    guardrails: LangpifyGuardrails


class LangpifyTemplateLLM(TypedDict, total=False):
    provider: str
    model: str
    temperature: Optional[float]
    max_tokens: Optional[int]


class LangpifyTemplateLLMGateway(TypedDict):
    primary_model: LangpifyTemplateLLM
    secondary_model: Optional[LangpifyTemplateLLM]


class LangpifyTemplateLanguage(TypedDict):
    default: str
    llm: LangpifyTemplateLLMGateway


class LangpifyLLM(TypedDict, total=False):
    """Represents a language model instance for an agent.

    This class defines the language model that an agent will use for communication,
    including the provider (e.g., OpenAI, Anthropic), model name, and optionally
    the actual model instance if already instantiated.
    """

    model_provider: str  # Provider of the language model (e.g., 'openai', 'anthropic', 'local')
    model_name: str  # Name of the specific model (e.g., 'gpt-4', 'claude-3')
    model: Optional[Any]  # The actual model instance, if already instantiated


class LangpifyLanguage(TypedDict):
    """Language configuration for an agent including LLM settings"""

    default: str
    llm: LangpifyLLM


class LangpifyTemplateWorkflow(TypedDict):
    type: str


class LangpifyTemplateGoal(TypedDict):
    name: str
    prompt: str
    prompt_extras: str


class LangpifyExecutionProtocol(TypedDict):
    prompt: str
    prompt_examples: str
    prompt_output: str


class LangpifyTemplatePlanning(TypedDict):
    workflow: LangpifyTemplateWorkflow
    excecution_protocol: LangpifyExecutionProtocol
    goal: LangpifyTemplateGoal


class LangpifyWorkflow(TypedDict):
    """This is just examplary
    LangpifyWorkflow is agnostic to any framework so its value type would depend on the framework set
    """

    graph: StateGraph


class LangpifyPlanning(TypedDict):
    workflow: LangpifyWorkflow
    excecution_protocol: LangpifyExecutionProtocol
    goal: LangpifyGoal
