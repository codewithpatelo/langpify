"""Langpify - SDK para programación basada en agentes neuro-simbolicos."""

__version__ = "0.1.0"
__author__ = "Patricio Gerpe"
__email__ = "pj.patriciojulian@gmail.com"

# Import main classes for easy access
from .entities import LangpifyBaseAgent, LangpifyRole, LangpifyGoal
from .utils import LangpifySanitizationUtils

__all__ = [
    "LangpifyBaseAgent",
    "LangpifyRole", 
    "LangpifyGoal",
    "LangpifySanitizationUtils",
]
