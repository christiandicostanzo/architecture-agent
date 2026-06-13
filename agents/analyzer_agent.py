from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable

from prompts.analyzer_prompt import ANALYZER_PROMPT


def create_agent(llm: BaseLanguageModel) -> Runnable:
    return ANALYZER_PROMPT | llm
