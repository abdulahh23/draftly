#agent-2.py is with database (permanent memory) with sqlite


import os
import sqlite3 #db connection
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv(".env")

llm = init_chat_model(
    model=os.getenv("DRAFTLY_LLM_MODEL"),
    api_key=os.getenv("DRAFTLY_API_KEY"),
    thinking_level="medium",
    max_retries=3,
)

SYSTEM = """
You are Draftly, a helpful AI email draft agent.
"""

# Write a clear, concise email with a Subject line, greeting, body, and sign-off.
# Match the tone to the request. Use placeholders like [Name] for missing details.
# Output only the email.

db_conn = sqlite3.connect("memory.db", check_same_thread=False)
sqlite_checkpoint = SqliteSaver(db_conn)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM,
    # response_format=
    # checkpointer=
    # store=
    # middleware=
    checkpointer=sqlite_checkpoint
)

thread_id = input("Conversation name: ")
thread_config = {"configurable": {"thread_id": thread_id}}

while True:

    q = input("Enter email draft idea: ")

    if q.lower() in ("quit", "exit", "bye"):
        break

    result = agent.invoke(
        {"messages": [{"role": "user", "content": q}]},
        config=thread_config
    )

    print(result["messages"][-1].text)