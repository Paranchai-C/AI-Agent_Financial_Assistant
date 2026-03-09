🚀 Benchmark Tasks & Demonstration
To verify the agent's capabilities, the following tasks are demonstrated in the [Demo Video Link]:

Task A: Persona (System Prompt)
Prompt: "Who are you?"

Expected Result: The agent identifies itself as a Financial Assistant and maintains a professional persona throughout the session.

Task B: Single Tool Call
Prompt: "What is the price of NVDA?"

Expected Result: The agent correctly calls get_stock_price("NVDA") and returns the mock value of 190.00.

Task C: Parallel Tool Calls (Integration & Comparison)
Prompt: "Compare the stock prices of AAPL and TSLA."

Key Checkpoints:

Debug Log: Shows two simultaneous tool executions in a single turn (get_stock_price for both AAPL and TSLA).

Analytical Answer: The agent integrates both results (260.00 vs 430.00) and provides a comparative analysis (e.g., stating which one is higher).

Task D: Memory & Context Awareness
Step 1: "My name is Paranchai."

Step 2: "What is my name?"

Expected Result: The agent successfully retrieves the user's name from the conversation history (Memory) without re-calling any tools.

Task E: Robustness & Error Handling
Prompt: "What is the price of GOOG?"

Expected Result: The agent handles unknown data gracefully by returning a polite "Data not found" message based on the mock function's error return, without crashing.
