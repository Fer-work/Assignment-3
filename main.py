from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from controller import (add_item_controller, delete_item_controller, fetch_all_items_controller, update_item_controller, create_tables_controller, fetch_all_records_controller)

# Initialize the main window
window = Tk()
window.title("Ledger System")
window.geometry("750x640")

# Treeview
my_tree = ttk.Treeview(window, show="headings", height=10)

placeholderArray = [StringVar() for _ in range(5)]

# Global variable to track current view
current_view = 'inventory'  # Possible values: 'inventory', 'ledger'

create_tables_controller()  # Create tables if they don't exist

# Refresh Treeview based on the current view
def refreshTable():
    # Clear existing columns before setting new ones
    my_tree["columns"] = ()  # Reset previous columns
    my_tree.delete(*my_tree.get_children())  # Clear old data

    if current_view == 'inventory':
        column_names = ("Item Id", "Name", "Category", "Price", "Quantity", "Date")
    else:  # Ledger view
        column_names = ("Record Id", "Operation Name", "Debit", "Credit", "Total Balance", "Date")

    my_tree.configure(columns=column_names)  # Set new column names

    for col in column_names:
        my_tree.column(col, anchor=W, width=120)
        my_tree.heading(col, text=col)

    # Fetch and display data
    if current_view == 'inventory':
        all_items = fetch_all_items_controller()
        for array in all_items:
            my_tree.insert('', 'end', values=(array))
    else:
        ledgerData = fetch_all_records_controller()
        for entry in ledgerData:
            formatted_entry = list(entry)  # Convert tuple to list
            formatted_entry[4] = f"{float(entry[4]):.2f}" 
            my_tree.insert('', 'end', values=tuple(formatted_entry))

    my_tree.pack()

# Validate Price and decimal values
def validate_number(P):
    return P == "" or P.replace(".", "", 1).isdigit()

# Validate name field
def validate_name(P):
    return P.isalpha()

# Clear Form
def clear_form():
    for var in placeholderArray:
        var.set("")

# Add Item to Inventory
def add_item():
    values = [var.get() for var in placeholderArray]
    
    # Validate name field
    if not values[1].replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name must be a string!")
        return

    # Validate category
    if values[2] not in ["Electronics", "Clothing", "Food", "Books", "Others"]:
        messagebox.showerror("Error", "Category must be Electronics, Clothing, Food, Books, or Others!")
        return

    # validate Price
    if values[3] == "":
        messagebox.showerror("Error", "Price must be a number!")
        return

    # Validate Quantity
    if values[4] == "" or not values[4].isdigit():
        messagebox.showerror("Error", "Quantity must be a number!")
        return

    success = add_item_controller(values[1], values[2], float(values[3]), int(values[4]))
    messagebox.showinfo("Success", "Item added successfully!" if success else "Item not added.")
    refreshTable()
    clear_form()

# Delete Item from Inventory
def delete_item():
    item_id = placeholderArray[0].get()
    if not item_id.isdigit():
        messagebox.showerror("Error", "Item ID must be a number!")
        return

    if messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?"):
        success = delete_item_controller(item_id)
        if success:
            messagebox.showinfo("Success", "Item deleted successfully!") 
        else:
            messagebox.showinfo("Item not found.")
    refreshTable()
    clear_form()

# Update Item in Inventory
def update_item():
    values = [var.get() for var in placeholderArray]

    # Validate id field
    if not values[0].isdigit():
        messagebox.showerror("Error", "Please enter the item Id to update!")
        return

    # Validate name field
    if not all(v.replace(" ", "").isalpha() for v in values[1]):
        messagebox.showerror("Error", "Name must be alphabetic!")
        return

    # Validate category
    if values[2] not in ["Electronics", "Clothing", "Food", "Books", "Others"]:
        messagebox.showerror("Error", "Category must be Electronics, Clothing, Food, Books, or Others!")
        return

    # validate Price
    if values[3] == "":
        messagebox.showerror("Error", "Price must be a number!")
        return

    # Validate Quantity
    if values[4] == "" or not values[4].isdigit():
        messagebox.showerror("Error", "Quantity must be a number!")
        return

    success = update_item_controller(int(values[0]), values[1], values[2], float(values[3]), int(values[4]))
    if success:
        messagebox.showinfo("Success", "Item updated successfully!")
    else:
        messagebox.showerror("Error", "Item not updated.")
    refreshTable()
    clear_form()


# Switch to the ledger view
def show_ledger():
    global current_view
    current_view = 'ledger'  # Change the view to ledger
    refreshTable()

# Switch to the inventory view
def show_inventory():
    global current_view
    current_view = 'inventory'  # Change the view to inventory
    refreshTable()

# UI Elements
frame = Frame(window, bg="#02577A")
frame.pack()

btnColor = "#196E78"
btnColor2 = "#02577A"

manageFrame = LabelFrame(frame, text="Manage", borderwidth=5)
manageFrame.grid(row=0, column=0, padx=[10, 200], pady=20)

# Buttons
createItemBtn = Button(manageFrame, text="Add", width=10, bg=btnColor, fg="white", command=add_item)
updateBtn = Button(manageFrame, text="Update", width=10, bg=btnColor, fg="white", command=update_item)
deleteBtn = Button(manageFrame, text="Delete", width=10, bg=btnColor, fg="white", command=delete_item)
clearBtn = Button(manageFrame, text="Clear", width=10, bg=btnColor, fg="white", command=clear_form)
inventoryBtn = Button(manageFrame, text="Inventory", width=10, bg=btnColor2, fg="white", command=show_inventory)
ledgerBtn = Button(manageFrame, text="Ledger", width=10, bg=btnColor2, fg="white", command=show_ledger)

# Layout
buttons = [createItemBtn, updateBtn, deleteBtn, clearBtn, inventoryBtn, ledgerBtn]
for i, btn in enumerate(buttons):
    btn.grid(row=0, column=i, padx=5, pady=5)

# Form Section
entriesFrame = LabelFrame(frame, text="Form", borderwidth=5)
entriesFrame.grid(row=1, column=0, padx=[10, 200], pady=[0, 20])

labels = ["Item ID", "Name", "Category", "Price", "Quantity"]
categoryArray = ["Electronics", "Clothing", "Food", "Books", "Others"]
entry_fields = []

for i, label in enumerate(labels):
    Label(entriesFrame, text=label, width=10, anchor="e").grid(row=i, column=0, padx=10, pady=10)
    
    if label == "Category":
        entry = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[i], values=categoryArray)
    elif label == "Name":
        entry = Entry(entriesFrame, width=50, textvariable=placeholderArray[i], validate="key", validatecommand=(window.register(validate_name), "%P"))
    else:
        entry = Entry(entriesFrame, width=50, textvariable=placeholderArray[i], validate="key",
                      validatecommand=(window.register(validate_number), "%P") if label in ["Price", "Quantity"] else None)
    
    entry.grid(row=i, column=2, padx=10, pady=10)
    entry_fields.append(entry)

# Treeview Configuration

my_tree.pack()

refreshTable()

window.resizable(False, False)
window.mainloop()
