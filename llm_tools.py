import os
from openai import OpenAI
from dotenv import load_dotenv
from robocorp.browser import page
from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize the OpenAI client for DeepSeek
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@tool
def find_element_selector(target_element_description: str) -> str:
    """
    A tool that receives a natural language description of a target UI element
    (like 'the username input field' or 'the login button') and the current HTML content of the page.
    It uses an LLM to return a precise CSS selector to locate that element.
    This is useful for adapting to UI changes without hardcoding selectors.
    """
    html_snippet = page().content()

    prompt = f"""
    You are a CSS-selector generator for Playwright.
    Given an HTML snippet and a target label/text, return only a fully qualified CSS selector
    that includes the tag name, any IDs or attributes, and is valid for Playwright.
    Wrap attribute values in double quotes.

    Examples:
    - input[id="username-uid1"]
    - button#login-submit
    - a[data-testid="members-button"]
    - button.Hm2Njssed7t23i.bxgKMAm3lq5BpA.SdamsUKjxSBwGb.SEj5vUdI3VvxDc

    HTML snippet:
    {html_snippet}

    Target element description: "{target_element_description}"

    Return only the single, most precise CSS selector below, with no extra text or explanation.
    """
    try:
        resp = client.chat.completions.create(
            model="YOUR LLM MODEL", # Using the coder model can be more reliable for this
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        selector = resp.choices[0].message.content.strip()
        # Clean up potential markdown formatting from the response
        if selector.startswith("```css"):
            selector = selector.split("\n")[1]
        if selector.endswith("```"):
            selector = selector[:-3]
        
        print(f"LLM generated selector for '{target_element_description}': {selector}")
        return selector.strip()
    except Exception as e:
        print(f"Error generating selector: {e}")
        return "ERROR"




