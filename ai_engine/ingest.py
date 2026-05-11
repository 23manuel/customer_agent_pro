import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def run_ingestion():
    print("Reading policy...")
    loader = TextLoader("data/policy.txt", encoding='utf-8')
    documents = loader.load()

    print("Splitting text...")
    # FIXED: Larger chunks, bigger overlap. Context stays intact.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print("Generating Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 
    
    vector_store = FAISS.from_documents(chunks, embeddings)

    print("Saving FAISS index...")
    vector_store.save_local("faiss_index")
    print("Ingestion finished. Index ready.")

if __name__ == "__main__":
    run_ingestion()