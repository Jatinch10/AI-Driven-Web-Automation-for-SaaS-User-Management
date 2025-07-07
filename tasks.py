import os
from robocorp.tasks import task
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from automation_tasks import login_to_trello, scrape_workspace_members, invite_user_to_workspace
from llm_tools import find_element_selector

# Define the tools the agent can use
tools = [
    login_to_trello,
    scrape_workspace_members,
    invite_user_to_workspace,
    find_element_selector
]


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


@task
def run_agent():
    """
    Initializes and runs the LangChain agent with AI-powered, resilient tools.
    """
    try:
        # Initialize the LLM for the agent
        agent_llm = ChatOpenAI(
            model="YOUR LLM MODEL",
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
        1. First, please log me into Trello. My username is 'example@mail.com' and my password is 'PASSWORD'.
        2. After you've logged in, wait for two seconds then go to the workspace members page, which is at 'https://trello.com/w/YOUR WORKSPACE/members'.
        3. On the members page, find a way to invite a new member by scanning through the elements and finding the text that has "invite", find the text and then find it's button.
        4. The new member's email is 'example@mail.com'. Invite them.
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

