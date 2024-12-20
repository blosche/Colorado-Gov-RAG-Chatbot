import os

from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI
from sentence_transformers import CrossEncoder
from store import create_retriever, create_retriever_unemployment

db_user = os.getenv("DB_USER", "admin")
db_password = os.getenv("DB_PASSWORD", "admin")
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "vectordb")

CONNECTION_STRING = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
retriever = create_retriever(CONNECTION_STRING)
retriever_unemployment = create_retriever_unemployment(CONNECTION_STRING)

rephrase_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
REPHRASE_TEMPLATE = PromptTemplate.from_template(rephrase_template)


rephrase_chain = REPHRASE_TEMPLATE | ChatOpenAI(temperature=0) | StrOutputParser()


def print_context(context):
    print("Final Context that goes into the prompt:")
    print(context)
    return context


print_context_chain = RunnableLambda(lambda input_data: print_context(input_data['context']))

def rerank_documents(input_data):
    query = input_data["question"]
    docs = input_data["context"]

    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    contents = [doc.page_content for doc in docs]

    pairs = [(query, text) for text in contents]
    scores = cross_encoder.predict(pairs)

    scored_docs = zip(scores, docs)
    sorted_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)
    return [doc for _, doc in sorted_docs]

# SERVICES TEMPLATE
template = """You are a professional and friendly government chatbot trying to help connect citizens with services.

1. Summarize the user's question back to them.
2. Provide relevant services that could address the user's question, following this specific format:

**Service Name**: [Service Name]  
**Service URL**: [Service Name](Service URL)  
**Department**: [Department Name](Department URL)  

3. Add the following disclaimer at the end of your response:

 This answer was generated with the use of AI, AI can make mistakes, please verify this service through the following sources
[Colorado Services](https://co.colorado.gov/services)
[Colorado Contact Us](https://co.colorado.gov/contacts-search?field_state_agency=All&field_county=All&field_keywords=)

Please ensure that only the headers (e.g., 'Service Name', 'Service URL', 'Department') are bolded, not the actual service names 
or URLs. Make sure the service name and department name use their respective links. Use the following context to find relevant services:  
{context}

Question: {question}

"""
# UNEMPLOYMENT TEMPLATE
template_unemployment = """You are a professional and friendly government chatbot trying to answer citizens questions about unemployment related things.
 1. Summarize the user's question back to them.
 2. Answer their question about unemployment benefits, make sure not to infer anything or add anything, only go off what is in the context. 
 3. Add the following disclaimer at the end of your response:
 
 This answer was generated with the use of AI, AI can make mistakes, please verify this information through the following sources
 [Unemployment FAQ's](https://cdle.colorado.gov/unemployment/faqs)
 [Unemployment Claimant Guide](https://cdle.colorado.gov/unemployment/ui-claimant-guide)
 [Contact Unemployment](https://cdle.colorado.gov/unemployment/contact-us)
 
 Here is the context you can use to answer the question:
 {context}
 
 Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
prompt_unemployment = ChatPromptTemplate.from_template(template_unemployment)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), max_retries=5)

rerank_chain = RunnablePassthrough.assign(context=RunnableLambda(rerank_documents))
model_chain = prompt | model | StrOutputParser()
model_chain_unemployment = prompt_unemployment | model | StrOutputParser()

rag_chain = RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
rag_chain_unemployment = RunnableParallel({"context": retriever_unemployment, "question": RunnablePassthrough()})

full_chain = rephrase_chain | rag_chain | model_chain
# full_chain = rephrase_chain | rag_chain | rerank_chain | model_chain
# full_chain_unemployment = rephrase_chain | rag_chain_unemployment | model_chain_unemployment
full_chain_unemployment = rephrase_chain | rag_chain_unemployment | rerank_chain | model_chain_unemployment
