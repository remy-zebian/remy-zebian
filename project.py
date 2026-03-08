from argon2 import PasswordHasher
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import *
from fpdf import FPDF
import calendar
import string
import json
import csv
import sys


def main():
    account_menu= {
        "1": ("Sign In", sign_in),
        "2": ("Create Account", create_account),
        "3": ("Delete Account", delete_account),
        "4": ("View All Accounts", view_accounts)
    }

    while True:
        print("=== User Account System ===")
        for number, (function, _) in account_menu.items():
            print(f"{number}. {function}")
        print("5. Exit\n")

        try:
            choice= input("Enter your choice: ").strip()
        except KeyboardInterrupt:
            continue

        if choice in account_menu:
            if account_menu[choice][1]():
                break
            else:
                continue

        elif choice == "5":
            sys.exit("\nExiting program...")

        else:
            print("\nInvalid choice! Try again.\n")


punctuations= list(string.punctuation)
ph = PasswordHasher()


def get_data_j():
    with open("users_info.json") as file:
        return json.load(file)

def store_data_j(old_users_info):
    with open("users_info.json", "w") as file:
        json.dump(old_users_info, file, indent=2)

def get_expenses():
    with open("data.csv") as file:
        reader= csv.DictReader(file)
        return [row for row in reader]


class Account:
    def __init__(self, username, password):
        self.username= username
        self.password= password

    def __str__(self):
        return f'username: "{self.username}" and password: "{self.password}"'


    @property
    def verify_infos(self):
        old_users_info= get_data_j()

        for _, list in old_users_info.items():
            for dict in list:
                if self.username == dict["username"]:
                    try:
                        ph.verify(dict["password"], self.password)
                    except:
                        pass
                    else:
                        print(f"\nHello, {self.username}")
                        return True

        print("Incorrect username or password!\n")
        return False


    @property
    def store_data(self):
        old_users_info= get_data_j()
        old_usernames= [dict["username"] for _, list in old_users_info.items() for dict in list]

        if self.username in old_usernames or len(self.username) < 3 :
            print("Username unavailable! Try another one.\n")
            return False

        else:
            hash= ph.hash(self.password)
            old_users_info["usernames"].append({"username":self.username, "password":hash})

            store_data_j(old_users_info)

            print("\nPlease reenter your infos to acces the program.\n")
            return False

    @property
    def check_infos(self):
        old_users_info= get_data_j()

        for _, list in old_users_info.items():
            for dict in list:
                if self.username == dict["username"]:
                    try:
                        ph.verify(dict["password"], self.password)
                        list.remove(dict)
                        print("This account was deleted.\n")

                        store_data_j(old_users_info)
                        return False
                    except:
                        pass

        print("Incorrect username or password!\n")
        return False



def sign_in():
    global username
    username= input("Enter username: ").strip()
    password= input("Enter password: ").strip()

    account= Account(username, password)
    return account.verify_infos


def create_account():
    new_username= input("\nEnter your new username: ").strip()
    new_password= input("Enter your new password: ").strip()
    if len(new_password) < 4:
        print("Password must be more that 4 characters!\n")
        return False

    new_account= Account(new_username, new_password)
    print(f"{new_account}\n")

    while True:
        confirmation= input("Are you sure you want to continue? (yes or no) ").strip().lower()

        if not confirmation in ["yes", "no"]:
            print("Invalid choice!\n")
            continue
        else:
            break

    if confirmation == "yes":
        return new_account.store_data

    elif confirmation == "no":
        print()
        return False


