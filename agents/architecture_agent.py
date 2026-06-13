from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable

from prompts.architecture_prompt import ARCHITECTURE_PROMPT


def create_agent(llm: BaseLanguageModel) -> Runnable:
    return ARCHITECTURE_PROMPT | llm
