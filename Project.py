#CRM SYSTEM
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import random

# Define file paths
file_paths = {
    "Customer Table": "customer_table.csv",
    "Product Table": "product_table.csv",
    "Purchase History Table": "purchase_history_table.csv",
    "Sales Data Table": "sales_data_table.csv",
    "Inventory Table": "inventory_table.csv",
    "Users Table": "users.csv"  
}

# Sample data generation
def generate_sample_data():
    # Users data
    users_data = [
        ["user_id", "username", "password", "role"],
        [1, "admin", "admin123", "admin"],
        [2, "manager", "manager123", "manager"],
        [3, "employee", "employee123", "employee"]
    ]
    
    # Customer data
    customers_data = [
        ["customer_id", "name", "email", "phone", "gender"],
        [1, "John Doe", "john@example.com", "123-456-7890", "male"],
        [2, "Jane Smith", "jane@example.com", "234-567-8901","female"],
        [3, "Bob Johnson", "bob@example.com", "345-678-9012", "male"],
        [4, "Alice Brown", "alice@example.com", "456-789-0123", "female"],
        [5, "Charlie Davis", "charlie@example.com", "567-890-1234", "female"]
    ]
    
    # Product data
    products_data = [
        ["product_id", "name", "category", "price", "popularity"],
        [1, "Laptop Pro", "Electronics", 999.99, 85],
        [2, "Smartphone X", "Electronics", 699.99, 90],
        [3, "Wireless Earbuds", "Accessories", 129.99, 75],
        [4, "Smart Watch", "Electronics", 249.99, 70],
        [5, "Power Bank", "Accessories", 49.99, 60]
    ]
    
    # Generate purchase history
    purchase_history_data = [
        ["purchase_id", "customer_id", "product_id", "purchase_date", "quantity", "price"]
    ]
    
    for i in range(1, 21):  # 20 purchase records
        purchase_history_data.append([
            i,  # purchase_id
            random.randint(1, 5),  # customer_id
            random.randint(1, 5),  # product_id
            (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
            random.randint(1, 3),  # quantity
            random.uniform(49.99, 999.99)  # price
        ])
    
    # Generate sales data
    sales_data = [
        ["product_id", "quantity_sold", "price"]
    ]
    for product_id in range(1, 6):
        sales_data.append([
            product_id,
            random.randint(50, 200),  # quantity_sold
            products_data[product_id][3]  # price from products_data
        ])
    
    # Generate inventory data
    inventory_data = [
        ["product_id", "stock_level", "reorder_threshold"]
    ]
    for product_id in range(1, 6):
        inventory_data.append([
            product_id,
            random.randint(10, 100),  # stock_level
            random.randint(5, 20)  # reorder_threshold
        ])
    
    return {
        "Users Table": users_data,
        "Customer Table": customers_data,
        "Product Table": products_data,
        "Purchase History Table": purchase_history_data,
        "Sales Data Table": sales_data,
        "Inventory Table": inventory_data
    }

# Initialize database with sample data
def initialize_database():
    # Generate sample data
    data = generate_sample_data()
    
    # Create CSV files
    for table_name, file_path in file_paths.items():
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data[table_name])
            
# HashTable Implementation
class HashTable:
    def __init__(self, size: int):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    def set_val(self, key, val):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]

        for index, record in enumerate(bucket):
            record_key, _ = record
            if record_key == key:
                bucket[index] = (key, val)
                return

        bucket.append((key, val))

    def get_val(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]

        for record_key, record_val in bucket:
            if record_key == key:
                return record_val

        return "No record found"

# Linked List for User Management
class UserNode:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.next = None

class UserLinkedList:
    def __init__(self):
        self.head = None

    def add_user(self, username, password, role):
        new_node = UserNode(username, password, role)
        new_node.next = self.head
        self.head = new_node

    def find_user(self, username):
        current = self.head
        while current:
            if current.username == username:
                return current
            current = current.next
        return None

    def remove_user(self, username):
        current = self.head
        prev = None

        while current:
            if current.username == username:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next

        return False

    def display_users(self):
        users = []
        current = self.head
        while current:
            users.append((current.username, current.role))
            current = current.next
        return users