def delete_account():
    r_username= input("Enter username: ").strip()
    r_password= input("Enter password: ").strip()

    r_account= Account(r_username, r_password)
    print(f"{r_account}\n")
    while True:
        confirmation= input("Are you sure you want to remove this account? (yes or no) ").strip().lower()

        if not confirmation in ["yes", "no", "noo"]:
            print("Invalid choice!\n")
            continue
        else:
            break
    if confirmation == "yes":
        while True:
            confirmation2= input("WARNING: This action will permanentely delete all your expenses history. Are you sure you want to continue? ").strip().lower()

            if not confirmation2 in ["yes", "no", "noo"]:
                print("Invalid choice!\n")
                continue
            else:
                break
        if confirmation2 == "yes":
            reader= get_expenses()
            new_data= sorted([{"Users": row["Users"], "Categories": row["Categories"], "Descriptions": row["Descriptions"], "Cost": row["Cost"], "Dates": row["Dates"]} for row in reader if row["Users"] != r_username], key= lambda x: x["Users"])

            with open("data.csv", "w") as file:
                writer= csv.DictWriter(file, fieldnames= ["Users", "Categories", "Descriptions", "Cost", "Dates"])
                writer.writeheader()
                for row in new_data:
                    writer.writerow(row)

            return r_account.check_infos

        elif confirmation2 == "no":
            print()
            return False

    elif confirmation == "no":
        print()
        return False


def view_accounts():
    old_users_info= get_data_j()

    print("\n--- All users ---")
    for _, list in old_users_info.items():
        for dict in list:
            print(f"- {dict["username"]}")
    print()
    return False

if __name__ == "__main__":
    main()


def new_expense():
    categories= {
        "Housing": ["🏠", True], "Food": ["🍔", True], "Transportation": ["🚗", True], "Health": ["🏥", True], "Education": ["🎓", True],"Personal": ["👕", True],
        "Entertainment": ["🎮", True], "Technology": ["📱", True], "Travel": ["🧳", True], "Bills & Financial": ["🧾", True], "Work & Business": ["💼", True],
        "Other": ["🧩", True], "Bills": ["Bills & Financial", False], "Financial": ["Bills & Financial", False], "Work": ["Work & Business", False],
        "Others": ["Other", False], "Business": ["Work & Business", False], "Tech": ["Technology", False], "Prsnl": ["Personal", False], "House": ["Housing", False]
         }

    print("Categories:")
    for cat, i in categories.items():
        if cat == "Bills":
            break
        print(f"{i[0]} {cat}")

    while True:
        try:
            category= input("Enter category name: ").strip().capitalize()
            if category in categories:
                if categories[category][1] is False:
                    category= categories[category][0]

            else:
                print("Please enter a valid category.")
                continue
            while True:
                description= input("Enter a description: ").strip().capitalize()
                if not description:
                    print("Please enter a valid description.")
                    continue
                break
            while True:
                try:
                    cost= float(input("Enter cost: "))
                    if cost <= 0:
                        print("Please enter a valid cost.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid cost.")
            break

        except KeyboardInterrupt:
            print("\nInvalid entry!")
            pass

    while True:
        confirmation= input("Are you sure to continue? ").lower().strip()
        if confirmation in ["yes", "yess","yesss", "sure"]:
            with open("data.csv", "a") as file:
                writer= csv.DictWriter(file, fieldnames= ["Users", "Categories", "Descriptions", "Cost", "Dates"])
                writer.writerow({"Users": username, "Categories": [category], "Descriptions": [description], "Cost": round(cost, 2), "Dates": date.today()})
                break
        elif confirmation in ["no", "noo"]:
            break
        print("Invalid entry!")


