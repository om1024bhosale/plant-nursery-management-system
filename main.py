import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


def connect_db():
    conn = sqlite3.connect('plants.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS plants (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, 
    quantity INTEGER, date_added TEXT)''')
    conn.commit()
    return conn


def add_plant(name, price, quantity, date_added):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO plants (name, price, quantity, date_added) VALUES (?, ?, ?, ?)",
                   (name, price, quantity, date_added))
    conn.commit()
    conn.close()


def view_plants():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    conn.close()
    return plants


def update_plant(id, name, price, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE plants SET name=?, price=?, quantity=? WHERE id=?", (name, price, quantity, id))
    conn.commit()
    conn.close()


def delete_plant(pid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plants WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def search_plant_name(pid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM plants WHERE id=?", (pid,))
    plant_name = cursor.fetchone()
    conn.close()
    return plant_name[0] if plant_name else None


def add_plant_click():
    name = name_entry.get()
    price_str = price_entry.get()
    quantity_str = quantity_entry.get()
    date_str = date_entry.get()
    time_str = time_entry.get()

    if not (name and price_str and quantity_str and date_str and time_str):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        price = float(price_str)
        quantity = int(quantity_str)
        datetime_str = f"{date_str} {time_str}"
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')  # corrected the format
    except ValueError:
        messagebox.showerror("Error", "Invalid price, quantity, or datetime format.")
        return

    date_added = datetime_str
    add_plant(name, price, quantity, date_added)
    messagebox.showinfo("Success", "Plant added successfully.")
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)


def view_plants_click():
    plants = view_plants()
    if not plants:
        messagebox.showinfo("No Plants", "No plants in the nursery.")
    else:
        plant_list = "\n".join(
            [f"{plant[0]} - {plant[1]} - ${plant[2]} - Quantity: {plant[3]} - Added on: {plant[4]}" for plant in
             plants])
        messagebox.showinfo("Plants in Nursery", plant_list)


def delete_plant_click():
    try:
        pid = int(id_entry.get())
        delete_plant(pid)
        messagebox.showinfo("Success", "Plant deleted successfully.")
        id_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a valid numeric ID.")


def update_plant_click():
    try:
        id = int(id_entry.get())
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        update_plant(id, name, price, quantity)
        messagebox.showinfo("Success", "Plant updated successfully.")
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid ID, price, or quantity. Please enter valid values.")


def search_plant_click():
    try:
        pid = int(id_entry.get())
        plant_name = search_plant_name(pid)
        if plant_name:
            search_result_label.config(text=f"Plant Name: {plant_name}")
        else:
            messagebox.showinfo("Not Found", "Plant with the provided ID not found.")
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a valid numeric ID.")



root = tk.Tk()
root.title("Plant Nursery Management System")

name_label = tk.Label(root, text="Plant Name:")  # corrected label text
name_label.grid(row=0, column=0)

name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

price_label = tk.Label(root, text="Plant Price:")  # corrected label text
price_label.grid(row=1, column=0)

price_entry = tk.Entry(root)
price_entry.grid(row=1, column=1)

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.grid(row=2, column=0)

quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1)

id_label = tk.Label(root, text="Plant ID:")  # corrected label text
id_label.grid(row=3, column=0)

id_entry = tk.Entry(root)
id_entry.grid(row=3, column=1)

date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=4, column=0)

date_entry = tk.Entry(root)
date_entry.grid(row=4, column=1)

time_label = tk.Label(root, text="Time (HH:MM:SS):")
time_label.grid(row=5, column=0)

time_entry = tk.Entry(root)
time_entry.grid(row=5, column=1)

add_button = tk.Button(root, text="Add Plant", command=add_plant_click)
add_button.grid(row=6, column=0, columnspan=2)

view_button = tk.Button(root, text="View Plants", command=view_plants_click)
view_button.grid(row=7, column=0, columnspan=2)

delete_button = tk.Button(root, text="Delete Plant", command=delete_plant_click)
delete_button.grid(row=8, column=0, columnspan=2)

update_button = tk.Button(root, text="Update Plant", command=update_plant_click)
update_button.grid(row=9, column=0, columnspan=2)

search_button = tk.Button(root, text="Search Plant", command=search_plant_click)
search_button.grid(row=10, column=0, columnspan=2)

search_result_label = tk.Label(root, text="")
search_result_label.grid(row=11, column=0, columnspan=2)


root.mainloop()
