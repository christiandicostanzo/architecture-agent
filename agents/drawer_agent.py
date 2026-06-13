from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable

from prompts.drawer_prompt import DRAWER_PROMPT


def create_agent(llm: BaseLanguageModel) -> Runnable:
    return DRAWER_PROMPT | llm