def organize_data():
    user_info= [dict for _, list in get_data_j().items() for dict in list if dict["username"] == username]
    budget= False if user_info[0].get("budget", False) is False else user_info[0]["budget"]
    expenses= [row for row in get_expenses() if row["Users"] == username]

    organized= list()
    for dict in expenses:
        new_category= dict["Categories"][2:-2]
        new_description= dict["Descriptions"][2:-2]
        new_cost= dict["Cost"]
        new_year= dict["Dates"][:4]
        new_month= dict["Dates"][5:7]
        if not organized:
            organized.append({"year": new_year,
                              "months":[{"month": new_month,
                                         "Categories": [{"category": new_category,
                                                         "description": [{"desc": new_description,
                                                                          "cost": new_cost}]}]}]})
            continue

        all_years= set([years["year"] for years in organized])
        if new_year in all_years:
            for years in organized:
                if years["year"] == new_year:
                    all_months= [months["month"] for months in years["months"]]
                    if new_month in all_months:
                        for months in years["months"]:
                            if months["month"] == new_month:
                                all_categories= [category["category"] for category in months["Categories"]]
                                if new_category in all_categories:
                                    for category in months["Categories"]:
                                        if category["category"] == new_category:
                                            category["description"].append({"desc": new_description,
                                                                            "cost": new_cost})

                                else:
                                    months["Categories"].append({"category": new_category,
                                                                 "description": [{"desc": new_description,
                                                                                  "cost": new_cost}]})
                    else:
                        years["months"].append({"month": new_month,
                                                "Categories": [{"category": new_category,
                                                                "description": [{"desc": new_description,
                                                                                 "cost": new_cost}]}]})

        else:
            organized.append({"year": new_year,
                              "months":[{"month": new_month,
                                         "Categories": [{"category": new_category,
                                                         "description": [{"desc": new_description,
                                                                          "cost": new_cost}]}]}]})

    return organized, budget, expenses


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=11)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align= "C")

    def prepare_pdf(self):
        self.set_title("Expenses Summary")
        self.set_margin(15)
        self.set_auto_page_break(True, 15)
        self.add_page()
        self.set_font("Helvetica", "B", 50)
        self.set_y(self.h/2)
        self.cell(0, text="Expenses Summary", align= "C")

    def print_toc(self, titles, links):
        self.add_page()
        self.set_font("Helvetica", "BU", 30)
        self.cell(0, text="Table Of Contents", align= "C")
        self.ln()
        for ym in titles:
            if ym[0] == "year":
                self.ln(10)
                self.set_x(15)
                self.line(15, self.get_y(), self.w - 15, self.get_y())
                self.ln()
                self.set_font("Helvetica", "B", 22)
                self.cell(0, text= ym[1][1], new_y= "NEXT", link= links[ym[1]])
            elif ym[0] == "month":
                self.set_x(35)
                self.set_font("Helvetica", size= 16)
                self.cell(0, text= datetime(1, int(ym[1][1]), 1).strftime("%B"), new_y= "NEXT", link= links[ym[1]])

    def print_year(self, year, links):
        self.add_page()
        self.set_link(links[(None, year)])
        self.set_left_margin(15)
        self.set_text_color(0, 0, 255)
        self.set_font("Helvetica", "B", 100)
        self.set_y(self.h/2)
        self.cell(0, text= year, align= "C")
        self.set_text_color(0, 0, 0)

    def print_year_summary(self, data):
        expense, budget, r_b, nb_transactions, date= organize_values(data)

        infos= [
            ["Total Budgets:  ", budget],
            ["Total Expenses:  ", expense],
            ["Remaining Balance:  ", r_b],
            ["Number of Transactions:  ", nb_transactions]
            ]
        if budget[-1:] == ")":
            infos[0].pop()
            infos[0]+= budget.split("^")
        if expense[-1:] == ")":
            infos[1].pop()
            infos[1]+= expense.split("^")

        self.add_page()
        self.set_margin(15)
        self.set_font("Helvetica", "B", 35)
        self.cell(0, text= f"{date} Summary", align= "C")
        self.ln(25)
        for info in infos:
            self.set_font("Helvetica", "B", 16)
            self.cell(self.get_string_width(info[0]), text= info[0])
            self.set_font("Helvetica", "I", 13)

            if info[1][0] == "-" or info[1][-1] == "!":
                self.set_text_color(255, 0, 0)
                self.cell(self.get_string_width(str(info[1])), text= str(info[1]), new_y= "NEXT")
                self.set_text_color(0, 0, 0)
                self.ln()

            elif len(info) == 3:
                self.cell(self.get_string_width(info[1]), text= info[1])
                self.set_text_color(245, 245, 0)
                self.cell(self.get_string_width(info[2]), text= info[2], new_y= "NEXT")
                self.set_text_color(0, 0, 0)
                self.ln()

            else:
                self.cell(self.get_string_width(str(info[1])), text= str(info[1]), new_y= "NEXT")
                self.ln()

        img= creat_graph(data)
        self.image(img, 15, self.get_y() + 25, self.w - 30)

    def print_month_summary(self, data, links):
        date, budget, t_expenses, R_B, nb_transactions, month = data
        self.add_page()
        self.set_link(links[month])
        self.set_left_margin(15)
        self.set_font("Helvetica", "B", 35)
        self.cell(0, text= f"{date}:")
        self.ln(22)
        infos= [
            ["Monthly Budget:  ", f"{budget} $"],
            ["Total Expenses:  ", f"{t_expenses} $"],
            ["Remaining Balance:  ", f"{R_B} $"],
            ["Number of Transactions:  ", nb_transactions]
            ]

        if budget is None:
            infos[0][1]= "You didn't submit your budget!"
            infos[2][1]= "Not available!"

        if R_B != 0:
            infos[2].append(True)

        for info in infos:
            self.set_font("Helvetica", "B", 16)
            self.cell(self.get_string_width(info[0]), text= info[0])
            self.set_font("Helvetica", "I", 13)

            if info[1][0] == "-" or info[1][-1] == "!":
                self.set_text_color(255, 0, 0)
                self.cell(self.get_string_width(str(info[1])), text= str(info[1]), new_y= "NEXT")
                self.set_text_color(0, 0, 0)
                self.ln()

            elif len(info) == 3:
                self.set_text_color(50, 255, 0)
                self.cell(self.get_string_width(str(info[1])), text= str(info[1]), new_y= "NEXT")
                self.set_text_color(0, 0, 0)
                self.ln()

            else:
                self.cell(self.get_string_width(str(info[1])), text= str(info[1]), new_y= "NEXT")
                self.ln()

        self.ln()
        self.set_font("Helvetica", "B", 16)
        self.cell(0, text= "Categories:")
        self.ln(15)

    def print_categories(self, categories):
        for c in categories:
            self.set_left_margin(25)
            self.set_font("Helvetica", "B", size=18)
            self.cell(5, 8, "-")
            self.set_font("Helvetica", size=14)
            page_width= self.w - self.l_margin - self.r_margin
            category_width= self.get_string_width(f"{c["category"]}:")
            cost_width= self.get_string_width(f"({c["cost"]}$)")
            space_width= self.get_string_width(" ")
            available= page_width- category_width - cost_width - 110
            space= " " * int(available/space_width)

            if c["last_month"] == 0:
                if c["cost"] == 0:
                    comp= f"Increased 0% compared to last month"
                else:
                    comp= "Infinite increase"
            else:
                perc= round(((c["cost"] - c["last_month"]) / c["last_month"]) * 100, 2)
                comp= f"Expenses {"decreased" if perc<0 else "increased"} by {abs(perc)}% compared to last month"

            txt= f"{c["category"]}:{space}({c["cost"]}$)"
            self.cell(self.get_string_width(txt) + 5, text= txt)
            self.set_font(size=11)
            self.cell(0, text= comp)
            self.ln(8)
            self.set_left_margin(40)
            for desc in c["description"]:
                self.set_font("Helvetica", "B", size=13)
                self.cell(5, 8, "-")
                self.set_font("Helvetica", size=11)
                self.multi_cell(0, text= f"'{desc[0]}'  cost  {desc[1]}$.", new_y= "NEXT")
                self.ln(4)
            self.ln(9)

    def print_bar(self, img):
        height= 150
        remaining_height= self.h - self.get_y() - 15

        if height > remaining_height:
            self.add_page()
            self.image(img, 15, self.get_y(), self.w - 30, 150)
        else:
            self.image(img, 15, self.get_y(), self.w - 30, 150)


