from langgraph.graph import END, START, Graph
from IPython.display import Image, display
# Initialize the graph
workflow = Graph()      

def node1(input1):
    return f"Hello from: {input1}\n"

def node2(input2):
    return f"Output of Node-1: {input2} and Hello from Node-2\n"


workflow.add_node(node="Node-1", action=node1)  # Add Node-1 with action
workflow.add_node(node="Node-2", action=node2)  # Add Node-2 with action


workflow.add_edge(START, "Node-1")  # Connect START to Node-1
workflow.add_edge("Node-1", "Node-2")  # Connect Node-1 to Node-2
workflow.add_edge("Node-2", END)  # Connect Node-2 to END

basic_graph = workflow.compile()  # Compile the graph



# try:
#     display(Image(basic_graph.get_graph(xray=True).draw_mermaid_png()))
# except Exception:
#     pass
start_message = "Hello from START"

for output in basic_graph.stream(start_message ):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"'{key}':")
        print("---")
        print(value)
    print("\n~~~~~~~~\n")