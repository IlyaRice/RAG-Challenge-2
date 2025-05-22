# study/demo_07_ingestion.py

import sys
import os
import json # For pretty printing the serialized table

# Add the src directory to the Python path for consistency
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 1. Prepare Sample Data (Simulate output from previous pipeline steps) ---
DOCUMENT_ID = "sample_report_XYZ123"

# Sample text chunks (e.g., from text splitting)
sample_text_chunk_1 = {
    "id": "chunk_001",
    "page_number": 1,
    "text": "This is the first paragraph from page 1, discussing financial performance."
}
sample_text_chunk_2 = {
    "id": "chunk_002",
    "page_number": 1,
    "text": "Another paragraph from page 1, focusing on market trends and analysis."
}
sample_text_chunk_3 = {
    "id": "chunk_003",
    "page_number": 2,
    "text": "This chunk is from page 2 and covers future outlook and strategy."
}

# Sample serialized table (e.g., from table serialization like in demo_02)
# This structure is a simplified example. Real table structures can be more complex.
sample_serialized_table_1 = {
    "id": "table_001", # Could be chunk_004 if tables are treated as chunks
    "page_number": 2,
    "type": "table", # Explicitly marking type
    "title": "Q4 Financial Summary",
    "columns": ["Metric", "Value", "Change"],
    "rows": [
        ["Revenue", "1.2M USD", "+5%"],
        ["Expenses", "0.8M USD", "+2%"]
    ],
    "summary": "Table shows Q4 financial highlights with positive revenue growth."
    # In a real scenario, this might be further serialized into a single string
    # or kept as a structured dict depending on ingestion needs.
    # For this demo, we'll treat the dict itself as the 'content' for the table chunk.
}


# --- 2. Illustrate Data Structuring for Ingestion ---
# Based on src/ingestion.py, data is typically processed from JSON files where
# each file represents a document, and contains a list of 'chunks' under 'content'.
# Each chunk is a dictionary with 'text' and other metadata.
# We will create a list of "ingestable items" (dictionaries) for our DOCUMENT_ID.

def structure_data_for_ingestion(doc_id: str, text_chunks: list[dict], serialized_tables: list[dict]) -> list[dict]:
    """
    Structures data into a list of dictionaries, where each dictionary represents
    an item to be ingested (e.g., a text chunk or a table).
    This simulates the 'chunks' list found within the JSON files processed by src/ingestion.py.
    """
    ingestable_items = []
    current_chunk_id_counter = 0 # Simple counter for unique chunk IDs within this document

    # Process text chunks
    for tc_meta in text_chunks:
        current_chunk_id_counter += 1
        item = {
            "id": f"doc_{doc_id}_chunk_{current_chunk_id_counter:03d}", # More robust ID
            "document_id": doc_id,
            "type": "text_chunk", # Differentiating from a whole page text or table
            "content": tc_meta["text"], # The actual text to be indexed/embedded
            "metadata": {
                "original_chunk_id": tc_meta["id"],
                "page_number": tc_meta.get("page_number", "N/A"),
                # Other metadata like section, etc., could be added here
            }
        }
        ingestable_items.append(item)

    # Process serialized tables
    # Tables might be ingested as distinct items or their textual representation added to text chunks.
    # Here, we'll treat them as distinct items to be potentially embedded/indexed.
    for table_meta in serialized_tables:
        current_chunk_id_counter += 1
        item = {
            "id": f"doc_{doc_id}_table_{current_chunk_id_counter:03d}",
            "document_id": doc_id,
            "type": "table_content",
            # Content could be a JSON string of the table, its summary, or a linearized version.
            # For this demo, we'll use its textual summary, but could also be json.dumps(table_meta)
            "content": table_meta.get("summary", json.dumps(table_meta)), # Or a more structured text representation
            "full_table_data": table_meta, # Keeping the full structured table for potential other uses
            "metadata": {
                "original_table_id": table_meta["id"],
                "page_number": table_meta.get("page_number", "N/A"),
                "title": table_meta.get("title", "N/A")
            }
        }
        ingestable_items.append(item)
        
    return ingestable_items

def main():
    print("--- Demo: Data Preparation for Ingestion (Conceptual) ---")
    print("This script demonstrates how data (text chunks, tables) is structured before actual ingestion")
    print("into a vector database or search index, based on patterns in src/ingestion.py.\n")

    # --- Step 1: Sample Data (defined above) ---
    print(f"1. Sample Data prepared for Document ID: {DOCUMENT_ID}\n")
    print(f"   Text Chunk 1 (ID {sample_text_chunk_1['id']}): \"{sample_text_chunk_1['text'][:50]}...\"")
    print(f"   Serialized Table 1 (ID {sample_serialized_table_1['id']}): Title: \"{sample_serialized_table_1['title']}\"")


    # --- Step 2 & 3: Structure Data and Prepare for Ingestion ---
    # In src/ingestion.py, `process_reports` reads JSON files. Each file's content,
    # particularly `report_data['content']['chunks']`, is a list of dictionaries.
    # This demo simulates creating such a list for one document.
    
    print("\n2. Structuring Data for Ingestion:")
    
    prepared_data_for_doc = structure_data_for_ingestion(
        DOCUMENT_ID,
        [sample_text_chunk_1, sample_text_chunk_2, sample_text_chunk_3],
        [sample_serialized_table_1]
    )
    
    print(f"   Created a list of {len(prepared_data_for_doc)} ingestable items for document '{DOCUMENT_ID}'.")
    print("   Each item is a dictionary containing content and metadata.\n")

    # --- Step 4: Output Structured Data ---
    print("3. Prepared Data (Simulating 'chunks' list for one document):")
    # Pretty print the list of dictionaries
    print(json.dumps(prepared_data_for_doc, indent=2))

    print("\n4. Next Steps (Conceptual):")
    print("   This list of structured items (prepared_data_for_doc) would then be processed further:")
    print("   - For VectorDBIngestor (src/ingestion.py):")
    print("     - The 'content' of each item would be passed to an embedding model (e.g., OpenAI).")
    print("     - These embeddings, along with the items' metadata, would be stored in a FAISS index.")
    print("   - For BM25Ingestor (src/ingestion.py):")
    print("     - The 'content' (text) of each item would be tokenized.")
    print("     - A BM25Okapi index would be built from these tokenized texts and saved as a .pkl file.")
    print("   The actual ingestion involves creating these index files (FAISS, PKL) per document.")
    
    print("\n--- End of Demo ---")
    print("Note: This demo focuses on data preparation. No actual database/index interactions occur.")

if __name__ == "__main__":
    main()