def creat_bar(categories):
    all_categories= []
    all_costs= []

    for info in categories:
        all_categories.append(info["category"])
        all_costs.append(info["cost"])

    n= len(all_categories)
    width= 0.6 if n > 1 else 0.2

    sorted_data= sorted(zip(all_costs, all_categories), reverse= True)
    values, category= zip(*sorted_data)

    plt.figure(dpi=300)
    plt.bar(category, values, width, color= "#1f4e79")
    plt.xticks(rotation=45)
    if n ==1:
        plt.xlim(-0.5, 0.5)
    plt.tight_layout()

    plt.ylabel("Expenses")
    plt.title("Expenses By Category")

    img_buffer= BytesIO()
    plt.savefig(img_buffer, format= "PNG", bbox_inches= "tight")
    plt.close()
    img_buffer.seek(0)

    return img_buffer


def creat_graph(data):
    expenses_info, budgets_info, _, _, _ = data
    expenses= [amount for _, amount in sorted(expenses_info.items())]
    budgets= [amount for _, amount in sorted(budgets_info.items())]
    months= sorted(list(set(expenses_info) | set(budgets_info)))
    months= list(map(int, months))
    amounts= expenses + budgets
    amounts= list(filter(None ,amounts))

    plt.figure(dpi=300)
    plt.plot(months, budgets, color= "b", label= "Budgets")
    plt.plot(months, expenses, color= "r", label= "Expenses")
    plt.hlines(y= amounts, xmin= min(months), xmax= max(months), linestyles= "dashed", linewidth= 0.5)
    plt.vlines(x= months, ymin= min(amounts), ymax= max(amounts), linestyles= "dashed", linewidth= 0.5)
    plt.xticks(months)
    plt.xlabel("Months")
    plt.ylabel("Amount")
    plt.title("Budget VS Expenses", fontsize= 16)
    plt.legend()

    img_buffer= BytesIO()
    plt.savefig(img_buffer, format= "PNG", bbox_inches= "tight")
    plt.close()
    img_buffer.seek(0)

    return img_buffer


