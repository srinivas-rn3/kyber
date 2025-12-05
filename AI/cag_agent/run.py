from src.graph_cag import build_graph

if __name__ == "__main__":

    customer_id = "cust_002"   # default
    rule_id = "car_rules"

    graph = build_graph()

    result = graph.invoke({
        "customer_id": customer_id,
        "rule_id": rule_id
    })

    print("\n===== FINAL DECISION =====")
    print(result['final_decision'])
