from query.retriever import get_retriever

def run_query(q):
    retriever = get_retriever()
    docs = retriever.invoke(q)   # NEW METHOD

    print("\n🔍 Top Results:\n")
    for i, d in enumerate(docs):
        print(f"{i+1}. {d.page_content[:200]}...\n" + "-" * 50)

if __name__ == "__main__":
    query = input("Enter your query: ")
    run_query(query)