def organize_values(data):
    expenses, budgets, r_b, nb_transactions, date = data

    missing_budgets= {month: True if amount is None else False for month, amount in budgets.items()}
    if all([check for _, check in missing_budgets.items()]):
        budget= "You didn't submit your budgets!"
    else:
        months= [datetime(1, int(month), 1).strftime("%b") for month, check in missing_budgets.items() if check is False]
        if len(months) == 12:
            budget= f"{sum([amount for _, amount in budgets.items() if amount is not None]):,} $"
        else:
            months= ", ".join(months)
            budget= f"{sum([amount for _, amount in budgets.items() if amount is not None]):,} $    ^for ({months})"

    missing_expenses= {month: True if amount is None else False for month, amount in expenses.items()}
    if all([check for _, check in missing_expenses.items()]):
        expense= "You didn't submit your expenses!"
    else:
        months= [datetime(1, int(month), 1).strftime("%b") for month, check in missing_expenses.items() if check is False]
        if len(months) == 12:
            expense= f"{sum([amount for _, amount in expenses.items() if amount is not None]):,} $"
        else:
            months= ", ".join(months)
            expense= f"{sum([amount for _, amount in expenses.items() if amount is not None]):,} $ ^for ({months})"

    if any([check for _, check in missing_budgets.items()]) or any([check for _, check in missing_expenses.items()]):
        r_b= "Not available!"
    else:
        r_b= f"{sum([amount for _, amount in r_b.items()]):,} $"

    return expense, budget, r_b, nb_transactions, date


