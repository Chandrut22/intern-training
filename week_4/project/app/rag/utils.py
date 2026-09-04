def format_docs(docs):
    # print(len(docs))
    # print(docs)
    return "\n\n".join(
        doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in docs
    )





def format_docs(docs):
    return "\n\n".join(
        doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in docs
    )

