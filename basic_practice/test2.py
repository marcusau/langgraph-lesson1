import operator
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState, StateGraph,END, START


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

workflow = StateGraph(MessagesState) # We replaced Graph() with StateGraph(MessagesState)

# MessagesState will keep on inserting messages while passing every Node
def node1(state: MessagesState):
    input1 = state['messages'][0].content # Use list index to access the content
    response = str(input1) + ", From Node-1: Hello, Human"
    return {"messages": [response]}

def node2(state: MessagesState):
    input2 = state['messages'][-1].content # To get the output of previous Node use index [-1]
    response =  str(input2) + " From Node-2, Hello, Human and Node-1"
    return {"messages": [response]}


workflow.add_node("Node-1", node1)
workflow.add_node("Node-2", node2)


workflow.add_edge(START, "Node-1")
workflow.add_edge("Node-1", "Node-2")
workflow.add_edge("Node-2", END)

graph_with_state = workflow.compile()

######################################################################

inputs =  { "messages": [ 
                {"role": "human", 
                 "content": "Hi I am Human"} ]
        }


for output in graph_with_state.stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"'{key}':  {value}")
        print("---")
       
    print("\n~~~~~~~~\n")
