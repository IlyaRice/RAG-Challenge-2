# study/demo_08_mini_pipeline.py

import sys
import os
import json # For pretty printing if needed, though mostly for consistency

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports from project/external libraries (simplified for demo)
from src.pdf_parsing import DocumentParser, Pipeline # For model download and parsing
from langchain.text_splitter import RecursiveCharacterTextSplitter # For text splitting

# --- Configuration & Sample Data ---
SAMPLE_PDF_PATH = "data/test_set/pdf_reports/194000c9109c6fa628f1fed33b44ae4c2b8365f4.pdf"
SAMPLE_QUESTION = "What are the main activities and business operations of the company?"
# For simulated retrieval, how many of the first chunks to pick
NUM_CHUNKS_TO_SIMULATE_RETRIEVAL = 2 

# --- Helper Functions (Simplified versions from previous demos) ---

def parse_pdf_and_concatenate_text(pdf_path: str) -> str:
    """
    Simplified PDF parsing: loads a PDF and concatenates text from all pages.
    Corresponds to parts of demo_01_pdf_parsing.py.
    """
    print(f"\n--- Step 2: Parsing PDF: {pdf_path} ---")
    if not os.path.exists(pdf_path):
        print(f"Error: Sample PDF file not found at {pdf_path}")
        return ""
    
    try:
        parser = DocumentParser() # Initializes models
        document = parser.parse(pdf_path)
    except Exception as e:
        print(f"Error during PDF parsing: {e}")
        return ""

    if not document.pages:
        print("Document has no pages or pages could not be parsed.")
        return ""

    print(f"Successfully parsed document. Number of pages: {len(document.pages)}")
    
    full_text_content = []
    for i, page in enumerate(document.pages):
        page_text = ""
        if hasattr(page, 'text_content') and page.text_content:
            page_text = page.text_content
        elif hasattr(page, 'text_elements') and page.text_elements:
            page_text = " ".join([elem.text for elem in page.text_elements if hasattr(elem, 'text')])
        elif hasattr(page, 'text_blocks') and page.text_blocks:
            page_text = " ".join([block.text for block in page.text_blocks if hasattr(block, 'text')])
        
        if page_text:
            full_text_content.append(page_text)
            
    concatenated_text = "\n\n".join(full_text_content)
    print(f"Concatenated text from all pages. Total length: {len(concatenated_text)} characters.")
    return concatenated_text

