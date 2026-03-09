import json
from openai import OpenAI

# 1. Setup Client for Local LLM (Ollama)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", 
)

MODEL_NAME = "mistral-nemo" 

# --- 2. Mock Data Functions ---
def get_exchange_rate(currency_pair: str):
    rates = {
        "USD_TWD": "32.0",
        "JPY_TWD": "0.2",
        "EUR_USD": "1.2"
    }
    print(f"[Debug] Calling get_exchange_rate for {currency_pair}")
    rate = rates.get(currency_pair)
    if rate:
        return json.dumps({"currency_pair": currency_pair, "rate": rate})
    return json.dumps({"error": "Data not found"})

def get_stock_price(symbol: str):
    prices = {
        "AAPL": "260.00",
        "TSLA": "430.00",
        "NVDA": "190.00"
    }
    print(f"[Debug] Calling get_stock_price for {symbol}")
    price = prices.get(symbol)
    if price:
        return json.dumps({"symbol": symbol, "price": price})
    return json.dumps({"error": "Data not found"})

# --- 3. Tool Definitions ---
available_functions = {
    "get_exchange_rate": get_exchange_rate,
    "get_stock_price": get_stock_price,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate for a currency pair.",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency_pair": {"type": "string", "description": "e.g. USD_TWD"}
                },
                "required": ["currency_pair"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get stock price for a symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "e.g. AAPL"}
                },
                "required": ["symbol"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

def run_financial_agent():
    # 4. System Prompt & Memory Initialization
    messages = [
        {
            "role": "system", 
            "content": (
                "You are a professional Financial Assistant. "
                "You must remember the user's name from the conversation history. "
                "If I tell you my name, just say 'Nice to meet you' and remember it. "
                "If I ask for my name, just tell me my name directly without mentioning tools or history."
                "Only call tools for stock prices (AAPL, TSLA, NVDA) or exchange rates. "
                "If a user asks to COMPARE stocks, you MUST calculate the difference"
                "and explicitly state which stock is more expensive or cheaper."
                "If no tool is needed, just reply naturally."
            )
        }
    ]
    
    print(f"Financial Agent ({MODEL_NAME}) Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        messages.append({"role": "user", "content": user_input})

        # Initial LLM call to determine if tools are needed
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )
        
        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        if tool_calls:
            # Convert to dict to ensure compatibility with history appending
            messages.append(response_msg.to_dict())
            
            # 5. Handle Tool Execution
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    continue
                
                function_to_call = available_functions.get(function_name)
                result = function_to_call(**function_args) if function_to_call else json.dumps({"error": "Function not found"})
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })
            
            # Final LLM call to synthesize the tool results into a natural response
            final_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            final_content = final_response.choices[0].message.content
            print(f"Agent: {final_content}")
            messages.append({"role": "assistant", "content": final_content})
        else:
            # Direct response for general queries
            print(f"Agent: {response_msg.content}")
            messages.append({"role": "assistant", "content": response_msg.content})

if __name__ == "__main__":
    run_financial_agent()