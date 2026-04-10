import os
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_aws import ChatBedrock

# Toggle between fake and real embeddings
USE_BEDROCK_EMBEDDINGS = True  # Set to True when AWS is configured
def build_retriever():
    docs = [
        Document(page_content="Leave policy: Earned leave is 24 days per year. Carry forward max 30 days."),
        Document(page_content="Sick leave: 12 days per year. Medical certificate required if >2 consecutive days."),
        Document(page_content="Work from home policy: Up to 2 days per week with manager approval."),
        Document(page_content="Travel policy: Economy class for domestic flights unless approved otherwise."),
    ]
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = splitter.split_documents(docs)

    if USE_BEDROCK_EMBEDDINGS:
        embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v2:0",
            region_name="ap-south-1",
        )
    else:
        embeddings = FakeEmbeddings(size=384)

    vs = FAISS.from_documents(chunks, embedding=embeddings)
    return vs.as_retriever(search_kwargs={"k": 2})


def format_docs(docs):
    return "\n\n".join([f"- {d.page_content}" for d in docs])

retriever = build_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer strictly using the provided context. If missing, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

# For a practical demo, we’ll simulate an LLM call with a simple function.
# Replace this with Bedrock Chat model once your tracing is working.
llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.5,
        "max_tokens": 300,
    },
)

chain = (
    {
        "question": RunnablePassthrough(),
        "context": retriever | format_docs
    }
    | prompt
    | llm
)

def ask(q: str):
    # The chain already executes the LLM and returns the response
    response = chain.invoke(q)
    # ChatBedrock returns an AIMessage object, extract the content
    return response.content if hasattr(response, 'content') else str(response)

if __name__ == "__main__":
    print(ask("How many earned leave days do we get and can we carry forward?"))
