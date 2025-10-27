from langgraph.graph import  StateGraph,END
from typing import TypedDict

# 1.#Define State
class State(TypedDict):
    query:str
    response:str

# 2. Define Nodes
def processs_query(state:State):
    query = state['query']
    response = f"Porcesssed: {query.upper()}"
    return {"query":query,"response":response}

#3. Build Graph
workflow = StateGraph(State)

# Adde Nodes
workflow.add_node("Process",processs_query)

# Set entry point
workflow.set_entry_point("Process")

# Add edge to end
workflow.add_edge("Process", END)

# Comile
app = workflow.compile()

# Run it

result = app.invoke({"query":"Hello world","response":""}) 
print(result)
print("Response:",result["response"])  