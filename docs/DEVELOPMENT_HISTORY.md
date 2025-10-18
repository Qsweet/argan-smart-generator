# 📜 Argan Smart Generator - Development History & Problem-Solving Log

**Version:** 7.4  
**Last Updated:** 18 October 2025

---

## 1. Introduction

This document is a living log of the development journey of the Argan Smart Generator. It chronicles every significant bug, challenge, and enhancement, detailing the problem, the investigation process, the final solution, and the key lessons learned. Its purpose is to provide context for future development and to prevent repeating past mistakes.

Any AI assistant or developer working on this project should consult this file first to understand the "why" behind the code's current state.

---

## 2. Development Log

### **v7.4 (18 Oct 2025): The `datetime.now()` Fix**

-   **Problem:** An `AttributeError: module 'datetime' has no attribute 'now'` was reported in the "Moraselaty Campaigns" section. The error was caused by an incorrect call to the `datetime` library.
-   **Investigation:** A project-wide search (`grep`) revealed 16 instances where `datetime.now()` was used instead of the correct `datetime.datetime.now()`. This was a recurring issue that needed a definitive fix.
-   **Solution:** A global find-and-replace was performed to change all occurrences of `datetime.datetime.now().datetime.now()` (a result of a previous faulty fix) and `datetime.now()` to the correct `datetime.datetime.now()`.
-   **Key Takeaway:** When fixing a recurring error, perform a global search to eradicate all instances of the bug. A partial fix will only lead to future failures.

### **v7.2 & v7.3 (16-17 Oct 2025): Fixing the Pricing Planner**

-   **Problem:** The newly created "Pricing Planner" had two major issues: 1) The product dropdown was empty. 2) It was loading the wrong list of campaigns.
-   **Investigation:**
    1.  **Product List:** The code was not reading from any product database. The user provided an Excel file (`Bo22ok1.xlsx`) with all products and prices.
    2.  **Campaign List:** The `load_campaigns()` function was hardcoded to read from `moraselaty_campaigns.json` instead of `campaign_plans.json`, which is where the "Campaign Planner" saves its data.
-   **Solution:**
    1.  The Excel file was converted into a structured `products_pricing.json` file.
    2.  The `pricing_planning.py` module was updated to:
        -   Load the product list from `products_pricing.json`.
        -   Automatically fill the base price when a product is selected.
        -   Change the `load_campaigns()` function to read from `campaign_plans.json` and filter for only active, non-deleted campaigns.
-   **Key Takeaway:** Features must be integrated with the correct data sources. Hardcoded paths or assumptions about data locations lead to brittle code.

### **v7.0 (15 Oct 2025): Deployment & Git Challenges**

-   **Problem:** After implementing the Pricing Planner, the new feature was not visible in the user's deployed Streamlit Cloud application, despite the code being correct in the development environment.
-   **Investigation:** The root cause was a misunderstanding of the deployment workflow. Changes made in the local sandbox are not automatically reflected in the production app. They must be pushed to the linked GitHub repository first.
-   **Solution:**
    1.  Guided the user on how to use `git` to `add`, `commit`, and `push` changes.
    2.  When authentication failed, guided the user to create a GitHub Personal Access Token (PAT).
    3.  Used the PAT to successfully push the updates to the `main` branch.
    4.  Resolved several `git pull` conflicts caused by divergent histories between the local and remote repositories.
-   **Key Takeaway:** The development-to-production workflow is critical. **Code -> Test -> Commit -> Push -> Deploy.** Any AI assistant must understand this cycle and be prepared to guide the user through it.

### **v6.0 & v6.1 (14 Oct 2025): Data Persistence & The Recurring `inventory_files` Bug**

-   **Problem:** The user reported losing all their data (campaigns, etc.) with every update. A related `UnboundLocalError` also kept appearing in the admin dashboard, related to the `inventory_files` directory.
-   **Investigation:** Both issues stemmed from the ephemeral nature of the sandbox environment. The `inventory_files` directory and all other data files were being deleted upon every restart.
-   **Solution:**
    1.  **Data Loss:** Implemented a "Backup & Restore" feature directly in the admin dashboard. This feature uses a helper script (`backup_utility.py`) to create a ZIP archive of all critical JSON files, which the user can download and re-upload after an update.
    2.  **`inventory_files` Bug:** The definitive fix was to add `os.makedirs("inventory_files", exist_ok=True)` at the beginning of the `admin_dashboard()` function. This ensures the directory is *always* created before it is accessed, completely eliminating the error.
-   **Key Takeaway:** Never assume a file or directory exists in an ephemeral environment. Always create it defensively (`exist_ok=True`). Provide users with a mechanism to persist their data across sessions.

### **v5.8 & v5.9 (13 Oct 2025): State Management & Scope Issues**

-   **Problem:** Two critical errors appeared: an `UnboundLocalError` in `create_moraselaty_campaign` and an `AttributeError` when saving an AI-generated marketing campaign.
-   **Investigation:** Both errors were caused by issues with variable scope and Streamlit's execution model.
    1.  **UnboundLocalError:** `min_price` and `max_price` were defined inside an `if` block but used later, outside of it.
    2.  **AttributeError:** Campaign data (like `selected_products`, `campaign_idea`) was defined within a tab, but the "Save" button was outside the tab. When the button was pressed, Streamlit re-ran the script, and the variables were no longer in scope.
-   **Solution:**
    1.  Initialized `min_price` and `max_price` to `0.0` at the top of the function.
    2.  Used `st.session_state` to store the campaign data. When the data was generated, it was saved to `st.session_state.campaign_data`. The "Save" button then read the data from the session state, which persists across script re-runs.
-   **Key Takeaway:** `st.session_state` is the primary tool for managing state in Streamlit. Use it to pass data between different parts of the UI and to persist information across user interactions and script re-runs.

-reruns.

