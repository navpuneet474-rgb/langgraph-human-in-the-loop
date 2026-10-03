from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode, tools_condition


llm = init_chat_model(model="openai/gpt-oss-120b", model_provider="groq")

@tool
def human_assistance_tool(query:str):
    # below part act as description of this tools
    """Request assistant from a human.
    
    Use this tool when the user explicitly asks to:
    - speak with a human
    - contact a support agent
    - connect with someone
    - get help from a person
    - escalate an issue to human support

    Do not provide generic troubleshooting instead when the user explicitly
    requests human.
    """

    human_response = interrupt({"query": query}) # Graph will exit out after saving the data in db
    return human_response["data"] # resume with the data

tools= [human_assistance_tool]
llm_with_tools = llm.bind_tools(tools=tools)

class State(TypedDict):
    # update the message list
    messages: Annotated[list, add_messages]



def chatbot(state: State):
    message = state.get("messages")

    response = llm_with_tools.invoke(message)
    return {"messages" : [response]}

graph_builder = StateGraph(State)

# add node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))


# add edge
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)


graph_builder.add_edge("tools", "chatbot")



# creae a new graph with given checkpointer
def create_chat_graph(checkpointer=None):
    return graph_builder.compile(checkpointer=checkpointer)

