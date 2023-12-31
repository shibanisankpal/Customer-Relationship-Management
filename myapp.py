import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

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
    customer_id = c.lastrowid
    c.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
    return c.fetchone()

# Update customer details in the database
def update_customer(customer_id, name, email, phone):
    c.execute("UPDATE customers SET name=?, email=?, phone=? WHERE id=?", (name, email, phone, customer_id))
    conn.commit()

# Remove a customer from the database
def remove_customer(customer_id):
    c.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()

# Get all customers from the database
def get_customers():
    c.execute("SELECT * FROM customers")
    return c.fetchall()

# Search customers by name, email, or phone number
def search_customers(query):
    c.execute("SELECT * FROM customers WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?",
              (f"%{query}%", f"%{query}%", f"%{query}%"))
    return c.fetchall()

# Filter customers based on specific criteria
def filter_customers(criteria):
    c.execute(f"SELECT * FROM customers WHERE {criteria}")
    return c.fetchall()

# Sort customers by attribute
def sort_customers(attribute, ascending=True):
    c.execute(f"SELECT * FROM customers ORDER BY {attribute} {'ASC' if ascending else 'DESC'}")
    return c.fetchall()

# Streamlit UI
def main():
    st.title("Customer Relationship Management System")

    # Add Customer
    st.header("Add Customer")
    add_name = st.text_input("Name", key="add_name")
    add_email = st.text_input("Email", key="add_email")
    add_phone = st.text_input("Phone", key="add_phone")
    if st.button("Add"):
        added_customer = add_customer(add_name, add_email, add_phone)
        if added_customer is not None:
            st.success("Customer added successfully.")
            st.write("Added Customer Details:")
            st.write(f"ID: {added_customer[0]}, Name: {added_customer[1]}, Email: {added_customer[2]}, Phone: {added_customer[3]}")
        else:
            st.error("Failed to add customer.")

    # Update Customer
    st.header("Update Customer Details")
    update_id = st.number_input("Enter the ID of the customer to update", step=1, key="update_id")
    update_name = st.text_input("Name", key="update_name")
    update_email = st.text_input("Email", key="update_email")
    update_phone = st.text_input("Phone", key="update_phone")
    if st.button("Update"):
        update_customer(update_id, update_name, update_email, update_phone)
        st.success("Customer details updated successfully.")

    # Remove Customer
    st.header("Remove Customer")
    remove_id = st.number_input("Enter the ID of the customer to remove", step=1, key="remove_id")
    if st.button("Remove"):
        remove_customer(remove_id)
        st.success("Customer removed successfully.")

    # Search Customers
    st.header("Search Customers")
    search_query = st.text_input("Enter a name, email, or phone number to search", key="search_query")
    if st.button("Search"):
        searched_customers = search_customers(search_query)
        if searched_customers:
            st.write("Search Results:")
            for customer in searched_customers:
                st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        else:
            st.write("No matching customers found.")

    # Filter Customers
    st.header("Filter Customers")
    filter_criteria = st.text_input("Enter a filter criteria (e.g., name = 'John')", key="filter_criteria")
    if st.button("Filter"):
        filtered_customers = filter_customers(filter_criteria)
        if filtered_customers:
            st.write("Filtered Customers:")
            for customer in filtered_customers:
                st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        else:
            st.write("No customers matching the filter criteria.")

    # Sort Customers
    st.header("Sort Customers")
    sort_attribute = st.selectbox("Select an attribute to sort by", ["name", "email", "phone"], key="sort_attribute")
    sort_ascending = st.checkbox("Sort in ascending order", value=True, key="sort_ascending")
    if st.button("Sort"):
        sorted_customers = sort_customers(sort_attribute, sort_ascending)
        st.write("Sorted Customers:")
        for customer in sorted_customers:
            st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")

    # Display Customers with Pagination
    st.header("Customer List")
    customers = get_customers()
    page_size = 10
    num_pages = (len(customers) - 1) // page_size + 1
    page_num = st.number_input("Enter page number", min_value=1, max_value=num_pages, value=1, step=1, key="page_num")
    start_index = (page_num - 1) * page_size
    end_index = min(start_index + page_size, len(customers))
    displayed_customers = customers[start_index:end_index]
    if displayed_customers:
        st.write("Customers:")
        for customer in displayed_customers:
            st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
    else:
        st.write("No customers to display.")

    # Export Customer Data
    st.header("Export Customer Data")
    export_format = st.selectbox("Select export format", ["CSV", "Excel"], key="export_format")
    if st.button("Export"):
        df = pd.DataFrame(customers, columns=["ID", "Name", "Email", "Phone"])
        if export_format == "CSV":
            st.download_button("Download CSV", df.to_csv(index=False), file_name="customer_data.csv", mime="text/csv")
        elif export_format == "Excel":
            st.download_button("Download Excel", df.to_excel(index=False), file_name="customer_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # Data Visualization: Customer Analysis
    st.header("Customer Analysis")

    # Bar Chart: Customer Count by Name
    st.subheader("Customer Count by Name")
    customers = get_customers()
    df_customers = pd.DataFrame(customers, columns=["ID", "Name", "Email", "Phone"])
    name = df_customers["Name"].value_counts()
    fig_bar = px.bar(name, x=name.index, y=name.values)
    st.plotly_chart(fig_bar)

    # Bar Chart: Customer Count by Email
    st.subheader("Customer Count by Email")
    customers = get_customers()
    df_customers = pd.DataFrame(customers, columns=["ID", "Name", "Email", "Phone"])
    email = df_customers["Email"].value_counts()
    fig_bar = px.bar(email, x=email.index, y=email.values)
    st.plotly_chart(fig_bar)
    # Bar Chart: Customer Count by Phone
    st.subheader("Customer Count by Phone")
    customers = get_customers()
    df_customers = pd.DataFrame(customers, columns=["ID", "Name", "Email", "Phone"])
    phone = df_customers["Phone"].value_counts()
    fig_bar = px.bar(phone, x=phone.index, y=phone.values)
    st.plotly_chart(fig_bar)


if __name__ == '__main__':
    main()