def show_data():
    organized, budget, expenses= organize_data()
    if budget is False or not expenses:
        print("No Data Available.")
        return None

    print("Please wait...", end="", flush= True)
    pdf= PDF()
    pdf.prepare_pdf()

    orders= []
    summary_titles= []

    for year in organized:
        orders.append(((pdf.print_year, True), year["year"]))
        summary_titles.append(("year", (None, year["year"])))

        y_budgets= {m_budget["month"][:2]: m_budget["budget"] for m_budget in budget if m_budget["month"][-4:] == year["year"]}
        m_expenses={}
        nb_transactions_y= 0
        for expense in expenses:
            if expense["Dates"][:4] == year["year"]:
                nb_transactions_y += 1
                month= expense["Dates"][5:7]
                if m_expenses.get(month, False) is False:
                    m_expenses[month]= [float(expense["Cost"])]
                else:
                    m_expenses[month] += [float(expense["Cost"])]
        y_expenses= {k: sum(v) for k, v in m_expenses.items()}
        for k, _ in y_expenses.items():
            if y_budgets.get(k, False) is False:
                y_budgets[k]= None
        for k, _ in y_budgets.items():
            if y_expenses.get(k, False) is False:
                y_expenses[k]= None
        remaining_y_balance= {}
        for k, _ in y_expenses.items():
            try:
                remaining_y_balance.update({k: y_budgets[k] - y_expenses[k]})
            except:
                remaining_y_balance.update({k: None})

        orders.append(((pdf.print_year_summary, False), [y_expenses, y_budgets, remaining_y_balance, str(nb_transactions_y), year["year"]]))

        for month in year["months"]:
            date= datetime(int(year["year"]), int(month["month"]), 1).strftime("%B")
            month_budget_list= [b["budget"] for b in budget if b["month"] == f"{month["month"]} {year["year"]}"]
            try:
                month_budget= month_budget_list[0]
            except:
                month_budget= None
            all_expenses= [float(exp["Cost"]) for exp in expenses if exp["Dates"][:7] == f"{year["year"]}-{month["month"]}"]
            total_expenses= sum(all_expenses)
            try:
                remaining_balance= month_budget - total_expenses
            except:
                remaining_balance= None
            nb_transactions= len(all_expenses)

            orders.append(((pdf.print_month_summary, True), [date, month_budget, total_expenses, remaining_balance, str(nb_transactions), (year["year"], month["month"])]))
            summary_titles.append(("month", (year["year"], month["month"])))

            categories_info= []
            for category in month["Categories"]:
                if not any(c["category"] == category["category"] for c in categories_info):
                    categories_info.append({"category": category["category"]})

                category_expenses= []
                description_orders= []

                for description in category["description"]:
                    category_expenses.append(float(description["cost"]))
                    description_orders.append((description["desc"], float(description["cost"])))

                for c in categories_info:
                    if c["category"] == category["category"]:
                        if c.get("cost", False) is False:
                            c.update({"cost": sum(category_expenses), "description": description_orders})
                        else:
                            c.update({"cost": sum(category_expenses) + c["cost"], "description": description_orders})

                last_month_amount=0
                for Expense in expenses:
                    if Expense["Categories"][2:-2] == category["category"]:
                        this_month= int(month["month"])
                        last_month= this_month - 1
                        this_year= int(year["year"])
                        if last_month == 0:
                            last_month= 12
                            this_year-= 1

                        if Expense["Dates"][:7] == f"{this_year}-{last_month:02d}":
                            last_month_amount+= float(Expense["Cost"])
                for c in categories_info:
                    if c["category"] == category["category"]:
                        c.update({"last_month": last_month_amount})

            orders.append(((pdf.print_categories, False), sorted(categories_info, key= lambda cat: cat["cost"], reverse= True)))
            orders.append(((pdf.print_bar, False), creat_bar(categories_info)))

    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()
    print("Generating PDF...", end="", flush= True)

    links= {}
    for ym in summary_titles:
        links[ym[1]]= pdf.add_link()
    pdf.print_toc(summary_titles, links)
    for order, data in orders:
        if order[1] is True:
            order[0](data, links)
            continue
        order[0](data)

    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()
    pdf.output("summary.pdf")
    print("PDF successfully generated.")


