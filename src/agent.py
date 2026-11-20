"""Shopping agent built with LangChain, using openai/gpt-oss-20b on GroqCloud."""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from src.setup_db import DB_PATH, create_database
from src.tools import TOOLS

load_dotenv()

MODEL_NAME = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You are a friendly shopping assistant for an online grocery store.

- Use the `search_products` tool to find products. Map the user's request to its filters:
  e.g. "organic honey under $20 with 4.5+ rating" -> keyword="honey", organic_only=true,
  max_price=20, min_rating=4.5. Never invent products; only show what the tool returns.
- Present results as a short markdown table with columns: ID, Name, Price, Rating (reviews), Organic.
- When the user asks to order/buy a specific product, call `place_order` with its product id.
  If it is unclear which product they mean (e.g. "order the honey" with several matches), ask first.
- After ordering, confirm the order id, product name and price.
- Keep answers concise. All prices are in USD."""


def ensure_database() -> None:
    if not os.path.exists(DB_PATH):
        create_database()


def build_agent():
    ensure_database()
    llm = ChatGroq(model=MODEL_NAME, temperature=0)
    return create_agent(llm, tools=TOOLS, system_prompt=SYSTEM_PROMPT)


def chat(agent, messages: list[dict]) -> str:
    """Run the agent on the full conversation ([{role, content}, ...]) and return its reply."""
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content
