# agent_service.py
# agent_service.py
 

from dotenv import load_dotenv
load_dotenv() 


from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import SystemMessage
import os



from tool import tool_ppt_to_pdf

def get_agent_executor():

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """

Use ppt_to_pdf_converter tool when needed.

Call only one tool.

Always Return in tis format:
{{
  "filename": "yourfile.pdf"
}}
         only give the single output nothing else
"""),
        ("human", "{input}"),
        SystemMessage(content="You convert file types"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    tools = [tool_ppt_to_pdf]

    agent = create_tool_calling_agent(
        llm=llm.bind_tools(tools),
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )