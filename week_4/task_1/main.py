from sentence_transformers import SentenceTransformer, util
import numpy as np

with open("corpus.txt", "r", encoding="utf-8") as file:
    corpus = [line.strip() for line in file if line.strip()]

print(f"Number of sentences: {len(corpus)}")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(corpus, convert_to_numpy=True, normalize_embeddings=True)

print(f"Embedding shape: {embeddings.shape}")

print("Embeddings saved to embeddings.npy")

def numpy_search(query, top_k=5):
    query_embedding = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    scores = embeddings @ query_embedding
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(index, corpus[index], scores[index]) for index in top_indices]

def library_search(query, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
    corpus_embeddings = util.normalize_embeddings(model.encode(corpus, convert_to_tensor=True))
    results = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)[0]
    return [(result["corpus_id"], corpus[result["corpus_id"]], result["score"]) for result in results]

queries = [
    "How can I create an API with Python?",
    "How can I store information in a relational database?",
    "How does user authentication work?",
    "How can I search text based on meaning?",
    "How can I improve application performance?"
]

for query in queries:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    numpy_results = numpy_search(query)
    print("\nNumPy Results:")
    for rank, (index, sentence, score) in enumerate(numpy_results, 1):
        print(f"{rank}. Score: {score:.4f} | Index: {index}")
        print(f"   {sentence}")

    library_results = library_search(query)
    print("\nLibrary Results:")
    for rank, (index, sentence, score) in enumerate(library_results, 1):
        print(f"{rank}. Score: {score:.4f} | Index: {index}")
        print(f"   {sentence}")

    numpy_indices = [result[0] for result in numpy_results]
    library_indices = [result[0] for result in library_results]

    print("\nSame ranking:", numpy_indices == library_indices)