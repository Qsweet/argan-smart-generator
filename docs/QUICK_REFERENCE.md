# ⚡ Argan Smart Generator - Quick Reference

**Objective:** A cheat sheet for developers and AI assistants for common tasks and commands.

---

## 📁 File Locations

| Item                      | Location                                      |
| ------------------------- | --------------------------------------------- |
| **Main Application**      | `app.py`                                      |
| **Pricing Logic**         | `pricing_planning.py`                         |
| **User Data**             | `users.json`                                  |
| **Product Database**      | `products_pricing.json`                       |
| **Campaign Plans**        | `campaign_plans.json`                         |
| **Pricing Plans**         | `pricing_plans.json`                          |
| **Moraselaty Campaigns**  | `moraselaty_campaigns.json`                   |
| **Python Dependencies**   | `requirements.txt`                            |
| **This Documentation**    | `docs/`                                       |

---

## 🛠️ Common Commands

-   **Check Python Syntax:**
    ```bash
    python3.11 -m py_compile <filename>.py
    ```

-   **Run the Application (Locally):**
    ```bash
    streamlit run app.py
    ```

-   **List All Files:**
    ```bash
    ls -R
    ```

-   **Find Text in Files:**
    ```bash
    grep -r "your_text_here" .
    ```

---

## ✨ Git Workflow (Pushing Updates)

1.  **Stage Changes:**
    ```bash
    git add <file1> <file2> ...
    # or to add all changes:
    git add -A
    ```

2.  **Commit Changes:**
    ```bash
    git commit -m "Your descriptive message here"
    ```

3.  **Push to GitHub:**
    ```bash
    git push origin main
    ```

---

## 🐛 Common Errors & Solutions

-   **`UnboundLocalError`**
    -   **Cause:** A variable was used before it was assigned a value in all possible code paths (e.g., defined in an `if` but used outside it).
    -   **Solution:** Initialize the variable with a default value (`None`, `0`, `[]`) at the top of the function scope.

-   **`AttributeError` / `NameError` after UI interaction**
    -   **Cause:** Streamlit re-ran the script, and the variable, which was defined in a previous run, is no longer in scope.
    -   **Solution:** Use `st.session_state` to store the variable. It persists across re-runs.
        -   **Writing:** `st.session_state.my_variable = "some_value"`
        -   **Reading:** `value = st.session_state.get("my_variable")`

-   **`FileNotFoundError`**
    -   **Cause:** The code tried to read a file that doesn't exist, especially common in a new or reset environment.
    -   **Solution:** Use a `try...except FileNotFoundError` block to handle the case where the file is missing and create it or use a default value.

-   **Feature Not Appearing in Deployed App**
    -   **Cause:** The code changes have not been pushed to the GitHub repository linked to the Streamlit Cloud app.
    -   **Solution:** Follow the Git Workflow above to `add`, `commit`, and `push` your changes.

-   **`git push` fails with authentication error**
    -   **Cause:** Git needs to authenticate with GitHub. The user has not configured credentials.
    -   **Solution:** Guide the user to create a Personal Access Token (PAT) with `repo` scope and use it to push.