# CSV Integration
USER_CSV_FILE = "users.csv"

def load_users_from_csv(file_path):
    user_list = UserLinkedList()
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_list.add_user(row["username"], row["password"], row["role"])
    except FileNotFoundError:
        print("User CSV file not found. Starting with an empty user list.")
    return user_list

def save_users_to_csv(file_path, user_list):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password", "role"])
        writer.writeheader()
        current = user_list.head
        while current:
            writer.writerow({"username": current.username, "password": current.password, "role": current.role})
            current = current.next

# LinkedList implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def display(self):
        return list(self)

# Stack implementation
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def peek(self):
        return self.stack[-1] if self.stack else None

    def peek_n(self, n: int):
        return self.stack[-n:] if n <= len(self.stack) else self.stack[:]

    def display(self):
        return list(reversed(self.stack))

# Customer class
class Customer:
    def __init__(self, customer_id: int, name: str, email: str, phone: str, gender: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.gender = gender
        self.purchase_history = LinkedList()

    def add_purchase(self, purchase):
        self.purchase_history.append(purchase)
        
    def display_purchase_history(self):
        return self.purchase_history.display()

# CRM System
class CRMSystem:
    def __init__(self):
        self.customers = HashTable(100)

    def add_customer(self, customer_id, name, email, phone, gender):
        if self.customers.get_val(customer_id) == "No record found":
            self.customers.set_val(customer_id, {"name": name, "email": email, "phone": phone, "gender": gender})
            print(f"Customer {name} added successfully.")
        else:
            print(f"Customer with ID {customer_id} already exists.")

    def generate_report(self):
        report = []
        for bucket in self.customers.hash_table:
            for customer_id, customer in bucket:
                report.append({
                    "customer_id": customer_id,
                    **customer
                })
        return report

    def save_to_csv(self, file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["customer_id", "name", "email", "phone", "gender"])
            for bucket in self.customers.hash_table:
                for customer_id, customer in bucket:
                    writer.writerow([customer_id, customer["name"], customer["email"], customer["phone"], customer["gender"]])

    def load_from_csv(self, file_path):
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_customer(row["customer_id"], row["name"], row["email"], row["phone"], row["gender"])

# Dynamic Pricing Model
class DynamicPricingModel:
    def __init__(self, pricing_rules, sales_data, inventory_data):
        self.pricing_rules = pricing_rules
        self.sales_data = sales_data
        self.inventory_data = inventory_data

    def calculate_price(self, product_id):
        try:
            base_price = self.sales_data.loc[self.sales_data['product_id'] == product_id, 'price'].values[0]
            stock_level = self.inventory_data.loc[self.inventory_data['product_id'] == product_id, 'stock_level'].values[0]

            for rule, adjustment in self.pricing_rules.items():
                if rule == "low_stock" and stock_level < adjustment['threshold']:
                    return base_price * adjustment['multiplier']
                elif rule == "high_stock" and stock_level > adjustment['threshold']:
                    return base_price * adjustment['multiplier']

            return base_price
        except IndexError:
            print(f"Product ID {product_id} not found in data.")
            return None

    def adjust_prices(self):
        adjusted_prices = {}
        for product_id in self.sales_data['product_id']:
            price = self.calculate_price(product_id)
            if price is not None:
                adjusted_prices[product_id] = price
        return adjusted_prices

# Restocking Model
class RestockingModel:
    def __init__(self, sales_trends, inventory_levels):
        self.sales_trends = sales_trends
        self.inventory_levels = inventory_levels

    def predict_restocking_needs(self):
        restocking_needs = {}
        for product_id in self.inventory_levels['product_id']:
            stock_level = self.inventory_levels.loc[self.inventory_levels['product_id'] == product_id, 'stock_level'].values[0]
            sales_rate = self.sales_trends.loc[self.sales_trends['product_id'] == product_id, 'sales_rate'].values[0]

            days_until_out_of_stock = stock_level / sales_rate if sales_rate > 0 else float('inf')

            if days_until_out_of_stock < 7:
                restocking_needs[product_id] = {
                    'current_stock': stock_level,
                    'days_until_out_of_stock': days_until_out_of_stock
                }

        return restocking_needs

# Recommendation Engine and Products class
class Product:
    def __init__(self, product_id, name, category, popularity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.popularity = popularity
        self.related_products = []

    def add_related_product(self, product):
        self.related_products.append(product)

class RecommendationEngine:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product['product_id']] = product

    def recommend_products(self):
        sorted_products = sorted(self.products.values(), key=lambda x: x['popularity'], reverse=True)
        return sorted_products[:5]

 # Recommenadtion Model
class RecommendationModel:
    def __init__(self):
        self.product_data = None
        self.similarity_matrix = None

    def load_data(self):
        self.product_data = pd.read_csv("product_table.csv")
        self.sales_data = pd.read_csv("purchase_history_table.csv")
        
        # Create feature matrix for products
        features = pd.get_dummies(self.product_data['category'])
        features['price'] = self.product_data['price'] / self.product_data['price'].max()
        features['popularity'] = self.product_data['popularity'] / 100
        
        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(features)

    def recommend_products(self, customer_id, n_recommendations=5):
        # Get customer's purchase history
        customer_purchases = self.sales_data[self.sales_data['customer_id'] == customer_id]['product_id'].unique()
        
        if len(customer_purchases) == 0:
            # If no purchase history, return most popular products
            return self.product_data.nlargest(n_recommendations, 'popularity')['name'].tolist()
        
        # Get similar products based on customer's last purchase
        last_purchase_id = customer_purchases[-1]
        product_idx = self.product_data[self.product_data['product_id'] == last_purchase_id].index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[product_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar products (excluding already purchased)
        recommendations = []
        for idx, _ in sim_scores:
            prod_id = self.product_data.iloc[idx]['product_id']
            if prod_id not in customer_purchases:
                recommendations.append(self.product_data.iloc[idx]['name'])
            if len(recommendations) >= n_recommendations:
                break
                
        return recommendations

# Login System
class LoginSystem:
    def __init__(self):
        self.user_list = load_users_from_csv(USER_CSV_FILE)

        self.access_levels = {
            "admin": "Full access to all systems.",
            "manager": "Access to management systems and reports.",
            "employee": "Access to standard employee resources."
        }

    def login(self, username, password):
        user = self.user_list.find_user(username)
        if user and user.password == password:
            print(f"Login successful. Welcome, {username}!")
            self.show_access_level(user.role)
            return True
        else:
            print("Invalid username or password. Please try again.")
            return False

    def show_access_level(self, role):
        access = self.access_levels.get(role, "No access defined for this role.")
        print(f"Access Level: {access}")

    def add_user(self, username, password, role):
        if self.user_list.find_user(username):
            print("Username already exists. Choose a different username.")
        elif role not in self.access_levels:
            print("Invalid role. Available roles are: admin, manager, employee.")
        else:
            self.user_list.add_user(username, password, role)
            save_users_to_csv(USER_CSV_FILE, self.user_list)
            print(f"User {username} added successfully with role {role}.")

    def remove_user(self, username):
        if self.user_list.remove_user(username):
            save_users_to_csv(USER_CSV_FILE, self.user_list)
            print(f"User {username} removed successfully.")
        else:
            print("User not found.")

## CELL 2
import customtkinter as ctk
from tkinter import messagebox
from CTkListbox import CTkListbox
import pandas as pd
from datetime import datetime

class CRMGUI:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("CRM System")
        self.root.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize CRM system and login
        self.login_system = LoginSystem()
        self.crm_system = CRMSystem()
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize with login page
        self.show_login_page()
        
    def show_login_page(self):
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Create login frame
        login_frame = ctk.CTkFrame(self.main_container)
        login_frame.pack(expand=True, padx=20, pady=20)
        
        # Login header
        header = ctk.CTkLabel(login_frame, text="CRM System Login", font=("Arial", 24, "bold"))
        header.pack(pady=20, padx=20)
        
        # Username field
        username_label = ctk.CTkLabel(login_frame, text="Username:", font=("Arial", 16))
        username_label.pack(pady=5)
        username_entry = ctk.CTkEntry(login_frame)
        username_entry.pack(pady=5)
        
        # Password field
        password_label = ctk.CTkLabel(login_frame, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(login_frame, show="*")
        password_entry.pack(pady=5)
        
        # Login button
        login_button = ctk.CTkButton(
            login_frame, 
            text="Login",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get())
        )
        login_button.pack(pady=20)
        
    def show_main_interface(self, role):
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Create sidebar
        sidebar = ctk.CTkFrame(self.main_container, width=200)
        sidebar.pack(side="left", fill="y", padx=5, pady=5)
        
        # Create main content area
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Sidebar buttons
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customers),
        ]
        
        if role == "manager":
            buttons.append(("Products", self.show_products))
        
        if role == "admin":
            buttons.append(("Products", self.show_products))
            buttons.append(("User Management", self.show_user_management))
            
        buttons.append(("Reports", self.show_reports))
            
        for text, command in buttons:
            btn = ctk.CTkButton(sidebar, text=text, command=command)
            btn.pack(pady=5, padx=10, fill="x")
            
        # Logout button at bottom of sidebar
        logout_btn = ctk.CTkButton(
            sidebar, 
            text="Logout", 
            command=self.show_login_page,
            fg_color="red"
        )
        logout_btn.pack(pady=20, padx=10, fill="x", side="bottom")
        
        # Show dashboard by default
        self.show_dashboard()
        
    def show_dashboard(self):
        self.clear_content_area()
        
        # Dashboard header
        header = ctk.CTkLabel(
            self.content_area, 
            text="Dashboard", 
            font=("Arial", 24, "bold")
        )
        header.pack(pady=20)
        
        # Load real data from CSVs
        customers_df = pd.read_csv("customer_table.csv")
        products_df = pd.read_csv("product_table.csv")
        sales_df = pd.read_csv("sales_data_table.csv")
    
        # Calculate metrics
        total_customers = len(customers_df)
        total_products = len(products_df)
        monthly_sales = sum(sales_df["quantity_sold"] * sales_df["price"])
        avg_product_rating = products_df["popularity"].mean() / 20  # Convert 0-100 to 0-5 scale
    
        # Create grid for dashboard widgets
        grid = ctk.CTkFrame(self.content_area)
        grid.pack(fill="both", expand=True, padx=20, pady=20)
    
        # Summary cards with real data
        for i in range(2):
            grid.grid_columnconfigure(i, weight=1, pad=10)
            
        self.create_summary_card(grid, "Total Customers", str(total_customers), 0, 0)
        self.create_summary_card(grid, "Total Products", str(total_products), 0, 1)
        self.create_summary_card(grid, "Monthly Sales", f"${monthly_sales:,.2f}", 1, 0)
        self.create_summary_card(grid, "Avg Product Rating", f"{avg_product_rating:.1f}/5", 1, 1)
        
    def create_summary_card(self, parent, title, value, row, col):
        card = ctk.CTkFrame(parent, width=70, height=70)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        title_label = ctk.CTkLabel(card, text=title, font=("Arial", 28, "bold"))
        title_label.pack(pady=5)
        
        value_label = ctk.CTkLabel(card, text=value, font=("Arial", 24))
        value_label.pack(pady=10)
        
    def show_customers(self):
        self.clear_content_area()
        
        # Customers header
        header = ctk.CTkLabel(
            self.content_area, 
            text="Customer Management", 
            font=("Arial", 24, "bold")
        )
        header.pack(pady=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.content_area)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        add_button = ctk.CTkButton(
            buttons_frame, 
            text="Add Customer",
            font=("Arial", 15, "bold"),
            command=self.show_customer_crud_dialog
        )
        add_button.pack(padx=5, pady=5)
        
        # Create listbox
        self.customers_listbox = CTkListbox(self.content_area)
        self.customers_listbox.font = ("Arial", 14)
        self.customers_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Load customer data
        customers_df = pd.read_csv("customer_table.csv")
        for _, row in customers_df.iterrows():
            display_text = f'{row["customer_id"]} | {row["name"]} | {row["email"]} | {row["phone"]} | {row["gender"]}'
            insertion = self.customers_listbox.insert("end", display_text)
            insertion.bind("<Double-1>", lambda e: self.show_customer_crud_dialog(
            customer_id=self.customers_listbox.get(self.customers_listbox.curselection()).split(" | ")[0]
        ))
        
    def show_products(self):
        self.clear_content_area()
        
        header = ctk.CTkLabel(
            self.content_area, 
            text="Product Management", 
            font=("Arial", 24, "bold")
        )
        header.pack(pady=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.content_area)
        buttons_frame.pack(fill="x", padx=20, pady=10)
    
        add_button = ctk.CTkButton(
            buttons_frame, 
            text="Add Product",
            font=("Arial", 15, "bold"),
            command=self.show_product_crud_dialog
        )
        add_button.pack(padx=5, pady=5)
    
        # Create listbox
        self.products_listbox = CTkListbox(self.content_area)
        self.products_listbox.font = ("Arial", 14)
        self.products_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Load product data
        products_df = pd.read_csv("product_table.csv")
        for _, row in products_df.iterrows():
            display_text = f'{row["product_id"]} | {row["name"]} | {row["category"]} | ${row["price"]} | Popularity: {row["popularity"]}%'
            insertion = self.products_listbox.insert("end", display_text)
            insertion.bind("<Double-1>", lambda e: self.show_product_crud_dialog(
            product_id=self.products_listbox.get(self.products_listbox.curselection()).split(" | ")[0]
        ))
        
    def show_customer_crud_dialog(self, customer_id=None):
        # Create dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Customer" if customer_id is None else "Edit Customer")
        dialog.geometry("850x250")
    
        # Title
        ctk.CTkLabel(dialog, text="Customer Information", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Configure grid layout
        for i in range(2):
            dialog.grid_columnconfigure(i, weight=1, pad=10)
        
        # Form fields
        fields = ["Name", "Email", "Phone", "Gender"]
        entries = {}
        
        for idx, (field) in enumerate(fields):
            row = idx // 2 + 1
            col = (idx % 2) * 2  # 0 or 2 for two columns

            lbl = ctk.CTkLabel(dialog, text=f'{field}:', font=("Arial", 20))
            lbl.grid(row=row, column=col, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(dialog, width=250)
            entry.grid(row=row, column=col+1, padx=10, pady=10, sticky="w")
            entries[field.lower()] = entry
        
        # If editing, load existing data
        if customer_id is not None:
            customer_id = int(customer_id)
            customers_df = pd.read_csv("customer_table.csv")
            customer_data = customers_df[customers_df["customer_id"] == customer_id].iloc[0]
            entries["name"].insert(0, customer_data["name"])
            entries["email"].insert(0, customer_data["email"])
            entries["phone"].insert(0, customer_data["phone"])
            entries["gender"].insert(0, customer_data["gender"])
        
        # Buttons
        save_btn = ctk.CTkButton(
            dialog,
            text="Save Customer",
            font=("Arial", 20, "bold"),
            command=lambda: self.save_customer(entries, dialog, customer_id)
        )
        save_btn.grid(row=(len(fields) // 2) + 1, column=1, pady=20)
        
        delete_btn = None
        if customer_id is not None:
            delete_btn = ctk.CTkButton(
                dialog,
                text="Delete",
                fg_color="red",
                font=("Arial", 20, "bold"),
                command=lambda: self.delete_customer(customer_id, dialog)
            )
            delete_btn.grid(row=(len(fields) // 2) + 1, column=2, pady=20)
        
        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            font=("Arial", 20, "bold"),
            command=dialog.destroy
        )
        cancel_btn.grid(row=(len(fields) // 2) + 1, column=3, pady=20)

    def show_product_crud_dialog(self, product_id=None):
        # Create dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Product" if product_id is None else "Edit Product")
        dialog.geometry("800x250")
        
        # Title
        ctk.CTkLabel(dialog, text="Product Information", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Configure grid layout
        for i in range(2):
            dialog.grid_columnconfigure(i, weight=1, pad=10)
        
        # Form fields
        fields = ["Name", "Category", "Price", "Popularity"]
        entries = {}
        
        for idx, (field) in enumerate(fields):
            row = idx // 2 + 1
            col = (idx % 2) * 2  # 0 or 2 for two columns

            lbl = ctk.CTkLabel(dialog, text=f'{field}:', font=("Arial", 20))
            lbl.grid(row=row, column=col, padx=10, pady=10, sticky="e")

            entry = ctk.CTkEntry(dialog, width=250)
            entry.grid(row=row, column=col+1, padx=10, pady=10, sticky="w")
            entries[field.lower()] = entry
        
        # If editing, load existing data
        if product_id is not None:
            product_id = int(product_id)
            products_df = pd.read_csv("product_table.csv")
            product_data = products_df[products_df["product_id"] == product_id].iloc[0]
            entries["name"].insert(0, product_data["name"])
            entries["category"].insert(0, product_data["category"])
            entries["price"].insert(0, str(product_data["price"]))
            entries["popularity"].insert(0, str(product_data["popularity"]))
        
        # Buttons        
        save_btn = ctk.CTkButton(
            dialog,
            text="Save Product",
            font=("Arial", 20, "bold"),
            command=lambda: self.save_product(entries, dialog, product_id)
        )
        save_btn.grid(row=(len(fields) // 2) + 1, column=1, pady=20)
        
        delete_btn = None
        if product_id is not None:
            delete_btn = ctk.CTkButton(
                dialog,
                text="Delete",
                font=("Arial", 20, "bold"),
                fg_color="red",
                command=lambda: self.delete_product(product_id, dialog)
            )
            delete_btn.grid(row=(len(fields) // 2) + 1, column=2, pady=20)
        
        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            font=("Arial", 20, "bold"),
            command=dialog.destroy
        )
        cancel_btn.grid(row=(len(fields) // 2) + 1, column=3, pady=20)
        
    def save_customer(self, entries, dialog, customer_id=None):
        # Read existing data
        customers_df = pd.read_csv("customer_table.csv")
        
        new_customer = {
            "name": entries["name"].get(),
            "email": entries["email"].get(),
            "phone": entries["phone"].get(),
            "gender": entries["gender"].get()
        }
        
        if customer_id is None:
            # Add new customer
            new_customer["customer_id"] = len(customers_df) + 1
            new_row = pd.DataFrame([new_customer])
            customers_df = pd.concat([customers_df, new_row], ignore_index=True)
        else:
            # Update existing customer
            customers_df.loc[customers_df["customer_id"] == customer_id, new_customer.keys()] = new_customer.values()
        
        customers_df.to_csv("customer_table.csv", index=False)
        dialog.destroy()
        self.show_customers()  # Refresh view

    def delete_customer(self, customer_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
            customers_df = pd.read_csv("customer_table.csv")
            customers_df = customers_df[customers_df["customer_id"] != customer_id]
            customers_df.to_csv("customer_table.csv", index=False)
            dialog.destroy()
            self.show_customers()  # Refresh view

    def save_product(self, entries, dialog, product_id=None):
        # Read existing data
        products_df = pd.read_csv("product_table.csv")
        
        new_product = {
            "name": entries["name"].get(),
            "category": entries["category"].get(),
            "price": float(entries["price"].get()),
            "popularity": int(entries["popularity"].get())
        }
        
        if product_id is None:
            # Add new product
            new_product["product_id"] = len(products_df) + 1
            products_df = pd.concat([products_df, new_product], ignore_index=True)
        else:
            # Update existing product
            products_df.loc[products_df["product_id"] == product_id, new_product.keys()] = new_product.values()
        
        products_df.to_csv("product_table.csv", index=False)
        dialog.destroy()
        self.show_products()  # Refresh view

    def delete_product(self, product_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            products_df = pd.read_csv("product_table.csv")
            products_df = products_df[products_df["product_id"] != product_id]
            products_df.to_csv("product_table.csv", index=False)
            dialog.destroy()
            self.show_products()  # Refresh view
        
    def show_reports(self):
        self.clear_content_area()
        header = ctk.CTkLabel(
            self.content_area, 
            text="Sales Reports & Analytics", 
            font=("Arial", 24, "bold")
        )
        header.pack(pady=20)
        
        # Create notebook for different report types
        notebook = ctk.CTkTabview(self.content_area)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add tabs
        notebook.add("Sales Overview")
        notebook.add("Product AI Recommendations")
        
        # Sales Overview Tab with existing functionality
        sales_frame = ctk.CTkFrame(notebook.tab("Sales Overview"))
        sales_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load data
        sales_df = pd.read_csv("sales_data_table.csv")
        products_df = pd.read_csv("product_table.csv")
        
        # Total sales
        total_sales = sum(sales_df["quantity_sold"] * sales_df["price"])
        sales_label = ctk.CTkLabel(
            sales_frame,
            text=f"Total Sales: ${total_sales:,.2f}",
            font=("Arial", 16)
        )
        sales_label.pack(pady=10)
        
        # Keep existing Top 5 Best Selling Products
        best_sellers = sales_df.groupby("product_id")["quantity_sold"].sum().nlargest(5)
        best_sellers_frame = ctk.CTkFrame(sales_frame)
        best_sellers_frame.pack(pady=20)
        
        ctk.CTkLabel(
            best_sellers_frame,
            text="Top 5 Best Selling Products",
            font=("Arial", 14, "bold")
        ).pack()
        
        for pid, qty in best_sellers.items():
            product_name = products_df.loc[products_df["product_id"] == pid, "name"].iloc[0]
            ctk.CTkLabel(
                best_sellers_frame,
                text=f"{product_name}: {qty} units"
            ).pack()
        
        # Product Recommendations Tab
        rec_frame = ctk.CTkFrame(notebook.tab("Product AI Recommendations"))
        rec_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize recommendation model
        recommendation_model = RecommendationModel()
        recommendation_model.load_data()
        customers_df = pd.read_csv("customer_table.csv")
        
        # Header
        ctk.CTkLabel(rec_frame, text="Select Customer to Get AI Recommendations", font=("Arial", 16, "bold")).pack(pady=[0, 10])
        
        customer_var = ctk.StringVar()
        customer_select = ctk.CTkComboBox(
            rec_frame,
            values=[str(name) for name in customers_df["name"]],
            variable=customer_var,
            width=200
        )
        customer_select.pack(pady=5)
        
        def show_recommendations():
            rec_listbox.delete(0, "end")
            customer_id = customers_df.loc[customers_df["name"] == customer_var.get(), "customer_id"].iloc[0]
            recommendations = recommendation_model.recommend_products(customer_id)
            
            for i, product in enumerate(recommendations, 1):
                rec_listbox.insert("end", f"{i}. {product}")
        
        ctk.CTkButton(
            rec_frame,
            text="Get Recommendations",
            font=("Arial", 14),
            command=show_recommendations
        ).pack(pady=10)
        
        # Recommendations listbox
        ctk.CTkLabel(rec_frame, text="Recommended Products:", font=("Arial", 16, "bold")).pack(pady=10)
        
        rec_listbox = CTkListbox(rec_frame)
        rec_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
    def show_user_management(self):
        self.clear_content_area()
        header = ctk.CTkLabel(
            self.content_area, 
            text="User Management", 
            font=("Arial", 24, "bold")
        )
        header.pack(pady=20)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.content_area)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        add_button = ctk.CTkButton(
            buttons_frame, 
            text="Add User",
            font=("Arial", 15, "bold"),
            command=lambda: self.show_user_crud_dialog()
        )
        add_button.pack(padx=5, pady=5)
        
        # Create listbox for users
        self.users_listbox = CTkListbox(self.content_area)
        self.users_listbox.font = ("Arial", 14)
        self.users_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Load user data
        users_df = pd.read_csv("users.csv")
        for _, row in users_df.iterrows():
            display_text = f'{row["user_id"]} | {row["username"]} | {row["role"]} | Last Login: {row.get("last_login", "Never")}'
            insertion = self.users_listbox.insert("end", display_text)
            insertion.bind("<Double-1>", lambda e: self.show_user_crud_dialog(
                user_id=self.users_listbox.get(self.users_listbox.curselection()).split(" |")[0]
            ))

    def show_user_crud_dialog(self, user_id=None):        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add User" if user_id is None else "Edit User")
        dialog.geometry("400x350")
        
        # Form fields
        header_left = ctk.CTkLabel(dialog, text="User Information", font=("Arial", 24, "bold"))
        header_left.pack(pady=10)
        
        entries = {}
        
        # Username field
        ctk.CTkLabel(dialog, text="Username:").pack(pady=5)
        entries["username"] = ctk.CTkEntry(dialog)
        entries["username"].pack(pady=5)
        
        # Password field
        ctk.CTkLabel(dialog, text="Password:").pack(pady=5)
        entries["password"] = ctk.CTkEntry(dialog, show="*")
        entries["password"].pack(pady=5)
        
        # Role selection
        ctk.CTkLabel(dialog, text="Role:").pack(pady=5)
        role_var = ctk.StringVar(value="user")
        entries["role"] = ctk.CTkComboBox(dialog, values=["user", "admin"])
        entries["role"].pack(pady=5)
        
        # Load existing data if editing
        if user_id is not None:
            user_id = int(user_id)
            users_df = pd.read_csv("users.csv")
            user_data = users_df[users_df["user_id"] == user_id].iloc[0]
            entries["username"].insert(0, user_data["username"])
            entries["password"].insert(0, user_data["password"])
            entries["role"].set(user_data["role"])
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog)
        btn_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save User",
            command=lambda: self.save_user(entries, dialog, user_id)
        )
        save_btn.pack(side="left", padx=5)
        
        if user_id is not None:
            delete_btn = ctk.CTkButton(
                btn_frame,
                text="Delete",
                fg_color="red",
                command=lambda: self.delete_user(user_id, dialog)
            )
            delete_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5)

    def save_user(self, entries, dialog, user_id=None):
        users_df = pd.read_csv("users.csv")
        
        new_user = {
            "username": entries["username"].get(),
            "role": entries["role"].get()
        }
        
        if entries["password"].get():  # Only update password if provided
            new_user["password"] = entries["password"].get()
        
        if user_id is None:
            # Add new user
            new_user["user_id"] = len(users_df) + 1
            if "password" not in new_user:
                messagebox.showerror("Error", "Password is required for new users")
                return
            users_df = pd.concat([users_df, new_user], ignore_index=True)
        else:
            # Update existing user
            if "password" not in new_user:
                del new_user["password"]  # Don't update password if not provided
            users_df.loc[users_df["user_id"] == user_id, new_user.keys()] = new_user.values()
        
        users_df.to_csv("users.csv", index=False)
        dialog.destroy()
        self.show_user_management()

    def delete_user(self, user_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            users_df = pd.read_csv("users.csv")
            users_df = users_df[users_df["user_id"] != user_id]
            users_df.to_csv("users.csv", index=False)
            dialog.destroy()
            self.show_user_management()
        
    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def handle_login(self, username, password):
        if self.login_system.login(username, password):
            user = self.login_system.user_list.find_user(username)
            self.show_main_interface(user.role)
        else:
            messagebox.showerror("Error", "Incorrect Username or Password")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CRMGUI()
    app.run()