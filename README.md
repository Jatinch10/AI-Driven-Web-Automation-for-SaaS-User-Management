# AI‑Driven Web Automation for SaaS User Management

This repository contains two phases of development:

1. **Initial Coding Phase (Proof‑of‑Concept):** Basic Playwright + LLM integration to automate login, scrape, and provisioning on Trello.
2. **Main Coding Phase:** A modular framework using LangChain, Robocorp, and Playwright for scalable, agentic RPA workflows.

---

## Prerequisites

* **Python 3.10+**
* **Git**
* **[Playwright](https://playwright.dev/python/docs/intro)** (browsers installed)
* **[OpenRouter API Key](https://openrouter.ai/)** for DeepSeek models
* **.env file** with the following keys:

  ```dotenv
  OPENROUTER_API_KEY=your_openrouter_key
  ```
* **Robocorp CLI (`rcc`)** (for main phase): download [rcc.exe](https://robocorp.com/docs/rcc/installation)

---

## Phase 1: Initial Coding (Proof‑of‑Concept)

**Files:**

* `llm_agent.py`
* `Test.py`

### Setup & Run

1. Clone the repo and navigate into it:

   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows
   .\.venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install playwright openai pandas
   playwright install
   ```
4. Create a file named `.env` in the project root with your API key and Trello credentials (see Prerequisites).
5. Update `Test.py` and replace hardcoded placeholders with environment variables using `os.getenv('TRELLO_USERNAME')`, etc.
6. Run the proof‑of‑concept script:

   ```bash
   python Test.py
   ```

The script will open a browser, log into Trello, scrape workspace members, save `user_data.csv`, and demonstrate invite/remove actions via LLM‑generated selectors.

---

## Phase 2: Main Coding (Modular Agentic RPA)

**Files:**

* `llm_tools.py`
* `automation_tasks.py`
* `tasks.py`
* `robot.yaml` (Robocorp configuration)
* `conda.yaml` (Conda environment specification)

### Setup & Run

1. **Environment Setup**

   * (Optional) Use Conda:

     ```bash
     conda env create -f conda.yaml
     conda activate rpa-env
     ```
   * **OR** use `pip`:

     ```bash
     python -m venv .venv
     source .venv/bin/activate  # or .\.venv\Scripts\activate
     pip install --upgrade pip
     pip install langchain playwright rpaframework openai pandas
     playwright install
     ```
2. Copy your `.env` file (with API key and Trello credentials) into the project root.
3. **Robocorp Configuration**

   * Ensure `rcc.exe` is installed and available in your PATH.
   * Run the RPA project:

     ```powershell
     rcc run
     ```

   This will execute the `robot.yaml` workflow, which:

   * Logs into Trello via a LangChain‑driven AgentExecutor
   * Scrapes workspace members and saves `trello_users.csv`
   * Attempts to invite and remove a user via Robocorp tools

---

## Project Structure

```
├── llm_agent.py             # Initial LLM selector helper
├── Test.py                  # Proof‑of‑Concept script
├── llm_tools.py             # LLM selector tool for main phase
├── automation_tasks.py      # Robocorp RPA tools (login, scrape, invite, remove)
├── tasks.py                 # LangChain AgentExecutor setup
├── robot.yaml               # Robocorp project definition
├── conda.yaml               # Conda environment spec (optional)
├── .env                     # Your credentials & API key (not committed)
└── README.md                # This file
```

---

## Notes

* **Customization:** To target a different SaaS portal, update the URL and element descriptions in `automation_tasks.py` and adjust `find_element_selector` prompts.
* **Rate Limits:** DeepSeek free tier has limited calls (≈50/day). Caching selectors or batching prompts is recommended.
* **Unresolved Issues:** CAPTCHA/MFA flows require integration with an external solver or manual challenge handling.

---

### License

MIT License
