# 🧠 Argan Smart Generator - Project Context

**Version:** 7.4  
**Last Updated:** 18 October 2025  
**Author:** Manus AI for Dr. Mohammed Al-Qudah

---

## 🎯 1. Project Overview

**Argan Smart Generator** is an advanced Streamlit-based web application designed to automate and enhance marketing and content creation for the **Argan Package** company. It provides a comprehensive suite of tools for managing customers, generating marketing scenarios, planning campaigns, and analyzing revenue.

### 1.1. Core Objectives

- **Automation:** Automate repetitive marketing tasks.
- **Intelligence:** Leverage AI (OpenAI GPT-4) to generate creative content and provide strategic insights.
- **Centralization:** Provide a single platform for managing all marketing-related data.
- **Efficiency:** Streamline workflows for campaign planning, pricing, and revenue tracking.

### 1.2. Key Features

- **User Authentication:** Secure login system with roles (Admin, User).
- **Dashboard:** A central hub displaying key metrics and quick actions.
- **Scenario Generation:** AI-powered tool to create marketing scenarios for different products and platforms.
- **Campaign Planning:** A calendar-based system to plan and manage marketing campaigns.
- **Pricing Planner:** An advanced tool for creating and analyzing pricing strategies for campaigns, with AI-powered recommendations.
- **Revenue Tracking:** A module to track monthly expenses and revenues.
- **Moraselaty Campaigns:** A dedicated section for creating and managing campaigns for the Moraselaty platform.
- **Admin Dashboard:** A control panel for managing users, data, and system settings.

---

## 🏗️ 2. Project Architecture

The project is a monolithic Streamlit application. All logic is contained within a single main file (`app.py`) and several helper modules.

### 2.1. Technology Stack

- **Framework:** Streamlit
- **Language:** Python 3.11
- **AI:** OpenAI GPT-4 API
- **Data Storage:** JSON files (for simplicity and portability)
- **Styling:** Custom CSS injected via `st.markdown`

### 2.2. File & Directory Structure

```
/argan-smart-generator
│
├── 📄 app.py                     # Main application file (contains all UI and logic)
├── 📄 pricing_planning.py        # Logic for the Pricing Planner section
├── 📄 requirements.txt           # Python dependencies
│
├── 📁 data/                      # (Proposed) To store all JSON data files
│   ├── 📄 users.json             # User credentials
│   ├── 📄 moraselaty_customers.json # Customer data for Moraselaty
│   ├── 📄 moraselaty_campaigns.json # Moraselaty campaigns
│   ├── 📄 campaign_plans.json     # Campaign plans from the planner
│   ├── 📄 products_pricing.json   # Product pricing database
│   ├── 📄 pricing_plans.json      # Saved pricing plans
│   └── 📄 revenue_data.json       # Monthly revenue data
│
├── 📁 docs/                      # (This documentation system)
│   ├── 📄 PROJECT_CONTEXT.md      # This file
│   ├── 📄 CODE_STRUCTURE.md     # Detailed code explanation
│   ├── 📄 DEVELOPMENT_HISTORY.md  # Log of all changes and fixes
│   └── 📄 AI_ASSISTANT_GUIDE.md   # Guide for AI assistants
│
├── 📁 backups/                   # Stores user-generated data backups
├── 📁 campaign_logos/            # Logos uploaded for campaigns
└── 📁 inventory_files/           # Excel files for inventory updates
```

---

## 🔄 3. How to Update & Modify (Quick Guide)

This guide is for developers and AI assistants to understand the modification workflow.

### 3.1. Development Environment

The application is developed in a sandboxed environment. All changes are made directly to the files in the `/home/ubuntu/argan-smart-generator/` directory.

### 3.2. Typical Workflow

1.  **Identify the Target:** Determine which section of the application needs modification (e.g., "Pricing Planner", "Admin Dashboard").
2.  **Locate the Code:**
    - Most UI and logic is in `app.py`, organized into functions corresponding to pages (e.g., `admin_dashboard()`, `pricing_planning()`).
    - Specific, complex logic might be in a separate file (e.g., `pricing_planning.py`).
3.  **Make Changes:**
    - Use the `file` tool to `read`, `edit`, or `write` files.
    - For UI changes, modify the Streamlit components (`st.button`, `st.text_input`, etc.).
    - For logic changes, modify the Python code.
4.  **Test Syntax:**
    - After every change, run `python3.11 -m py_compile <filename>.py` to ensure there are no syntax errors.
5.  **Test Functionality:**
    - Create a separate test script (e.g., `test_my_feature.py`) to test the new logic.
    - Run the application (`streamlit run app.py`) to test the UI and user flow.
6.  **Document Changes:**
    - **Crucially**, update the documentation in the `docs/` folder, especially `DEVELOPMENT_HISTORY.md`.
7.  **Commit & Push:**
    - Use `git add`, `git commit`, and `git push` to upload the changes to the GitHub repository.
    - Always use a descriptive commit message.

### 3.3. Key Principles

- **Modularity:** Keep functions small and focused on a single task.
- **Data-Driven:** Load data from JSON files, don't hardcode it.
- **User Experience:** Use Streamlit components creatively to provide a clean and intuitive UI.
- **Robustness:** Always handle potential errors (e.g., file not found, invalid data) with `try...except` blocks.

---

## 🚀 4. Next Steps & Future Improvements

- **Refactor to a Multi-Page App:** Convert the single `app.py` into a multi-page Streamlit application for better organization.
- **Database Migration:** Migrate from JSON files to a proper database (like SQLite or PostgreSQL) for better performance and data integrity.
- **Modularize Code:** Break down `app.py` into smaller, more manageable modules (e.g., `auth.py`, `ui_components.py`).
- **Improve State Management:** Rely more on `st.session_state` for a more robust user experience.

This document provides the foundational knowledge needed to understand and contribute to the Argan Smart Generator project. For more detailed information, refer to the other documents in this `docs` folder.

