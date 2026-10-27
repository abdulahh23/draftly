from langchain.chat_models import init_chat_model   #chatbbot

llm = init_chat_model(
    model="ollama:gemma4:31b-cloud",
    temperature=0.3
)

q = input("Query: ")
response = llm.invoke(q)
print(response.text)