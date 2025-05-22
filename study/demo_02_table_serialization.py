# study/demo_02_table_serialization.py

import sys
import os
import json # For pretty printing serialized output

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_parsing import DocumentParser, Pipeline
# Assuming DocumentParser result (`document.pages[i].tables`) will yield objects
# that TableSerializer can work with.
from src.tables_serialization import TableSerializer # Key import for this demo

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
        parser = DocumentParser() # This loads all models for parsing
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

    # --- Step 2: Import and Instantiate TableSerializer ---
    # Import is at the top.
    print("\nInitializing TableSerializer...")
    try:
        table_serializer = TableSerializer()
    except Exception as e:
        print(f"Error initializing TableSerializer: {e}")
        # This might happen if TableSerializer has its own dependencies or setup.
        return
    print("TableSerializer initialized.")

    # --- Step 3: Iterate through pages and tables, serialize, and print ---
    print("\n--- Serializing Tables from Document ---")
    tables_found_count = 0
    max_tables_to_print = 3 # Let's limit the output

    for i, page in enumerate(document.pages):
        if tables_found_count >= max_tables_to_print:
            break # Stop if we have printed enough tables

        # Assuming `page.tables` exists and contains list of table objects
        if hasattr(page, 'tables') and page.tables:
            print(f"\nFound {len(page.tables)} table(s) on Page {page.page_number + 1}:")
            for j, table_obj in enumerate(page.tables):
                if tables_found_count >= max_tables_to_print:
                    break

                print(f"\nSerializing Table {j+1} from Page {page.page_number + 1}...")
                try:
                    # The `serialize` method should take the table object from DocumentParser
                    # and return a serializable representation (e.g., dict).
                    serialized_table = table_serializer.serialize(table_obj)

                    print(f"--- Serialized Table {j+1} (Page {page.page_number + 1}) ---")
                    # Pretty print the JSON string for better readability
                    print(json.dumps(serialized_table, indent=2, ensure_ascii=False))
                    print("--------------------------------------")
                    tables_found_count += 1

                except Exception as e:
                    print(f"Error serializing Table {j+1} on Page {page.page_number + 1}: {e}")
                    # Print details of the table object if serialization fails, for debugging
                    print("Table object details:", dir(table_obj))
                    if hasattr(table_obj, '__dict__'):
                        print("Table object __dict__:", table_obj.__dict__)

        else:
            # print(f"No tables found on Page {page.page_number + 1}.") # Can be verbose
            pass

    if tables_found_count == 0:
        print("\nNo tables were found or serialized from the document.")
    else:
        print(f"\nFinished processing. Serialized and printed {tables_found_count} table(s).")

if __name__ == "__main__":
    main()
