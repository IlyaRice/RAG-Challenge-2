# study/demo_06_reranking.py

import sys
import os

# Add the src directory to the Python path for consistency
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 1. Define Sample Inputs ---
SAMPLE_QUESTION = "Tell me about the company's sustainability efforts and environmental impact."

# Sample chunks with varying (implied) relevance and initial scores
# Scores are dummy "initial retrieval scores" (e.g., from a vector search, higher is better here)
# Each item: (text_chunk, initial_score)
SAMPLED_RETRIEVED_CHUNKS = [
    ("The company launched a new line of eco-friendly packaging for all its products in Q4.", 0.85),
    ("Financial results for the fiscal year showed a 10% increase in net profit.", 0.60), # Less relevant
    ("Our annual report details significant investments in renewable energy sources, reducing our carbon footprint by 20% last year.", 0.90), # Highly relevant
    ("Employee training programs were updated to include new safety protocols.", 0.55), # Irrelevant
    ("We are committed to water conservation and have implemented recycling programs across our facilities.", 0.80) # Relevant
]

# --- 2. Reranking Logic (Simplified/Conceptual) ---
# src/reranking.py uses actual LLMs (OpenAI, Jina) to get new relevance scores.
# This demo mocks that logic.

def mock_rerank_logic(question: str, chunks_with_initial_scores: list[tuple[str, float]]) -> list[tuple[str, float, float, float]]:
    """
    Simulates an LLM-based reranker.
    - Assigns a mock "LLM relevance score".
    - Calculates a "combined score".
    Returns a list of tuples: (text_chunk, initial_score, llm_score, combined_score)
    """
    print("\n--- Running Mock Reranking Logic ---")
    reranked_results = []
    
    # Example keywords to boost scores for this specific question
    positive_keywords = ["sustainability", "environmental", "eco-friendly", "renewable", "carbon footprint", "conservation", "recycling"]

    for i, (chunk_text, initial_score) in enumerate(chunks_with_initial_scores):
        mock_llm_score = 0.5 # Default LLM score
        
        # Simplified logic: boost LLM score if keywords are present
        if any(keyword in chunk_text.lower() for keyword in positive_keywords):
            mock_llm_score += 0.4 # Boost for relevant keywords
            if "carbon footprint" in chunk_text.lower() or "renewable energy" in chunk_text.lower():
                 mock_llm_score += 0.1 # Extra boost for very specific terms
        
        # Ensure score is capped at 1.0
        mock_llm_score = min(mock_llm_score, 1.0)

        # In src/reranking.py, LLM_WEIGHT and VECTOR_WEIGHT are used.
        # Let's use a simple weighting: 60% LLM, 40% initial score.
        llm_weight = 0.6
        initial_weight = 0.4
        combined_score = round((llm_weight * mock_llm_score) + (initial_weight * initial_score), 4)
        
        print(f"  Chunk {i+1}: Initial Score={initial_score:.2f}, Mock LLM Score={mock_llm_score:.2f}, Combined Score={combined_score:.4f}")
        reranked_results.append((chunk_text, initial_score, mock_llm_score, combined_score))
        
    # Sort by the new combined_score in descending order
    reranked_results.sort(key=lambda x: x[3], reverse=True)
    
    print("--- Mock Reranking Complete ---")
    return reranked_results

def main():
    print("--- Demo: Conceptual Reranking of Retrieved Chunks ---")
    print("This script demonstrates a simplified reranking process.")
    print("The actual project implementation in src/reranking.py uses LLMs to obtain more nuanced relevance scores.\n")

    # --- Original Question and Initial Retrieval ---
    print("1. Original User Question:")
    print(f"   \"{SAMPLE_QUESTION}\"\n")

    print("2. Initially Retrieved Chunks (with initial scores):")
    # Sort initially by score for a clear "before" picture, though vector DBs don't always guarantee perfect order for diverse results.
    # For this demo, we'll just show them as defined, then sort after reranking.
    initial_ordered_chunks = sorted(SAMPLED_RETRIEVED_CHUNKS, key=lambda x: x[1], reverse=True)
    for i, (text, score) in enumerate(initial_ordered_chunks):
        print(f"   Rank {i+1} (Score: {score:.2f}): \"{text}\"")

    # --- Apply Mock Reranking ---
    # The mock_rerank_logic function will print its internal reasoning for scores.
    reranked_chunks_with_scores = mock_rerank_logic(SAMPLE_QUESTION, SAMPLED_RETRIEVED_CHUNKS)

    # --- Output Reranked Results ---
    print("\n3. Chunks After Mock Reranking (ordered by new combined scores):")
    for i, (text, initial_s, llm_s, combined_s) in enumerate(reranked_chunks_with_scores):
        print(f"   New Rank {i+1} (Combined Score: {combined_s:.4f}, Initial: {initial_s:.2f}, LLM: {llm_s:.2f}): \"{text}\"")

    # --- Explanation of Reranking Benefit ---
    print("\n4. Why is Reranking Beneficial?")
    print("   Reranking helps to refine the initially retrieved set of text chunks.")
    print("   Initial retrieval (e.g., from vector search) is good at finding semantically similar chunks,")
    print("   but might not always capture the true relevance or specific nuances of the user's query perfectly.")
    print("   A more sophisticated reranking step (often using a powerful LLM, as in src/reranking.py)")
    print("   can re-evaluate the chunks against the query, leading to a better ordered and more relevant")
    print("   set of context to be passed to the final LLM for answer generation.")
    print("   This improves the quality and accuracy of the final answer.")
    
    print("\n--- End of Demo ---")

if __name__ == "__main__":
    main()
