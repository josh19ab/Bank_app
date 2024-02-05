import sqlite3

# customer
class Customer:
    def __init__(self, cust_name, password, balance=0):
        self.cust_name = cust_name
        self.password = password
        self.balance = balance


class BankApplication:
    def __init__(self):
        self.conn = sqlite3.connect('bank_database.db')  #connect with database
        self.create_table()

# creating table in db to store customer details
    def create_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    cust_name TEXT PRIMARY KEY,
                    password TEXT,
                    balance REAL
                )
            ''')
            
    # to add customer
    def insert_customer(self, customer):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO customers VALUES (?, ?, ?)
            ''', (customer.cust_name, customer.password, customer.balance))
            
    # existing customer details
    def get_customer_by_credentials(self, cust_name, password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM customers WHERE cust_name=? AND password=?
            ''', (cust_name, password))
            return cursor.fetchone()
        
    # user choice
    def display_menu(self):
        print("\nMenu:")
        print("1. Customer Login")
        print("2. New Customer Sign in")
        print("3. Exit")

    # login details
    def customer_login(self):
        cust_name = input("Enter Customer Name: ")
        password = input("Enter Password: ")

        customer_data = self.get_customer_by_credentials(cust_name, password)

        if customer_data:
            customer = Customer(*customer_data)
            print(f"Welcome {cust_name}!")
            self.account_menu(customer)
        else:
            print("Not a valid customer...")

# adding new customer
    def new_customer_sign_in(self):
        cust_name = input("Enter Customer Name: ")
        password = input("Enter Password: ")

        if not self.get_customer_by_credentials(cust_name, password):
            new_customer = Customer(cust_name, password)
            self.insert_customer(new_customer)
            print("Customer signed in successfully.")
        else:
            print("Customer already exists. Try a different username.")

# options after login
    def account_menu(self, customer):
        while True:
            print("\nAccount Details:")
            print("a. Amount Deposit")
            print("b. Amount Withdrawal")
            print("c. Check Balance")
            print("d. Exit")

            option = input("Choose an option: ").lower()
            # deposit
            if option == 'a': 
                amount = self.get_valid_amount("Enter amount to deposit: ")
                customer.balance += amount
                print(f"Current balance: {customer.balance}")
            # withdrawal
            elif option == 'b':
                amount = self.get_valid_amount("Enter amount to withdraw: ")
                if amount > customer.balance:
                    print("!!!Insufficient balance.!!!")
                else:
                    customer.balance -= amount
                    print(f"Withdrawal successful. Current balance: {customer.balance}")
            # balance
            elif option == 'c':
                print(f"Current balance: {customer.balance}")

            elif option == 'd':
                break
# exceptions and handling invalid inputs
    def get_valid_amount(self, prompt):
        while True:
            try:
                amount = float(input(prompt))
                if amount > 0:
                    return amount
                else:
                    print("Amount must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def __del__(self):
        self.conn.close()

# main program
if __name__ == "__main__":
    bank_app = BankApplication()

    while True:
        bank_app.display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            bank_app.customer_login()
        elif choice == '2':
            bank_app.new_customer_sign_in()
        elif choice == '3':
            print("Exited Application successfully...")
            break
