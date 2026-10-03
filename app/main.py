from dotenv import load_dotenv
load_dotenv()

from .graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver




MONGODB_URI = "mongodb://localhost:27017"
config = {
    "configurable": {
        "thread_id": "10"
        }
    }

def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        while True:

            # check if graph is already paused

            if graph_with_mongo.get_state(config).next:
                print("Graph is waiting for human assistance.")


            user_input = input(">")
            for event in graph_with_mongo.stream(
                {"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"
            ):
                if "messages" in event:
                    event["messages"][-1].pretty_print()

            # # check whether the graph is paused
            # state= graph_with_mongo.get_state(config)


            # if state.next:
            #     print("Graph is waiting for human assistance")
            #     print("Run: python -m app.support")


init()