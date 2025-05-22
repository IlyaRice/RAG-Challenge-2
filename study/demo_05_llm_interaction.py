# study/demo_05_llm_interaction.py

import sys
import os

# Add the src directory to the Python path for consistency (though not strictly needed for this demo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 1. Define Sample Inputs ---
SAMPLE_QUESTION = "What is the company's total revenue for the latest fiscal year?"

SAMPLE_CONTEXT_CHUNKS = [
    "Chunk 1 (from Page 5): ...In the fiscal year ending 2023, the company reported strong financial performance. Total revenue reached $150 million, an increase of 15% from the previous year...",
    "Chunk 2 (from Page 12): ...Operating expenses were managed effectively, contributing to a healthy net profit margin. The CEO highlighted the revenue growth as a key achievement...",
    "Chunk 3 (from Page 8): ...Segment analysis shows that the software division contributed $100 million to total revenue, while the hardware division accounted for $50 million..."
]

# --- 2. Prompt Engineering (Simplified) ---
# Inspired by src/prompts.py (e.g., AnswerWithRAGContextSharedPrompt.user_prompt)
# For a real application, prompts are much more complex, often including:
# - System instructions (role, task, output format)
# - Few-shot examples
# - Specific constraints (e.g., "answer only from context")
# - Pydantic schemas for structured output (as seen in src/prompts.py)

def format_simplified_prompt(question: str, context_chunks: list[str]) -> str:
    """
    Creates a simplified prompt by combining the question and context.
    """
    context_str = "\n".join(context_chunks)
    
    # This is a very basic prompt structure.
    # Real prompts (see src/prompts.py) are more detailed.
    prompt = f"""
You are an AI assistant. Based on the following context, please answer the user's question.
If the answer is not found in the context, state that clearly.

--- CONTEXT ---
{context_str}
--- END CONTEXT ---

--- QUESTION ---
{question}
--- END QUESTION ---

Answer:
"""
    return prompt

# --- 3. LLM Interaction (Mocked) ---
# In a real system (see src/api_requests.py), this would involve:
# - Setting up an API client (e.g., OpenAI, Gemini, IBM WatsonX)
# - Handling API keys and authentication
# - Making an HTTP request to the LLM API endpoint
# - Parsing the LLM's JSON response
# - Error handling, retries, etc.

def mock_llm_call(prompt: str) -> str:
    """
    Simulates a call to an LLM.
    Returns a hardcoded, plausible-sounding answer.
    """
    print("\n--- Mock LLM Call ---")
    print("Sending the following prompt to the (mocked) LLM:\n")
    print(prompt) # Show what would be sent
    print("----------------------")
    
    # Simulate a delay as if an API call was made
    # import time
    # time.sleep(1) 
    
    # Hardcoded response
    mocked_response = "Based on the provided context (Chunk 1 and Chunk 3), the company's total revenue for the fiscal year ending 2023 is $150 million. [This is a mocked LLM response]"
    
    return mocked_response

def main():
    print("--- Demo: Simplified LLM Interaction Flow (Mocked) ---")
    print("This script demonstrates the basic flow of forming a prompt and getting a (mocked) LLM response.")
    print("Refer to src/api_requests.py for actual LLM API interactions and src/prompts.py for complex prompt engineering.\n")

    # --- Step 1: Original Question and Context (Already defined above) ---
    print("1. Original User Question:")
    print(f"   \"{SAMPLE_QUESTION}\"")

    print("\n2. Retrieved Context Chunks:")
    for i, chunk in enumerate(SAMPLE_CONTEXT_CHUNKS):
        print(f"   Chunk {i+1}: \"{chunk}\"")

    # --- Step 2: Format the Prompt ---
    print("\n3. Formatting the Prompt:")
    formatted_prompt = format_simplified_prompt(SAMPLE_QUESTION, SAMPLE_CONTEXT_CHUNKS)
    # We'll print the formatted prompt inside the mock_llm_call to simulate it being "sent"
    # For clarity here, let's show a snippet or confirmation:
    print("   Prompt has been formatted. It will be shown when 'mock_llm_call' is invoked.")


    # --- Step 3: Call the Mock LLM ---
    # The prompt itself will be printed within mock_llm_call
    mocked_answer = mock_llm_call(formatted_prompt)

    # --- Step 4: Output the Mocked LLM's Answer ---
    print("\n4. Mocked LLM's Answer:")
    print(f"   \"{mocked_answer}\"")
    
    print("\n--- End of Demo ---")

if __name__ == "__main__":
    main()
