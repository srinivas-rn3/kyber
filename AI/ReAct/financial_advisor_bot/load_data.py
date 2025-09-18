import pandas as pd
from langchain.schema import Document

def load_expenses(file_path: str):
    df = pd.read_csv(file_path)
    docs = []
    for _, row in df.iterrows():
        text = f"Date:{row['Date']},Category:{row['Category']},Amount:{row['Amount']},Description:{row['Description']}"
        docs.append(Document(page_content=text))
    return docs 



