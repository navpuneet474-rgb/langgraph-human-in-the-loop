from dotenv import load_dotenv
load_dotenv()

from .graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import Command



MONGODB_URI = "mongodb://localhost:27017"
config = {
    "configurable": {
        "thread_id": "10"
        }
    }

def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        state =graph_with_mongo.get_state(config=config)
        for message in state.values['messages']:
            message.pretty_print()

        last_message= state.values['messages'][-1]
        tools_call = last_message.tool_calls

        for call in tools_call:


            if call["name"] == "human_assistance_tool":
                user_query = call["args"].get("query")

        print("user is trying to ask:", user_query)

        ans = input("Resolution>")
        resume_command = Command(resume={"data": ans})


        for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()
        
init()