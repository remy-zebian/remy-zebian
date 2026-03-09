ExpensesTracker

Video Demo: https://youtu.be/HDFsAKcYC-Y

Description

    ExpensesTracker is a command-line financial management system that allows users to securely create accounts, track expenses, set monthly budgets, and generate professional PDF summaries with visual analytics. The project integrates authentication, structured data storage, financial computation, and automated report generation into a cohesive and practical application.
    The system is divided into two main components: a secure user account system and a financial tracking/reporting engine. User credentials are stored securely using Argon2 password hashing via the argon2-cffi library. Passwords are never saved in plain text. Instead, they are hashed and verified using modern cryptographic standards, ensuring account security.
    User data is stored in two persistent files:
    •	users_info.json — stores usernames, hashed passwords, and budget history.
    •	data.csv — stores all expense transactions, including user, category, description, cost, and date.

Account Management

    The program begins with a user account system. Users can:
    •	Sign in
    •	Create a new account
    •	Delete an existing account (including all associated expense history)
    •	View all registered usernames
    Account verification is handled inside the Account class. Password hashing and verification are implemented using Argon2. When an account is deleted, all related financial records are removed from the CSV file to maintain consistency.

Expense Tracking

    Once authenticated, users can:
    1. Enter new expenses
    2. Show financial summaries (generate PDF)
    3. Set a monthly budget
    Expenses are categorized into predefined groups such as Housing, Food, Transportation, Health, Education, Technology, and others. The system supports alternative category aliases (for example, “Tech” maps to “Technology”). Each expense includes a description, cost, and automatic date assignment.
    Data is dynamically reorganized into a structured hierarchy (Year → Month → Category → Description) using the organize_data() function. This enables efficient aggregation and reporting.

Budget System

    Users can set a monthly budget. The program checks whether a budget exists for the current month and warns the user if a new budget is required.
    The check_budget() function compares the percentage of budget spent to the expected daily spending pace. Based on this comparison, the program prints feedback messages such as:
    •	“You barely spent any money!”
    •	“Your spendings are normal.”
    •	“Your expenses are too high!”
    This feature provides real-time financial behavior analysis rather than simple tracking.

PDF Generation & Visualization

    One of the most advanced parts of the project is automated PDF generation.
    The custom PDF class extends FPDF and includes:
    •	Custom footer with dynamic page numbering
    •	Cover page
    •	Table of contents with internal navigation links
    •	Year summary pages
    •	Month summary pages
    •	Category breakdown pages
    •	Embedded graphs and bar charts
    The system generates:
    •	Line graphs comparing monthly budgets vs expenses
    •	Bar charts displaying expense distribution by category
    •	Summary statistics (total expenses, remaining balance, number of transactions)
    Graphs are created using matplotlib and stored temporarily in memory using BytesIO before being inserted into the PDF.
    The final report is exported as:
    summary.pdf
    This PDF includes structured navigation links between sections, making it interactive and professional.

Design Decisions

    Several important design choices were made:
    •	Argon2 was selected for password hashing due to its security strength.
    •	JSON was used for structured user data storage.
    •	CSV was chosen for expense records for simplicity and tabular structure.
    •	Matplotlib was integrated to provide visual analytics rather than only textual summaries.
    •	The PDF class was customized to improve layout control and formatting.
    Additionally, comparisons between current and previous month category spending were implemented to calculate percentage increases or decreases. Special cases such as division by zero and missing budgets are handled carefully to avoid runtime errors.

Conclusion

    ExpensesTracker is a fully functional financial tracking system combining secure authentication, structured data management, financial analysis, visual analytics, and professional PDF reporting. The project demonstrates object-oriented programming, file handling, data aggregation, visualization, and document automation within a single cohesive application.
    This system is not just a simple tracker; it is a complete reporting engine designed to simulate real-world financial management software.

