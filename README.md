## 🚀 Benchmark Tasks & Demonstration
The following tasks are demonstrated in the [Demo Video Link]: https://youtu.be/ODrNZ7Z5DMQ

### **Task A: Persona (System Prompt)**
- **Input:** `"Who are you?"`
- **Result:** Agent identifies as a professional **Financial Assistant**.

### **Task B: Single Tool Call**
- **Input:** `"What is the price of NVDA?"`
- **Result:** Correctly returns the mock price of **$190.00**.

### **Task C: Parallel Tool Calls & Comparison**
- **Input:** `"Compare the stock prices of AAPL and TSLA."`
- **Checkpoints:** - Debug log shows **two simultaneous tool calls**.
  - Final answer provides an **integrated comparison** (e.g., TSLA is higher than AAPL).

### **Task D: Memory Test**
- **Step 1:** `"My name is Paranchai."`
- **Step 2:** `"What is my name?"`
- **Result:** Agent correctly retrieves **"Paranchai"** from history.

### **Task E: Robustness (Error Handling)**
- **Input:** `"What is the price of GOOG?"`
- **Result:** Handles unknown data gracefully by returning a **polite error message**.

---

## 💻 Local LLM Configuration
To optimize performance for this agent on local hardware (NVIDIA RTX 4050 LAPTOP 6GB VRAM), the following configuration was used:

* **Inference Engine:** [Ollama](https://ollama.com/)
* **Primary Model:** `mistral-nemo` (12B parameters) - Chosen for its superior function-calling accuracy and context retention compared to smaller models.
* **Context Handling:** Adjusted System Prompts to reduce "hallucinations" regarding user identity and memory tasks.

---
