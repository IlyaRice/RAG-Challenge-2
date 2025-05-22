# study/demo_09_advanced_concepts.py

import sys
import os
import json # For pretty printing example structures

# Add the src directory to the Python path for consistency
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This script is primarily explanatory, using text and pseudo-code.
# It does not execute complex logic but guides towards the main codebase.

def main():
    print("--- Demo: Advanced Concepts in RAG Pipeline ---")

    # --- 1. Introduction ---
    print("\n--- 1. Introduction ---")
    print("The previous demos (01-08) primarily focused on a simplified flow:")
    print("  - Processing a single PDF document.")
    print("  - Answering a single, relatively straightforward question based on that document.")
    print("\nThis script outlines how the full project (`src/`) handles more complex scenarios,")
    print("such as multiple reports, advanced question understanding, and structured LLM outputs.")

    # --- 2. Handling Multiple Reports ---
    print("\n--- 2. Handling Multiple Reports ---")
    print("Real-world applications often involve querying across a collection of documents.")
    print("For example, to answer a comparative question like 'Which company had higher revenue in 2022, A or B?',")
    print("the system needs to access and process reports from both Company A and Company B.")
    print("\nReference: `src/parsed_reports_merging.py` and `src/ingestion.py` handle aspects of")
    print("           processing multiple report files.")
    
    print("\nConceptual Need:")
    print("  - Aggregate data from various parsed PDF outputs (e.g., individual JSON files per report).")
    print("  - Maintain clear association between each piece of text/table/chunk and its original report source.")
    print("  - Enable targeted retrieval from specific reports or across all reports as needed.")

    print("\nPseudo-code / High-level Description (Data Aggregation):")
    print("""
# PSEUDO-CODE:
# all_parsed_reports_data = {} # Dictionary to hold data from all reports
# 
# for report_json_file in list_of_parsed_report_files:
#     report_data = load_json(report_json_file)
#     report_id = report_data['metainfo']['report_identifier'] # e.g., company_name + year
#     
#     # Store chunks, ensuring they are linked to their source report
#     processed_chunks_for_report = []
#     for chunk in report_data['content']['chunks']:
#         chunk['source_report_id'] = report_id
#         # Add other processing or metadata as needed
#         processed_chunks_for_report.append(chunk)
#     
#     all_parsed_reports_data[report_id] = {
#         'metainfo': report_data['metainfo'],
#         'chunks': processed_chunks_for_report,
#         # Potentially other structured data like tables, pages, etc.
#     }
# 
# # This `all_parsed_reports_data` can then be used to build a unified search index
# # or to selectively query data from specific reports.
# # The `src/ingestion.py` scripts create per-report FAISS/BM25 indexes,
# # which are then selected at query time by `src/questions_processing.py`.
    """)
    print("\nKey Data Management Points:")
    print("  - `document_id` or `report_id`: Crucial for associating data with its source.")
    print("  - Consistent data structure for chunks, tables, and metadata across all reports.")
    print("  - Efficient indexing to allow quick look-up of specific reports or global search.")

    # --- 3. Advanced Question Processing ---
    print("\n--- 3. Advanced Question Processing ---")
    print("User questions can be complex and may not map directly to a single piece of text.")
    print("The system needs to 'understand' the question to retrieve relevant information effectively.")
    print("\nReference: `src/questions_processing.py` implements sophisticated question handling.")
    print("           `src/prompts.py` (e.g., `RephrasedQuestionsPrompt`) shows how LLMs can be used")
    print("           for question decomposition.")

    print("\nCommon Complexities & System Responses:")
    print("  a. Decomposition: A question like 'Compare revenue and employee count for Company A and Company B'")
    print("     might be broken down into sub-questions for each metric and company.")
    print("     Example (from `RephrasedQuestionsPrompt` in `src/prompts.py`):")
    print("       - 'What was Company A's revenue?'")
    print("       - 'What was Company A's employee count?'")
    print("       - 'What was Company B's revenue?'")
    print("       - 'What was Company B's employee count?'")
    
    print("\n  b. Report Identification / Targeting:")
    print("     If the system has data from many reports, it needs to identify which report(s)")
    print("     a question refers to. This might involve extracting company names or other entities from the question.")
    print("     `src/questions_processing.py` uses company names from questions to target specific reports.")

    print("\n  c. Information Type Classification:")
    print("     Understanding if a question is about financial data, ESG initiatives, executive changes, etc.,")
    print("     can help tailor the retrieval process (e.g., prioritize tables for financial data) or the final prompt.")

    print("\nPseudo-code / High-level Description (Query Router/Classifier):")
    print("""
# PSEUDO-CODE:
# function process_user_question(user_question_text):
#     # 1. Entity Extraction (e.g., company names, years)
#     entities = extract_entities(user_question_text) # (e.g., using Spacy, an LLM, or regex)
#     target_reports = identify_target_reports(entities)
# 
#     # 2. Question Type Classification (e.g., using an LLM or rule-based system)
#     question_type = classify_question_type(user_question_text) 
#     # (e.g., 'FINANCIAL_METRIC', 'ESG_INFO', 'COMPARATIVE', 'GENERAL_INFO')
# 
#     # 3. Question Decomposition (if needed, e.g., for comparative or multi-part questions)
#     if question_type == 'COMPARATIVE' or is_multi_part(user_question_text):
#         sub_questions = decompose_question_with_llm(user_question_text, entities)
#     else:
#         sub_questions = [user_question_text]
# 
#     # 4. Strategy Selection based on type and targets
#     retrieval_strategy = "default_semantic_search"
#     prompting_strategy = "default_qa_prompt"
#     
#     if question_type == 'FINANCIAL_METRIC':
#         # May prioritize searching in tables or financial sections
#         retrieval_strategy = "search_financial_tables_then_text" 
#         prompting_strategy = "financial_data_extraction_prompt" # (e.g. AnswerWithRAGContextNumberPrompt)
# 
#     # 5. Execute retrieval and generation for each sub_question against target_reports
#     #    using the selected strategies.
#     #    (This is what `src/questions_processing.py` does in detail)
# 
#     return processed_results
    """)
    print("\nInfluence on Strategy:")
    print("  - Retrieval: Might search specific document sections, types of chunks (text vs. table),")
    print("    or use different algorithms (keyword vs. semantic) based on question type.")
    print("  - Prompting: Different system prompts or few-shot examples might be used for the final LLM call")
    print("    to guide it towards the desired answer format or reasoning style.")

    # --- 4. Chain-of-Thought / Structured Output (Briefly) ---
    print("\n--- 4. Chain-of-Thought / Structured Output ---")
    print("For complex questions, simply asking for a final answer might not yield the best results.")
    print("Prompting the LLM to produce a 'chain of thought' (step-by-step reasoning) or a structured")
    print("output (e.g., JSON) can significantly improve answer quality, reliability, and verifiability.")
    print("\nReference: `src/prompts.py` contains many examples, such as `AnswerWithRAGContextNumberPrompt`,")
    print("           `AnswerWithRAGContextNamePrompt`, etc., which define Pydantic schemas for structured")
    print("           JSON output and include fields like `step_by_step_analysis`.")

    print("\nConceptual Example (Structured Output for a Financial Question):")
    print("  Prompt Snippet (Instructing LLM):")
    print("  \"\"\"")
    print("  ... (context provided) ...")
    print("  Question: What was the company's net profit margin in 2023?")
    print("  Provide your answer in the following JSON format:")
    print("  {")
    print("    \"step_by_step_analysis\": \"Explain how you found the answer, including page numbers and calculations.\",")
    print("    \"metric_name\": \"Net Profit Margin\",")
    print("    \"year\": 2023,")
    print("    \"value_percentage\": <float or 'N/A'>,")
    print("    \"relevant_pages\": [<list of page numbers>]")
    print("  }")
    print("  \"\"\"")

    print("\n  Potential LLM JSON Output:")
    example_llm_output = {
        "step_by_step_analysis": "1. Identified the question asks for 'Net Profit Margin' for 2023. 2. Scanned context for keywords like 'net profit margin', 'net income', 'revenue'. 3. Found 'Net Income of $15M on page 42' and 'Total Revenue of $100M on page 40' for 2023. 4. Calculated margin as (15/100)*100 = 15%.",
        "metric_name": "Net Profit Margin",
        "year": 2023,
        "value_percentage": 15.0,
        "relevant_pages": [40, 42]
    }
    print(f"  ```json\n{json.dumps(example_llm_output, indent=2)}\n  ```")
    print("\nBenefits:")
    print("  - Improved Accuracy: LLM is forced to 'think step-by-step'.")
    print("  - Verifiability: Reasoning steps allow humans to check the LLM's work.")
    print("  - Consistency: Structured output is easier to parse and use programmatically.")

    # --- 5. Conclusion ---
    print("\n--- 5. Conclusion ---")
    print("This script has briefly touched upon advanced topics like handling multiple reports,")
    print("sophisticated question processing, and leveraging structured LLM outputs.")
    print("These are crucial for building robust and effective RAG applications.")
    print("\nThe actual implementations in the `src/` directory (especially `src/pipeline.py`,")
    print("`src/questions_processing.py`, `src/prompts.py`, and `src/ingestion.py`) are more detailed")
    print("and handle many more edge cases and optimizations.")
    print("\nWe encourage you to explore `main.py` and `src/pipeline.py` to see how these concepts")
    print("are orchestrated in the full project.")

    print("\n--- End of Advanced Concepts Demo ---")

if __name__ == "__main__":
    main()
