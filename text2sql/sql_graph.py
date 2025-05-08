from langgraph.graph import END, StateGraph, START,MessagesState
from text2sql.sql_tools import generate_query, clean_query, execute_query
 
workflow = StateGraph(MessagesState)

workflow.add_node("Query_Generator", generate_query)
workflow.add_node("Query_Cleaner", clean_query)
workflow.add_node("Query_Executor", execute_query)

workflow.add_edge(START, "Query_Generator")
workflow.add_edge("Query_Generator", "Query_Cleaner")
workflow.add_edge("Query_Cleaner", "Query_Executor")
workflow.add_edge("Query_Executor", END)

graph = workflow.compile()

########################################################################################################
question =  "Provide name, email and salary of employees joined before 2021. first Name and last name should be concatinated with space and in uppercase"

#"Provide the average salary of each department_id. Answer should be in single word or number" 

#"What is the department number of the highest paid employee and what is his/her name? Answer should be in single word or number "
inputs =  { "messages": [{"role": "human", "content": question} ] }

for output in graph.stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("---")
        print(value)
    print("\n---\n")