def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> list[str]:
    """
    Simplified text splitting.
    Corresponds to demo_03_text_splitting.py.
    """
    print("\n--- Step 3: Splitting Text into Chunks ---")
    if not text:
        print("No text to split.")
        return []
        
    try:
        # Using basic RecursiveCharacterTextSplitter for simplicity in this demo
        # instead of tiktoken-based one from demo_03 to avoid tiktoken dependency here.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len, # Standard length function
        )
        chunks = text_splitter.split_text(text)
        print(f"Split text into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        print(f"Error during text splitting: {e}")
        return []

def simulate_retrieval(chunks: list[str], num_to_select: int) -> list[str]:
    """
    Simplified/Simulated Retrieval.
    Corresponds conceptually to demo_04_retrieval.py, but heavily simplified.
    Instead of embedding and similarity search, just selects the first N chunks.
    """
    print("\n--- Step 4: Retrieving Relevant Chunks (Simulated) ---")
    if not chunks:
        print("No chunks available to retrieve from.")
        return []
    
    retrieved = chunks[:num_to_select]
    print(f"Selected the first {len(retrieved)} chunk(s) as 'retrieved' context (SIMULATION).")
    print("NOTE: This is a simplification. Real retrieval involves embedding chunks and the query,")
    print("      and finding the most similar chunks (see src/retrieval.py or demo_04_retrieval.py).")
    return retrieved

def format_simplified_prompt_for_llm(question: str, context_chunks: list[str]) -> str:
    """
    Simplified prompt formatting.
    Corresponds to demo_05_llm_interaction.py.
    """
    print("\n--- Step 5a: Formatting Prompt for LLM ---")
    context_str = "\n\n".join(context_chunks) # Join selected chunks
    
    prompt = f"""
Context from the document:
---
{context_str}
---

Question: {question}

Based *only* on the context provided above, please answer the question.
If the answer is not found in the context, state "Answer not found in context."

Answer:
"""
    print("Prompt formatted.")
    return prompt

def mock_llm_interaction(prompt: str) -> str:
    """
    Mocked LLM call.
    Corresponds to demo_05_llm_interaction.py.
    """
    print("\n--- Step 5b: Sending Prompt to Mock LLM ---")
    print("Formatted Prompt (being sent to Mock LLM):\n")
    print(prompt)
    print("-" * 30) # Separator
    
    # Hardcoded response based on the sample question and likely content of early chunks
    # This simulates what an LLM might generate.
    mocked_answer = "Based on the provided context, the company appears to be involved in [simulated activity, e.g., resource extraction and processing], with operations including [simulated operation, e.g., mining and refining products]. The company also focuses on [simulated focus, e.g., sustainable practices and community engagement]. (This is a MOCKED LLM response)."
    
    print("\nMock LLM has 'processed' the prompt.")
    return mocked_answer

# --- Main Mini-Pipeline Script ---
def main():
    print("--- Starting Demo: Mini End-to-End RAG Pipeline (Conceptual) ---")
    print("This script shows a simplified flow connecting various stages of an RAG pipeline.")
    print("Many steps are simplified or mocked for clarity. Refer to `src/` for full implementations.\n")

    # --- Step 1: Model Download (from Demo 1) ---
    # This ensures that any models DocumentParser might need are pre-downloaded.
    print("--- Step 1: Ensuring Docling Models are Available ---")
    try:
        Pipeline.download_docling_models()
        print("Docling model check/download initiated successfully (if needed).\n")
    except Exception as e:
        print(f"Error during Docling model download: {e}")
        print("Continuing, but parsing might fail if models are missing.\n")

    # --- Step 2: PDF Parsing (Simplified from Demo 1) ---
    concatenated_text = parse_pdf_and_concatenate_text(SAMPLE_PDF_PATH)
    if not concatenated_text:
        print("Failed to parse PDF or extract text. Exiting mini-pipeline.")
        return

    # --- Step 3: Text Splitting (Simplified from Demo 3) ---
    text_chunks = split_text_into_chunks(concatenated_text)
    if not text_chunks:
        print("Failed to split text into chunks. Exiting mini-pipeline.")
        return

    # --- Step 4: Retrieval (Simulated, inspired by Demo 4) ---
    # Using the predefined SAMPLE_QUESTION
    print(f"\nSample User Question: \"{SAMPLE_QUESTION}\"")
    retrieved_context_chunks = simulate_retrieval(text_chunks, NUM_CHUNKS_TO_SIMULATE_RETRIEVAL)
    if not retrieved_context_chunks:
        print("No context chunks retrieved (simulated). Exiting mini-pipeline.")
        return
        
    print("\nSimulated Retrieved Context Chunks:")
    for i, chunk in enumerate(retrieved_context_chunks):
        print(f"  Chunk {i+1}: \"{chunk[:150]}...\"") # Print snippet

    # --- Step 5: LLM Interaction (Mocked, from Demo 5) ---
    # Step 5a: Format prompt
    llm_prompt = format_simplified_prompt_for_llm(SAMPLE_QUESTION, retrieved_context_chunks)
    
    # Step 5b: Call mock LLM
    final_mock_answer = mock_llm_interaction(llm_prompt)

    # --- Step 6: Output Final (Mocked) Answer ---
    print("\n--- Step 6: Final (Mocked) Answer from LLM ---")
    print(f"Mock LLM's Answer: \"{final_mock_answer}\"")

    # --- Step 7: Summary of Demonstration ---
    print("\n--- Mini-Pipeline Demonstration Summary ---")
    print("This script demonstrated a conceptual end-to-end RAG flow:")
    print("1. Ensured models were available (conceptual model download).")
    print("2. Parsed a PDF to extract and concatenate its text content.")
    print("3. Split the concatenated text into smaller chunks.")
    print(f"4. Simulated retrieval: A sample question ('{SAMPLE_QUESTION}') was posed, and the first {NUM_CHUNKS_TO_SIMULATE_RETRIEVAL} chunk(s) were selected as context (actual retrieval is more complex).")
    print("5. Formatted a prompt combining the question and the 'retrieved' context.")
    print("6. Sent this prompt to a 'mock' LLM, which returned a hardcoded answer.")
    print("\nThis provides a bird's-eye view of how different components (parsing, splitting, retrieval, generation)")
    print("connect in a RAG system. Each step is significantly more complex in the full project (see `src/` files).")
    print("For instance, `src/pipeline.py` and `main.py` orchestrate these steps with more robust error handling,")
    print("advanced configurations, actual retrieval using vector databases, and real LLM API calls.")
    print("--- End of Demo ---")

if __name__ == "__main__":
    main()
