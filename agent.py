
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_base import KNOWLEDGE_BASE

# Load API credentials
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "openai.env", override=True)

client = OpenAI()

# Agent instructions
INSTRUCTIONS = f"""
You are a customer support AI agent.

Use the following company knowledge:

{KNOWLEDGE_BASE}

Your responsibilities:
1. Answer customer questions accurately.
2. Never invent information.
3. If information is unavailable, say so.
4. Be professional and concise.
"""

# Agent execution function
def run_agent(question):

    response = client.responses.create(
        model="gpt-5.5",
        instructions=INSTRUCTIONS,
        input=question
    )

    return response.output_text
