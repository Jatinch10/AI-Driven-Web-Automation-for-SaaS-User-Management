# src/agents/llm_agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def locate_selector(html_snippet: str, target_text: str) -> str:
    prompt = f"""
    You are a CSS‑selector generator for Playwright.
    Given an HTML snippet and a target label/text, return only a fully qualified CSS selector 
    that includes the tag name, any IDs or attributes, and is valid for Playwright’s page.fill() 
    or page.click(). Wrap attribute values in double quotes.

    Examples:
    • input[id="username-uid1"]
    • button#login-submit
    • input#password

    HTML snippet:
    {html_snippet}

    Target text: "{target_text}"

    Only Return the selector below with no extra snippet, just the selector:
    """
    resp = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0
    )
    return resp.choices[0].message.content.strip()
