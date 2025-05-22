# study/demo_01_pdf_parsing.py

import sys
import os

# Add the src directory to the Python path to allow importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_parsing import DocumentParser, TextExtractor, LayoutDetector, StructureDetector, EntityRecognizer, Pipeline

def main():
    # Ensure Docling models are downloaded
    # This might take a while if the models are not already downloaded
    print("Checking and downloading Docling models if necessary...")
    Pipeline.download_docling_models()
    print("Docling models are ready.")

    # Define the path to the sample PDF file
    # Using a relative path from the root of the project
    sample_pdf_path = "data/test_set/pdf_reports/194000c9109c6fa628f1fed33b44ae4c2b8365f4.pdf"
    print(f"Using sample PDF: {sample_pdf_path}")

    # Check if the sample PDF file exists
    if not os.path.exists(sample_pdf_path):
        print(f"Error: Sample PDF file not found at {sample_pdf_path}")
        print("Please ensure the data is available in the 'data/test_set/pdf_reports/' directory.")
        # As a fallback, let's try to list files in the directory to help debug
        print(f"Looking for data in: {os.path.abspath('data/test_set/pdf_reports/')}")
        if os.path.exists('data/test_set/pdf_reports/'):
             print(f"Files in 'data/test_set/pdf_reports/': {os.listdir('data/test_set/pdf_reports/')[:5]}") # Show first 5
        else:
            print("'data/test_set/pdf_reports/' directory does not exist.")
        return

    # Initialize components for PDF parsing
    # For this demo, we'll focus on text extraction and basic structure.
    # More advanced components like EntityRecognizer might require specific model setups.
    text_extractor = TextExtractor()
    layout_detector = LayoutDetector() # Depends on Detectron2 and models
    # StructureDetector and EntityRecognizer might be more complex to set up for a simple demo
    # For now, let's try to use DocumentParser which encapsulates some of this.

    print("Initializing DocumentParser...")
    # The DocumentParser might try to load all models, which can be heavy.
    # Let's see if we can parse with just text and layout.
    # We might need to adjust this based on how DocumentParser is implemented.
    try:
        parser = DocumentParser() # This might trigger model loading for all components
    except Exception as e:
        print(f"Error initializing DocumentParser: {e}")
        print("This might be due to missing models or dependencies for all components.")
        print("Attempting a more basic parsing approach...")
        # Fallback: Try to use TextExtractor directly if DocumentParser is too complex for a quick demo
        try:
            doc_bytes = open(sample_pdf_path, "rb").read()
            # TextExtractor usually works on a page-by-page basis after layout detection.
            # Let's try to simulate a simplified flow if DocumentParser is problematic.
            # This part might need adjustment based on actual class interfaces.
            # For a true demo, we'd ideally use the full Pipeline or DocumentParser.
            # If direct text extraction is needed, it would be more involved.
            print("DocumentParser initialization failed. A full demo of DocumentParser requires all models.")
            print("For a simplified text extraction, you would typically integrate TextExtractor within a pipeline.")
            print("This demo will focus on what can be achieved with available components.")
            # As an alternative, we can try to show how many pages pdfminer.six detects.
            from pdfminer.high_level import extract_pages
            try:
                page_count = 0
                for _ in extract_pages(sample_pdf_path):
                    page_count +=1
                print(f"Basic check: pdfminer.six detected {page_count} pages in the document.")
            except Exception as pe:
                print(f"Error during basic pdfminer.six check: {pe}")

            return # Exiting if DocumentParser fails as it's key for the intended demo
        except Exception as fallback_e:
            print(f"Error in fallback parsing attempt: {fallback_e}")
            return


    # Parse the PDF document
    print(f"Parsing PDF: {sample_pdf_path}")
    try:
        # The `parse` method should take the PDF path and return a Document object
        document = parser.parse(sample_pdf_path)
    except Exception as e:
        print(f"Error during PDF parsing: {e}")
        print("This could be due to issues with the PDF file or model incompatibilities.")
        print("Ensure all models for DocumentParser components are correctly downloaded and configured.")
        # Let's try to see if any specific component is causing the issue
        # This is for debugging purposes if the above fails.
        print("Attempting to extract text directly to see if that part works...")
        try:
            from src.pdf_parsing.utils import pdf_to_images_pymupdf
            from PIL import Image
            doc_images = list(pdf_to_images_pymupdf(sample_pdf_path))
            if not doc_images:
                print("Could not convert PDF to images using PyMuPDF.")
                return
            
            first_page_image = Image.open(doc_images[0])
            extracted_text_elements = text_extractor.extract_text(first_page_image, page_number=0)
            
            if extracted_text_elements:
                print(f"Direct text extraction from first page (first 5 elements): {extracted_text_elements[:5]}")
                first_page_text_content = " ".join([te.text for te in extracted_text_elements])
                print("\n--- Text Content of First Page (Direct Extraction) ---")
                print(first_page_text_content[:1000]) # Print first 1000 characters
                print("----------------------------------------------------")
            else:
                print("Direct text extraction yielded no elements.")

        except Exception as te_e:
            print(f"Error during direct text extraction attempt: {te_e}")
        return

    # Print the number of pages parsed
    num_pages = len(document.pages)
    print(f"\nSuccessfully parsed document. Number of pages: {num_pages}")

    # Print the text content of the first page
    if num_pages > 0:
        first_page = document.pages[0]
        print("\n--- Text Content of First Page ---")
        # The 'text' attribute of a Page object should give its full text content
        # Or, it might be a list of text blocks that need to be joined.
        # This depends on the structure of the Page object from pdf_parsing.py
        if hasattr(first_page, 'text_content'): # Assuming a 'text_content' field
            print(first_page.text_content[:1000]) # Print first 1000 characters
        elif hasattr(first_page, 'text_blocks') and first_page.text_blocks: # Assuming it has text_blocks
            full_text = " ".join([block.text for block in first_page.text_blocks if hasattr(block, 'text')])
            print(full_text[:1000]) # Print first 1000 characters
        elif hasattr(first_page, 'text_elements') and first_page.text_elements: # Common alternative
            full_text = " ".join([elem.text for elem in first_page.text_elements if hasattr(elem, 'text')])
            print(full_text[:1000])
        else:
            print("Could not find a direct text attribute on the first page object.")
            print("Page object details:", dir(first_page)) # To understand its structure
        print("----------------------------------")
    else:
        print("The document has no pages or pages could not be parsed.")

if __name__ == "__main__":
    main()
