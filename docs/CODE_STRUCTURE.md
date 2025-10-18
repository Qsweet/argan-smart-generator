# 🧬 Argan Smart Generator - Code Structure & Data Flow

**Version:** 7.4  
**Last Updated:** 18 October 2025

---

## 1. Overview

This document provides a detailed breakdown of the project's code structure, key files, and the flow of data between different components. The application is primarily contained in `app.py`, with specialized logic in `pricing_planning.py`.

---

## 2. Main File: `app.py`

`app.py` is the heart of the application. It handles routing, UI rendering, and the logic for most of the features.

### 2.1. Core Components

| Component              | Description                                                                                             | Key Functions                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Imports & Setup**    | Imports necessary libraries (Streamlit, Pandas, etc.) and sets up the page configuration (`st.set_page_config`). | -                                                                                                           |
| **Styling**            | Injects custom CSS using `st.markdown` to achieve the application's unique visual style.                  | `local_css()`                                                                                               |
| **Authentication**     | Manages user login, logout, and session state. It checks credentials against `users.json`.                | `login()`, `check_password()`, `save_session()`, `load_session()`                                             |
| **Main Router (main)** | The central function that controls which page is displayed based on the user's login status and selection. | `main()`                                                                                                    |
| **Sidebar Navigation** | Renders the main navigation menu in the sidebar and handles page selection.                               | `st.sidebar...`                                                                                             |
| **Page Functions**     | Each feature/page is encapsulated in its own function, which is called by the `main()` router.            | `home_page()`, `admin_dashboard()`, `campaign_planner()`, `pricing_planning()`, `moraselaty_campaigns()`, etc. |

### 2.2. Data Flow in `app.py`

1.  **Application Start:** `main()` is called.
2.  **Session Check:** It checks if a user is logged in via `st.session_state`.
3.  **Login Page:** If not logged in, `login()` is displayed.
4.  **Authentication:** User enters credentials, which are checked against `users.json` by `check_password()`.
5.  **Successful Login:** User data is stored in `st.session_state`, and the `main()` function re-routes to the `home_page()`.
6.  **Navigation:** The user selects a page from the sidebar.
7.  **Page Display:** The `main()` function calls the corresponding page function (e.g., `pricing_planning()`).
8.  **Feature Logic:** The page function executes its logic, reading from and writing to relevant JSON files (e.g., `pricing_planning()` reads `products_pricing.json` and writes to `pricing_plans.json`).

---

## 3. Pricing Planner: `pricing_planning.py`

This file was created to encapsulate the complex logic of the "Pricing Planner" feature, keeping `app.py` cleaner.

### 3.1. Key Functions

| Function                    | Description                                                                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `pricing_planning()`        | The main entry point for the feature, called from `app.py`. It handles the overall layout and state.            |
| `load_pricing_plans()`      | Loads all saved pricing plans from `pricing_plans.json`.                                                      |
| `save_pricing_plans()`      | Saves the current state of pricing plans back to `pricing_plans.json`.                                        |
| `load_products_list()`      | Loads the master list of all available products from `products_pricing.json`.                                 |
| `get_product_pricing()`     | Retrieves the default pricing for a specific product from `products_pricing.json`.                            |
| `load_campaigns()`          | Loads the list of upcoming campaigns from `campaign_plans.json` (from the Campaign Planner section).          |
| `create_new_pricing_plan()` | Renders the UI for creating a new pricing plan, including product selection and price input.                |
| `get_ai_recommendations()`  | Sends the current pricing plan data to the OpenAI API and returns strategic pricing advice.                   |
| `export_to_excel()`         | Exports the selected pricing plan to a beautifully formatted Excel file with full Arabic support.             |

### 3.2. Data Flow in `pricing_planning.py`

1.  **User Enters Page:** `app.py` calls `pricing_planning()`.
2.  **Load Data:** The page immediately calls `load_pricing_plans()` and displays a list of existing plans.
3.  **Create New Plan:** User clicks "➕ خطة جديدة", which calls `create_new_pricing_plan()`.
4.  **Populate Dropdowns:** This function calls `load_products_list()` and `load_campaigns()` to populate the product and campaign selection dropdowns.
5.  **Add Product:** User selects a product. The UI automatically calls `get_product_pricing()` to fetch and display the base price.
6.  **User Input:** User adjusts prices (discount, coupon) and adds more products. All data is temporarily stored in `st.session_state.pricing_products`.
7.  **Save Plan:** User clicks "💾 حفظ الخطة". The data from `st.session_state` is formatted and appended to the main `pricing_plans` dictionary, which is then saved to `pricing_plans.json` by `save_pricing_plans()`.
8.  **AI Advice:** User clicks "🤖 الحصول على نصائح". The current plan's data is passed to `get_ai_recommendations()`, which returns a string of AI-generated advice.
9.  **Export:** User clicks "📊 تصدير Excel". The plan data is passed to `export_to_excel()`, which generates and offers an `.xlsx` file for download.

---

## 4. Data Storage (JSON Files)

The project uses a set of JSON files as a simple database. This makes the application portable and easy to manage without a database server.

-   **`users.json`**: Stores user credentials and roles.
-   **`campaign_plans.json`**: Stores campaigns created in the "📅 تخطيط الحملات" section.
-   **`products_pricing.json`**: The master database of all products and their default prices.
-   **`pricing_plans.json`**: Stores all pricing plans created in the "💰 تخطيط التسعير" section.
-   **`moraselaty_campaigns.json`**: Stores campaigns for the "حملات مراسلاتي" section.
-   **`moraselaty_customers.json`**: Stores customer data for Moraselaty.
-   **`revenue_data.json`**: Stores monthly revenue and expense data.

This structure, while simple, is the backbone of the application. **Any function that modifies data must follow the pattern: Read the JSON -> Modify the Python object -> Write the entire object back to the JSON.**

