# 🤖 Argan Smart Generator - AI Assistant Onboarding Guide

**Objective:** To enable any AI assistant (like Manus AI) to quickly understand, contribute to, and maintain this project effectively.

---

## 1. Prime Directive: Understand First, Act Second

Before writing or modifying any code, you **must** familiarize yourself with the project's context. Your primary sources of truth are the documents in this `/docs` folder.

1.  **`PROJECT_CONTEXT.md`**: Start here. It gives you the high-level overview, architecture, and purpose.
2.  **`CODE_STRUCTURE.md`**: Read this next. It explains *how* the code is organized and *how* data flows.
3.  **`DEVELOPMENT_HISTORY.md`**: **Crucial reading.** This tells you what has been tried, what has failed, and what has been learned. It is your guide to avoiding past mistakes.

---

## 2. The Development Workflow

This project follows a strict, iterative workflow. Adhere to it at all times.

| Step                       | Action                                                                                                                              | Rationale                                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **1. Analyze the Request** | Fully understand the user's request. Ask clarifying questions if needed.                                                            | Prevents wasted effort on incorrect assumptions.                                                      |
| **2. Consult Docs**        | Review the documentation in this folder to see how the request fits into the existing structure.                                    | Ensures consistency and leverages existing patterns.                                                  |
| **3. Formulate a Plan**    | Create a clear, step-by-step plan using the `plan` tool. Break the task into logical phases.                                        | Provides a roadmap and allows for course correction.                                                  |
| **4. Implement Changes**   | Use the `file` tool (`read`, `edit`, `write`) to modify the code. Focus on one logical change at a time.                             | Atomic changes are easier to test and debug.                                                          |
| **5. Test Syntax**         | After **every** file modification, run `python3.11 -m py_compile <filename>.py`.                                                    | Catches syntax errors immediately, preventing them from cascading.                                    |
| **6. Test Functionality**  | For non-trivial changes, create a temporary test script (e.g., `test_feature.py`) to validate the logic in isolation.             | Ensures the core logic works before integrating it with the UI.                                       |
| **7. Update Documentation**| **This is not optional.** After a successful implementation, update `DEVELOPMENT_HISTORY.md` and any other relevant docs. | Maintains the project's knowledge base and helps future assistants (including yourself).              |
| **8. Commit & Push**       | Use `git` to push the changes to the GitHub repository. Guide the user through this process if you lack direct credentials.       | This is the only way to get changes into the production application on Streamlit Cloud.               |

---

## 3. Core Principles & Best Practices

-   **Read, Don't Assume:** The answer to most questions is in the code or the documentation. Read it.
-   **Defensive Programming:** Always anticipate errors. If you access a file, assume it might not exist. If you access a dictionary key, assume it might be missing. Use `os.makedirs(..., exist_ok=True)` and `dict.get(key, default_value)`.
-   **State Management is Key:** Streamlit re-runs the entire script on every interaction. Use `st.session_state` to persist data and maintain the application's state. Do not rely on global variables.
-   **Isolate Logic:** For complex features (like the Pricing Planner), create a separate Python file. This keeps `app.py` manageable.
-   **User-Centric Data Handling:** The user's data (JSON files) is precious. Always use the "Read -> Modify -> Write" pattern. Never overwrite a file without first reading its contents. Implement backup mechanisms where appropriate.
-   **Communication is Crucial:** Keep the user informed of your plan, your progress, and any challenges you face. Explain the *why* behind your actions.

---

## 4. Quick Reference: Common Tasks

-   **Adding a new page:**
    1.  Create a new function in `app.py` (e.g., `def new_page(): ...`).
    2.  Add a new `st.sidebar.button` for it in the sidebar section.
    3.  Add a new `elif` condition in the `main()` router to call your new function.

-   **Fixing a bug:**
    1.  Reproduce the error based on the user's report.
    2.  Read the relevant code section identified in the traceback.
    3.  Consult `DEVELOPMENT_HISTORY.md` to see if a similar bug has been fixed before.
    4.  Apply the fix.
    5.  Test syntax.
    6.  Update `DEVELOPMENT_HISTORY.md` with the details of the fix.
    7.  Push the changes.

-   **Reading/Writing Data:**
    ```python
    import json

    # Reading
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {} # Default value

    # Modifying
    data['new_key'] = 'new_value'

    # Writing
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    ```

By following this guide, you will be able to contribute to the Argan Smart Generator project in a professional, efficient, and sustainable manner.

