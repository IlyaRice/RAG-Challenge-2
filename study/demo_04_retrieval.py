# study/demo_04_retrieval.py

import sys
import os
import numpy as np

# --- Configuration ---
# Attempt to use sentence-transformers for more realistic embeddings.
# If this script is run in an environment where sentence-transformers is not installed,
# it will fall back to dummy embeddings.
# To install: pip install sentence-transformers scikit-learn numpy
USE_SENTENCE_TRANSFORMERS = True
MODEL_NAME = 'all-MiniLM-L6-v2' # A small, fast model

# Add the src directory to the Python path for consistency, though not strictly needed for this demo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Embedding Generation ---
# We aim to illustrate the concept. src/retrieval.py uses OpenAI models (e.g., text-embedding-3-large)
# which require API keys and more setup. For this demo, we'll use a local sentence transformer
# or a dummy function if sentence-transformers is unavailable.

def get_embeddings_sentence_transformer(texts: list[str]) -> np.ndarray:
    """
    Generates embeddings using a sentence-transformers model.
    """
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
        embeddings = model.encode(texts)
        return np.array(embeddings)
    except ImportError:
        print("SentenceTransformers library not found. Falling back to dummy embeddings.")
        print("Please install it via 'pip install sentence-transformers' for better results.")
        global USE_SENTENCE_TRANSFORMERS # Allow modification of global flag
        USE_SENTENCE_TRANSFORMERS = False
        return get_dummy_embeddings(texts) # Fallback
    except Exception as e:
        print(f"Error loading SentenceTransformer model ({MODEL_NAME}): {e}")
        print("Falling back to dummy embeddings.")
        global USE_SENTENCE_TRANSFORMERS
        USE_SENTENCE_TRANSFORMERS = False
        return get_dummy_embeddings(texts) # Fallback

def get_dummy_embeddings(texts: list[str], vector_size: int = 10) -> np.ndarray:
    """
    Generates dummy embeddings.
    This is a placeholder for real embedding models like those in src/retrieval.py.
    It creates a fixed-size vector based on the hash of the text.
    """
    print("Using DUMMY embedding function.")
    embeddings = []
    for text in texts:
        # Simple hash-based vector, not semantically meaningful
        hash_val = hash(text)
        embedding = np.array([float(hash_val % (i + 100)) for i in range(vector_size)])
        # Normalize to have some consistency, though still not semantic
        norm = np.linalg.norm(embedding)
        if norm == 0:
            norm = 1
        embeddings.append(embedding / norm)
    return np.array(embeddings)

def get_embeddings(texts: list[str]) -> np.ndarray:
    """Wrapper to select embedding function based on availability."""
    if USE_SENTENCE_TRANSFORMERS:
        return get_embeddings_sentence_transformer(texts)
    else:
        return get_dummy_embeddings(texts)

# --- Similarity Search ---
def cosine_similarity_search(query_embedding: np.ndarray, chunk_embeddings: np.ndarray, top_n: int = 2) -> list[tuple[int, float]]:
    """
    Performs cosine similarity search between query and chunk embeddings.
    Returns a list of (chunk_index, similarity_score) for the top_n results.
    """
    try:
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        print("scikit-learn not found. Cosine similarity search cannot be performed.")
        print("Please install it via 'pip install scikit-learn'")
        return []

    # query_embedding is 1D, needs to be 2D for cosine_similarity function
    similarities = cosine_similarity(query_embedding.reshape(1, -1), chunk_embeddings)
    
    # Squeeze similarities to 1D array and get sorted indices
    sorted_indices = np.argsort(similarities[0])[::-1] # Descending order
    
    top_results = []
    for i in range(min(top_n, len(sorted_indices))):
        idx = sorted_indices[i]
        score = similarities[0][idx]
        top_results.append((idx, score))
        
    return top_results

def main():
    print("--- Demo: Conceptual Retrieval using Vector Similarity ---")
    print("This script demonstrates a simplified retrieval process.")
    print(f"It attempts to use SentenceTransformers ('{MODEL_NAME}'). If unavailable or fails, it uses dummy embeddings.")
    print("The actual project implementation in src/retrieval.py uses more advanced models and infrastructure.\n")

    # --- 1. Prepare Sample Data ---
    # Using a small, predefined list of text chunks for simplicity.
    # Alternatively, one could parse a PDF and chunk it as in demo_03_text_splitting.py.
    sample_chunks = [
        "The company reported a significant increase in revenue for the last quarter.",
        "Environmental sustainability initiatives are a key focus for future growth.",
        "New product development is progressing on schedule, with a launch expected next year.",
        "Challenges in the supply chain have impacted production timelines.",
        "Our financial performance exceeded expectations despite market volatility."
    ]
    print("Sample Text Chunks:")
    for i, chunk in enumerate(sample_chunks):
        print(f"  Chunk {i}: {chunk}")

    # --- 2. Embedding Generation ---
    print("\nGenerating embeddings for sample chunks...")
    chunk_embeddings = get_embeddings(sample_chunks)
    
    if chunk_embeddings.size == 0: # Could happen if scikit-learn is missing for dummy fallback too
        print("Could not generate embeddings. Exiting.")
        return

    # print("\nChunk Embeddings (first embedding, first 5 dims):")
    # if chunk_embeddings.any():
    # print(f"  {chunk_embeddings[0][:5]}...") # Show a snippet

    # --- 3. Similarity Search ---
    sample_query = "What were the company's financial results?"
    print(f"\nSample Query: \"{sample_query}\"")

    print("Generating embedding for the query...")
    query_embedding = get_embeddings([sample_query])[0] # Get the first (and only) embedding

    if query_embedding.size == 0:
        print("Could not generate query embedding. Exiting.")
        return

    print("\nPerforming similarity search...")
    # Retrieve top 2 most similar chunks
    retrieved_items = cosine_similarity_search(query_embedding, chunk_embeddings, top_n=2)

    # --- 4. Output ---
    print("\n--- Retrieval Results ---")
    if not retrieved_items:
        print("No items retrieved. This might be due to missing scikit-learn or other errors.")
    else:
        print(f"Query: \"{sample_query}\"")
        print("\nTop Retrieved Chunks:")
        for idx, score in retrieved_items:
            print(f"  Similarity Score: {score:.4f}")
            print(f"  Chunk {idx}: \"{sample_chunks[idx]}\"\n")
    
    print("--- End of Demo ---")
    print("Note: The similarity scores and retrieved chunks will be more meaningful if")
    print("SentenceTransformers was used. Dummy embeddings provide placeholder results.")
    print("Refer to src/retrieval.py for the project's actual retrieval mechanisms,")
    print("which involve sophisticated models and vector databases like FAISS.")


if __name__ == "__main__":
    # This is a conceptual demo. For actual embedding and retrieval,
    # the project uses tools like OpenAI, FAISS, and specific model configurations
    # as seen in src/ingestion.py and src/retrieval.py.
    
    # Attempt to install libraries if needed (conceptual, won't run in this isolated step)
    # print("To ensure all features work, you might need to install: pip install sentence-transformers scikit-learn numpy")
    main()
