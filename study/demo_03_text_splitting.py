# study/demo_03_text_splitting.py

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_parsing import DocumentParser, Pipeline
# The project uses langchain's RecursiveCharacterTextSplitter via tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

def main():
    # --- Step 1: Ensure models are downloaded and parse the sample PDF ---
    print("Checking and downloading Docling models if necessary...")
    Pipeline.download_docling_models()
    print("Docling models are ready.")

    sample_pdf_path = "data/test_set/pdf_reports/194000c9109c6fa628f1fed33b44ae4c2b8365f4.pdf"
    print(f"Using sample PDF: {sample_pdf_path}")

    if not os.path.exists(sample_pdf_path):
        print(f"Error: Sample PDF file not found at {sample_pdf_path}")
        # Fallback message similar to demo_01
        print(f"Looking for data in: {os.path.abspath('data/test_set/pdf_reports/')}")
        if os.path.exists('data/test_set/pdf_reports/'):
             print(f"Files in 'data/test_set/pdf_reports/': {os.listdir('data/test_set/pdf_reports/')[:5]}")
        else:
            print("'data/test_set/pdf_reports/' directory does not exist.")
        return

    print("Initializing DocumentParser...")
    try:
        parser = DocumentParser()
    except Exception as e:
        print(f"Error initializing DocumentParser: {e}")
        print("Ensure all models for DocumentParser components are correctly downloaded and configured.")
        return

    print(f"Parsing PDF: {sample_pdf_path}")
    try:
        document = parser.parse(sample_pdf_path)
    except Exception as e:
        print(f"Error during PDF parsing: {e}")
        print("This could be due to issues with the PDF file or model incompatibilities.")
        return

    num_pages = len(document.pages)
    print(f"\nSuccessfully parsed document. Number of pages: {num_pages}")

    if num_pages == 0:
        print("The document has no pages or pages could not be parsed.")
        return

    # --- Step 2: Concatenate text content from all pages ---
    print("\nConcatenating text content from all pages...")
    full_text_content = []
    for i, page in enumerate(document.pages):
        # Assuming page.text_content or similar attribute holds the text
        # Based on demo_01, we might need to check for 'text_content', 'text_blocks', or 'text_elements'
        page_text = ""
        if hasattr(page, 'text_content') and page.text_content:
            page_text = page.text_content
        elif hasattr(page, 'text_elements') and page.text_elements:
            page_text = " ".join([elem.text for elem in page.text_elements if hasattr(elem, 'text')])
        elif hasattr(page, 'text_blocks') and page.text_blocks: # Fallback, structure might vary
            page_text = " ".join([block.text for block in page.text_blocks if hasattr(block, 'text')])
        
        if page_text:
            full_text_content.append(page_text)
        # else:
            # print(f"Page {i+1} has no extractable text content.")

    concatenated_text = "\n\n".join(full_text_content) # Join pages with double newline for separation

    if not concatenated_text:
        print("No text content could be extracted from the document to split.")
        return
    
    print(f"Total length of concatenated text: {len(concatenated_text)} characters.")
    # print(f"First 200 chars of concatenated text: {concatenated_text[:200]}")


    # --- Step 3: Instantiate RecursiveCharacterTextSplitter ---
    # Parameters based on src.text_splitter.TextSplitter._split_page method:
    # model_name="gpt-4o" (for tiktoken encoder)
    # chunk_size=300 (tokens)
    # chunk_overlap=50 (tokens)
    print("\nInitializing RecursiveCharacterTextSplitter...")
    try:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4o", # As used in src.text_splitter
            chunk_size=300,    # As used in src.text_splitter for page text
            chunk_overlap=50   # As used in src.text_splitter
        )
    except Exception as e:
        print(f"Error initializing RecursiveCharacterTextSplitter: {e}")
        print("This might be due to tiktoken or model name issues. Ensure tiktoken is installed.")
        # Fallback to basic character splitter if tiktoken fails for some reason in demo
        print("Attempting fallback to basic RecursiveCharacterTextSplitter...")
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, # Character count for basic splitter
                chunk_overlap=100 # Character count for basic splitter
            )
            print("Using basic RecursiveCharacterTextSplitter (character-based).")
        except Exception as fallback_e:
            print(f"Error initializing basic RecursiveCharacterTextSplitter: {fallback_e}")
            return
        

    # --- Step 4: Split the concatenated text into chunks ---
    print("Splitting text into chunks...")
    try:
        text_chunks = text_splitter.split_text(concatenated_text)
    except Exception as e:
        print(f"Error during text splitting: {e}")
        return

    # --- Step 5: Print the total number of chunks and first few chunks ---
    num_chunks = len(text_chunks)
    print(f"\nTotal number of chunks created: {num_chunks}")

    print("\n--- First 3 Chunks ---")
    for i, chunk in enumerate(text_chunks[:3]):
        print(f"\n--- Chunk {i+1} (Length: {len(chunk)} chars) ---")
        print(chunk)
        print("----------------------")
    
    if num_chunks > 3:
        print(f"\n({num_chunks - 3} more chunks not printed)")

if __name__ == "__main__":
    main()
