from langchain_experimental.sql import SQLDatabaseChain
from langgraph.graph import MessagesState
from langchain_community.utilities import SQLDatabase
#from langchain_community.llms.cohere import Cohere
from langchain_cohere import ChatCohere
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

load_dotenv()


os.environ['COHERE_API_KEY'] = os.getenv("COHERE_API_KEY")

db_engine = create_engine("sqlite:///employees.db")



# Forcefully made return_sql=True, return_direct=True to get the generated SQL
# else, it will create and execute query internally which is sometime error prone
def generate_query(state: MessagesState):
    llm_cohere = ChatCohere(model = "command-r-plus-08-2024", max_tokens=100, temperature=0)
    sql_chain = SQLDatabaseChain.from_llm(llm_cohere, db=SQLDatabase(db_engine),  return_sql=True, return_direct=True)
    messages = state['messages']
    response = sql_chain.invoke(messages)
    return {"messages": [response['result']]}


def clean_query(state: MessagesState):
    messages = state['messages'][-1]
    corrected_query = messages.content.replace("`","").replace("sql","").replace("SQLQuery: ","")
    #print(f"Cleaned query: {corrected_query}")
    return {"messages": [corrected_query]}


# Execute the generated query and extract or formmat output as per requirement
def execute_query(state: MessagesState):
    messages = state['messages'][-1]
    sql = messages.content
    #print(f"Executing query: {sql}")
    with db_engine.begin() as connection:
        answer = connection.execute(text(sql)).fetchall()
    return {"messages": [str(answer)]}

if __name__ == "__main__":
    print(generate_query({"messages": [{"role": "human", "content": "What is the highest salary of all employees? "}]}))
