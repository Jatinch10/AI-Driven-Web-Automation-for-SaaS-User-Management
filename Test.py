import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from llm_agent import locate_selector



async def scrape_users_and_manage():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")  
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://trello.com/login")  
         # or snippet around the table
        await page.wait_for_load_state('networkidle')
        # await page.wait_for_timeout(2000)
        html = await page.content() 

        # await page.wait_for_selector("form", timeout=10000)
        username_sel = locate_selector(html, "username")      
        # await page.fill('input[id="username-uid1"]', "example@mail.com")
        await page.fill(username_sel, "example@mail.com")
        button_sel = locate_selector(html, "login")
        # await page.click('button#login-submit')
        await page.click(button_sel)
        await page.wait_for_timeout(3000)

        pass_sel = locate_selector(html, "password")
        await page.fill(pass_sel, "PASSWORD")
        submit_sel = locate_selector(html, "submit")
        await page.click(submit_sel)
        await page.wait_for_timeout(2000)

        await page.wait_for_load_state('networkidle')
        # await page.wait_for_timeout(2000)
        # await page.wait_for_load_state('networkidle')
        # await page.wait_for_timeout(2000)
        html = await page.content() 
        print(html)

        await page.goto("https://trello.com/w/workspace/members") #Your Workspace link  

        await page.wait_for_load_state('networkidle')

        
        member_cards = await page.query_selector_all('div[data-testid="workspace-member-item"]')
        user_data = []

        for row in member_cards:
            name = await row.inner_text()  # Simplified; adjust selectors based on SaaS
            user_data.append({
                "name": name
            })

        # for row in member_cards:
        #     title = await row.get_attribute("title")
        #     user_data.append({
        #         "name": title
        #     })

        # for card in member_cards:
        #     # find the little div with the title attribute
        #     photo_div = await card.query_selector('div[title]')
        #     if not photo_div:
        #         continue
        
        #     title_attr = await photo_div.get_attribute("title")

        #     # extract just the username inside the parentheses
        #     import re
        #     m = re.search(r'\(([^)]+)\)', title_attr or "")
        #     username = m.group(1) if m else title_attr

        #     user_data.append({"username": username})

        print(user_data)
        df = pd.DataFrame(user_data)
        df.to_csv("user_data.csv", index=False)
        print(df)

        await page.click('button.Hm2Njssed7t23i.bxgKMAm3lq5BpA.SdamsUKjxSBwGb.SEj5vUdI3VvxDc')
        await page.fill('input[data-testid="add-members-input"]', 'example@mail.com')
        await page.keyboard.press("Enter")
        await page.click('button.C71gijCMxUFbvL.bxgKMAm3lq5BpA.SdamsUKjxSBwGb.PnEv2xIWy3eSui.SEj5vUdI3VvxDc')

        # await page.click('button[data-test-id="remove-user-button"]')
        await page.click('button:has-text("Remove…")')
        await page.click('a:has-text("Remove from Workspace")')

        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(scrape_users_and_manage())