def set_budget():
    while True:
        try:
            budget= round(float(input("Enter your monthly budget: ")))
            if budget <= 0:
                print("Please enter a valid budget.\n")
                continue
            break
        except (ValueError, KeyboardInterrupt):
            print("Please enter a valid budget.\n")

    old_users_info= get_data_j()

    for _, list in old_users_info.items():
        for dict in list:
            if username == dict["username"]:
                if dict.get("budget", False) is False:
                    dict.update({"budget": [{"month": date.today().strftime("%m %Y"), "budget": budget}]})
                    print(f"{budget}$ is your budget for this month: {date.today().strftime("%B %Y")}.")

                else:
                    months= [dictionary["month"] for dictionary in dict["budget"]]

                    if date.today().strftime("%m %Y") in months:
                        print("A Budget has already been set for this month!")
                        break
                    else:
                        dict["budget"].append({"month": date.today().strftime("%m %Y"), "budget": budget})
                        print(f"{budget}$ is your budget for this month: {date.today().strftime("%B %Y")}.")
                        break

    store_data_j(old_users_info)


def check_budget():
    old_users_info= get_data_j()

    for _, list in old_users_info.items():
        for dict in list:
            if username == dict["username"]:
                if dict.get("budget", True) is True:
                    print("⚠️ It's a new month. You need to enter a new Budget.")
                    break
                else:
                    months= [dictionary["month"] for dictionary in dict["budget"]]

                    if date.today().strftime("%m %Y") in months:
                        expenses= 0
                        reader= get_expenses()
                        for row in reader:
                            if row["Users"] == username:
                                if str(row["Dates"][:7]) == f"{date.today().strftime("%Y")}-{date.today().strftime("%m")}":
                                    expenses+= float(row["Cost"])

                        for dict_budget in dict["budget"]:
                            if dict_budget["month"] == date.today().strftime("%m %Y"):
                                percentage_today= (expenses/dict_budget["budget"])*100

                        days= int(calendar.monthrange(date.today().year, date.today().month)[1])
                        difference_in_percentage= percentage_today-(100/days)*int(date.today().strftime("%d"))
                        daily_per= 100/days


                        if -100 <= difference_in_percentage < -7*daily_per:
                            print("You barely spent any money!")

                        elif -7*daily_per <= difference_in_percentage < -2*daily_per:
                            print("You spent very little.")

                        elif -2*daily_per <= difference_in_percentage <= daily_per:
                            print("Your spendings are normal.")

                        elif daily_per < difference_in_percentage <= 6*daily_per:
                            print("You spent a lot of money.")

                        elif 6*daily_per < difference_in_percentage:
                            print("Your expenses are too high!")
                        break
                    else:
                        print("⚠️ It's a new month. You need to enter a new Budget.")
                        break

def main2():
    actions= {
        "1": ("Enter new expense", new_expense),
        "2": ("Show financial summaries (generate PDF)", show_data),
        "3": ("Set your monthly budget", set_budget)
    }

    check_budget()

    while True:
        print("\n=== Welcome To Our ExpensesTracker System ===")
        for number, (function, _) in actions.items():
            print(f"{number}. {function}")
        print("4. Exit")

        try:
            choice= input("\nEnter your choice: ").strip()
        except KeyboardInterrupt:
            continue

        if choice in actions:
            actions[choice][1]()

        elif choice == "4":
            sys.exit("\nExiting program...")

        else:
            print("\nInvalid choice! Try again.\n")
            
if __name__ == "__main__":
    main2()
