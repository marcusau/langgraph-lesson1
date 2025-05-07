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

def some_tool(state: MessagesState):
    tool_input = state['messages'][-1].content
    print(f"Tool input: {tool_input}")
    response = tool_input.upper()
    return {"messages": [response]}

def routing_logic(state: MessagesState):
    input3 = state['messages'][-1].content
    # If the input is more than 10 size, then we route to the "tool" node
    if len(input3)>80:
        return "tool"
    # Otherwise, we end the workflow
    return "__end__"

#This tool makes the input upper case


##############################################################################################

workflow = StateGraph(MessagesState)

workflow.add_node("Node-1", node1)
workflow.add_node("Node-2", node2)
workflow.add_node("tool", some_tool)


workflow.add_edge(START, "Node-1")
workflow.add_edge("Node-1", "Node-2")
# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node (The node from where we need branching). We use `Node-2`.
    source="Node-2",
    # Next, we pass in the router function that will determine next Node.
    path = routing_logic,
    # This means these are the edges taken after the `Node-2` node is called.
    path_map={
        "tool": "tool",
        "__end__": "__end__"
    }
)
workflow.add_edge("tool", END)


graph_with_state = workflow.compile()

################################################################

inputs =  {  "messages": [ {"role": "human", 
                            "content": "Hi"} ]  ##"Hi I am Human, I am from planet Earth"
         }

for output in graph_with_state.stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"'{key}': {value}")
        print("---")
    print("\n~~~~~~~~\n")