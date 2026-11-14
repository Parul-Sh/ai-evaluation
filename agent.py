
import json
import inspect
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from knowledge_base import KNOWLEDGE_BASE
from tools import (
    search_order,
    check_refund_eligibility,
    create_support_ticket
)


# 1. Load API credentials

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "openai.env", override=True)

client = OpenAI()

MODEL = "gpt-5.5"


# 2. Agent instructions

INSTRUCTIONS = f"""
You are a customer support AI agent.

Use this company knowledge:
{KNOWLEDGE_BASE}

Rules:
1. Answer accurately and never invent information.
2. If information is unavailable, say so.
3. Use tools when customer-specific information is needed.
4. Never invent an order ID or customer ID.
5. Ask for missing information when required.
6. Create a support ticket only when the customer
   explicitly requests one.
"""


# 3. Map tool names to actual Python functions

AVAILABLE_FUNCTIONS = {
    "search_order": search_order,
    "check_refund_eligibility": check_refund_eligibility,
    "create_support_ticket": create_support_ticket
}


# 4. Define parameters expected by each function

TOOL_PARAMETERS = {
    "search_order": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string"}
        },
        "required": ["order_id"],
        "additionalProperties": False
    },

    "check_refund_eligibility": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string"}
        },
        "required": ["order_id"],
        "additionalProperties": False
    },

    "create_support_ticket": {
        "type": "object",
        "properties": {
            "customer_id": {"type": "string"},
            "issue": {"type": "string"}
        },
        "required": ["customer_id", "issue"],
        "additionalProperties": False
    }
}


# 5. Build OpenAI tool definitions

TOOLS = [
    {
        "type": "function",
        "name": name,
        "description": inspect.getdoc(function) or name,
        "parameters": TOOL_PARAMETERS[name],
        "strict": True
    }
    for name, function in AVAILABLE_FUNCTIONS.items()
]


# 6. Execute the selected Python function

def execute_tool(tool_name, arguments):
    function = AVAILABLE_FUNCTIONS.get(tool_name)

    if function is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    result = function(**arguments)

    return json.dumps(result)


# 7. Run the agent

def run_agent(question):

    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=question,
        tools=TOOLS,
        tool_choice="auto"
    )

    # Handle tool calls
    for _ in range(5):

        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No tool call: return the final answer
        if not function_calls:
            return response.output_text

        tool_outputs = []

        for tool_call in function_calls:

            arguments = json.loads(tool_call.arguments)

            try:
                result = execute_tool(
                    tool_call.name,
                    arguments
                )
            except Exception as error:
                result = json.dumps({"error": str(error)})

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": result
            })

        # Send tool results back to OpenAI
        response = client.responses.create(
            model=MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS,
            tool_choice="auto"
        )

    raise RuntimeError("Maximum tool-call rounds exceeded.")
