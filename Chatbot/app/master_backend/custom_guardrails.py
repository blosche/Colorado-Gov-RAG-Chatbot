from classification import classification_chain
from langchain_core.runnables import RunnableLambda, RunnableParallel
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from retrieval import full_chain, full_chain_unemployment
from sql_queries import sql_chain

config = RailsConfig.from_path("./config")
guardrails = RunnableRails(config, input_key="question")


def route(info):
    if "services" in info["topic"].lower():
        return full_chain  #retrieval
    if "unemployment" in info["topic"].lower():
        return full_chain_unemployment
    else:
        return 'Please reword your question to be about a general service we may offer, such as "How can I renew my driver\'s license?"'


full_chain_with_classification = RunnableParallel(
    {
        "topic": classification_chain, #classification 
        "question": lambda x: x["question"],
        "chat_history": lambda x: x["chat_history"],
    }
) | RunnableLambda(route)

if __name__ == "__main__":

    print(
        full_chain_with_classification.invoke(
            {
                "question": "Where do i renew my driver's license?",
                "chat_history": [],
            }
        )
    )
