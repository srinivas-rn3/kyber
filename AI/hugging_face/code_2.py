from transformers import pipeline

summarizer  = pipeline("summarization",framework="pt")
text = """
LangChain is a framework that simplifies building applications with large language models.
It provides abstractions for chains, memory, and agents, and supports integration with multiple LLM providers.
"""
print(summarizer(text,max_length=40,min_length=10,do_sample=False))