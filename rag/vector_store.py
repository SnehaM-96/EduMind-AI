from langchain_community.vectorstores import FAISS

def create_vector_store(chunks, embeddings, metadata):

    vector_db = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata
    )

    return vector_db