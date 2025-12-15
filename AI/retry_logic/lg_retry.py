from langgraph.graph import StateGraph
from langgraph.pregel import RetryPolicy 

@graph.node(retry=RetryPolicy(retry_count=3,retry_delay=2))
def evaluate_rules(state):
    # do something
    raise Exception("API Timeout")