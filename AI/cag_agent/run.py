from src.graph_cag import build_graph
import json
import os

if __name__ == "__main__":
    graph = build_graph()

    customer_id = input("Enter customer ID (e.g., cust_001): ")

    try:
        # Load customer file manually to see their policy types
        base_dir = os.path.dirname(os.path.abspath(__file__))
        customer_path = os.path.join(base_dir, "data", "customers", f"{customer_id}.json")

        with open(customer_path) as f:
            customer_data = json.load(f)

        policy_types = customer_data.get("policy_types", [])

        if not policy_types:
            print("\n❌ This customer has no active policies.")
            exit()

        print(f"\nCustomer has policies: {policy_types}")

        # Evaluate each policy separately
        for p in policy_types:
            print("\n----------------------------------")
            print(f"Evaluating {p.upper()} POLICY...")
            print("----------------------------------")

            result = graph.invoke({
                "customer_id": customer_id,
                "policy_type_override": p   # tell graph which product to use
            })

            print(result["final_decision"])

    except ValueError as e:
        print("\n" + str(e))
    except Exception:
        print("\n❌ Something went wrong.")
