#embeddings + FAISS
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import config

# 1. Load KB text
with open(config.KB_FILE,"r",encoding="utf8") as f:
    kb_text = f.read()


# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP,
) 
docs = [Document(page_content=chunk) for chunk in splitter.split_text(kb_text)]

# 3. Create embeddings
embedding = BedrockEmbeddings(
    model_id=config.EMBEDDING_MODEL,
    region_name=config.REGION  # Specify your AWS region
)

# 4. Build FAISS vector DB
db = FAISS.from_documents(docs,embedding)

# 5. Save
db.save_local(config.FAISS_INDEX)
print("KB Ingested into FAISS")