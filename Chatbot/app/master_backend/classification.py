from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

classification_template = PromptTemplate.from_template(
    """You are good at classifying a question.
    Given the user question below, classify it as either being about `Services` or 'Offtopic' 'Unemployment'.

    <If the question is about unemployment, how to get unemployment benefits, or questions relating specifically to unemployment, classift it as 'Unemployment'>
    <If the question is about government services, or any things related to colorado states operations, services, and duties, classify it as 'Services'>
    <If the question is about sports, movies, opinions, or anything not related to services and government duties, classify the question as 'offtopic'>

    <question>
    {question}
    </question>

    Classification:"""
)

classification_chain = (
    classification_template
    | ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), max_retries=5)
    | StrOutputParser()
)
