import pandas as pd
from robocorp import browser
from llm_tools import find_element_selector
from langchain.tools import tool

# Configure browser to be headful for debugging
browser.configure(
    browser_engine="chrome",
    headless=False,
)

@tool
def login_to_trello(username: str, password: str) -> str:
    """
    A tool to log into Trello.
    It navigates to the login page, fills in the username and password,
    and handles the multi-step login process.
    """
    try:
        page = browser.goto("https://trello.com/login")
        page.wait_for_load_state('networkidle')

        # Step 1: Enter username
        username_selector = find_element_selector("The email or username input field")
        page.fill(username_selector, username)
        
        continue_button_selector = find_element_selector("The 'Continue' or 'Login' button")
        page.click(continue_button_selector)
        page.wait_for_timeout(2000) # Wait for password page to load

        # Step 2: Enter password
        password_selector = find_element_selector("The password input field")
        page.fill(password_selector, password)
        
        submit_button_selector = find_element_selector("The final 'Log in' or 'Submit' button")
        page.click(submit_button_selector)

        page.wait_for_load_state('networkidle')
        print("Successfully logged into Trello.")
        return "Login successful."
    except Exception as e:
        return f"Login failed: {e}"


@tool
def scrape_workspace_members(workspace_url: str, output_csv_path: str = "output/trello_users.csv") -> str:
    """
    A tool to navigate to a specific Trello workspace members page and scrape all member data.
    It extracts the name and username of each member and saves the data to a CSV file.
    """
    try:
        page = browser.page()
        page.goto(workspace_url)
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('[data-testid="workspace-member-list"]')

        member_cards = page.query_selector_all('[data-testid="workspace-member-list"]')
        user_data = []

        for card in member_cards:
            # The name and username are often in the title of the avatar
            avatar = card.query_selector('div[title]')
            if avatar:
                title_attr = avatar.get_attribute("title")
                # Example title: "Gemini Bot (geminibot123)"
                name = title_attr.split('(')[0].strip()
                username = title_attr.split('(')[-1].replace(')', '').strip()
                user_data.append({"name": name, "username": username})

        df = pd.DataFrame(user_data)
        df.to_csv(output_csv_path, index=False)
        print(f"Scraped {len(user_data)} users and saved to {output_csv_path}")
        return f"Successfully scraped {len(user_data)} users."
    except Exception as e:
        return f"Failed to scrape users: {e}"


@tool
def invite_user_to_workspace(email: str) -> str:
    """
    A tool to add a new user to the current Trello workspace by their email address.
    """
    try:
        temp = []
        page = browser.page()
        page.wait_for_load_state('networkidle')
        invite_button_selector = find_element_selector("The 'Invite' or 'Invite Workspace Members' button or class that has the same text")
        temp.append(invite_button_selector)
        page.click(invite_button_selector)

        email_input_selector = find_element_selector("The input field to add members by email")
        temp.append(email_input_selector)
        page.fill(email_input_selector, email)
        page.wait_for_timeout(1000)

        send_invite_selector = find_element_selector("The 'Send invite' or 'Add to Workspace' button")
        temp.append(send_invite_selector)
        page.click(send_invite_selector)
        page.wait_for_load_state('networkidle')

        print(temp)
        print(f"Successfully invited user: {email}")
        return f"Invitation sent to {email}."
    except Exception as e:
        return f"Failed to add user: {e}"


