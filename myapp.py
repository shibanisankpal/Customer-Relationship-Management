import streamlit as st
import sqlite3

# Connect to the database
conn = sqlite3.connect('crm.db')
c = conn.cursor()

# Create customers table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS customers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             email TEXT,
             phone TEXT)''')
conn.commit()

# Add a new customer to the database
def add_customer(name, email, phone):
    c.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()

# Remove a customer from the database
def remove_customer(customer_id):
    c.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()

# Get all customers from the database
def get_customers():
    c.execute("SELECT * FROM customers")
    return c.fetchall()

# Streamlit UI
def main():
    st.title("CRM System")

    # Add Customer
    st.header("Add Customer")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    if st.button("Add"):
        add_customer(name, email, phone)
        st.success("Customer added successfully.")
        
    # Remove Customer
    st.header("Remove Customer")
    remove_id = int(st.number_input("Enter the ID of the customer to remove"))
    if st.button("Remove"):
        remove_customer(remove_id)
        st.success("Customer removed successfully.")

    # Display Customers
    st.header("Customer List")
    customers = get_customers()
    for customer in customers:
        st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")

if __name__ == '__main__':
    main()
