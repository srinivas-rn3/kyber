from langgraph.graph import StateGraph,END
from typing import TypedDict

class State(TypedDict):
    pizza_type:str
    order_placed:bool

def decide_pizza(state:State):
    print("Thinking about pizza")
    return{
        "pizza_type":"Margherita",
        "order_placed":False}

def order_pizza(state:State):
   pizza = state["pizza_type"]
   print(f"Ordering {pizza} pizza...")
   return{
    "pizza_type":pizza,
    "order_placed":True
   }

def celebrate(state:State):
    print(f"YAAAAYYY! {state['pizza_type']} pizza is coming!")
    return state

workflow = StateGraph(State)
workflow.add_node("Decide",decide_pizza)
workflow.add_node("Order",order_pizza)
workflow.add_node("Celebrate", celebrate)

# Connect them with arrows (edges)
workflow.set_entry_point("Decide")
workflow.add_edge("Decide","Order")
workflow.add_edge("Order", "Celebrate")
workflow.add_edge("Celebrate", END)

app = workflow.compile()

result = app.invoke({'pizza_type':'','order_placed':False})
print("\n Final result:",result)

