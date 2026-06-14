def retrieve_docs(vector_db, query):

    docs = vector_db.similarity_search(
        query,
        k=2
    )

    return docs