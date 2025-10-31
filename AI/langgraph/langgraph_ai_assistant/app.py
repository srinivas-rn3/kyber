from graph.main_graph import build_graph

def main():
    app = build_graph()
    app.invoke({"history":[]})

if __name__ == "__main__":
    main()
