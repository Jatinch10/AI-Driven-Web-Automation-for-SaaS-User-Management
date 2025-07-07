import os
from robocorp.tasks import task
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from automation_tasks import login_to_trello, scrape_workspace_members, invite_user_to_workspace
from llm_tools import find_element_selector

# import asyncio
# from robocorp import browser
# from automation_tasks import get_tools

# Define the tools the agent can use
tools = [
    login_to_trello,
    scrape_workspace_members,
    invite_user_to_workspace,
    find_element_selector
]




# Define the prompt template for the agent
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant that automates tasks in Trello using the provided tools."),
#     ("user", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ])

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a highly intelligent web automation assistant.
Your goal is to complete tasks in a web browser by interacting with elements.
You have one primary tool for interaction: `perform_ui_action`.

- **Always use `perform_ui_action` for clicking buttons or filling out forms.**
- **Be descriptive.** Instead of "the button", say "the blue 'Save Changes' button at the bottom of the form".
- **Check your assumptions.** After navigating, you are on a new page. Don't assume elements from the previous page are there.
- **If an action fails, the tool will tell you why.** Read the error message carefully. The selector might be wrong, or you might be on the wrong page. Try describing the element differently or navigating to the correct page first.
- **Proceed step-by-step.** Do not try to do too many things in one thought.
"""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# A new, more effective prompt that guides the agent on how to use the tools.
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """
# You are a precise and methodical web automation assistant.
# - **Goal:** Your goal is to follow the user's instructions step-by-step.
# - **Tool Usage:**
#   1. ALWAYS start with the `login_and_navigate` tool. This is the only way to log in.
#   2. For ALL other actions on the page (clicking buttons, filling forms), use the `perform_ui_action` tool.
# - **Critical Instructions:**
#   - When using `perform_ui_action`, your 'description' MUST focus on the visible text. For a button with "Invite members", your description should be "the button with text 'Invite members'". This is the key to success.
#   - Read the result of every tool call. If it fails, the error message will tell you why. Do not imagine success.
# """),
#     ("user", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),
# ])



# @task
# def run_agent():
#     """
#     Initializes and runs the LangChain agent to perform a high-level task.
#     """
#     # Initialize the LLM
#     llm = ChatOpenAI(
#         model="deepseek/deepseek-chat-v3-0324:free",
#         temperature=0,
#         openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#         openai_api_base="https://openrouter.ai/api/v1"
#     )

#     # Create the agent
#     agent = create_openai_tools_agent(llm, tools, prompt)
#     agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#     # Define the high-level task for the agent
#     # You can change this to perform different sequences of actions
#     task_description = """
#     My goal is to add a new member to my Trello workspace.
#     1. First, please log me into Trello. My username is 'lavel89909@dxirl.com' and my password is 'JcHn1111'.
#     2. After you've logged in, go to the workspace members page, which is at 'https://trello.com/w/lavelsworkspace/members'.
#     3. On the members page, find a way to invite a new member. The new member's email is 'rakohi5975@bulmp3.com'. Invite them.
#     4. Confirm that the invitation was sent successfully.
#     """

#     # Run the agent
#     result = agent_executor.invoke({
#         "input": task_description
#     })

#     print("Agent run finished.")
#     print(result)


@task
def run_agent():
    """
    Initializes and runs the LangChain agent with AI-powered, resilient tools.
    """
    try:
        # browser.configure(
        #     browser_engine="chrome",
        #     headless=False,
        # )
        # page = browser.new_page()

        # # Get the toolset bound to our single page instance
        # tools = get_trello_tools(page)

        # Initialize the LLM for the agent
        agent_llm = ChatOpenAI(
            model="deepseek/deepseek-chat-v3-0324:free",
            temperature=0,
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )

        # Create the agent
        agent = create_openai_tools_agent(agent_llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # The task description now guides the agent's high-level thinking.
        # The agent will figure out the low-level UI interactions itself.
        task_description = """
        My goal is to add a new member to my Trello workspace.
        1. First, please log me into Trello. My username is 'lavel89909@dxirl.com' and my password is 'JcHn1111'.
        2. After you've logged in, wait for two seconds then go to the workspace members page, which is at 'https://trello.com/w/lavelsworkspace/members'.
        3. On the members page, find a way to invite a new member by scanning through the elements and finding the text that has "invite", find the text and then find it's button.
        4. The new member's email is 'rakohi5975@bulmp3.com'. Invite them.
        4. Confirm that the invitation was sent successfully.
        """

        # Run the agent
        result = agent_executor.invoke({
            "input": task_description
        })

        print("Agent run finished.")
        print(result)

    finally:
        print("Closing browser...")


run_agent()

