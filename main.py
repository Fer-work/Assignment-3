from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from controller import (add_item_controller, delete_item_controller, fetch_all_items_controller, update_item_controller, create_tables_controller)

# Initialize the main window
window = Tk()
window.title("Ledger System")
window.geometry("750x640")

# Treeview
my_tree = ttk.Treeview(window, show="headings", height=10)

placeholderArray = [StringVar() for _ in range(5)]

ledgerData = []  # This will store the ledger entries

# Global variable to track current view
current_view = 'inventory'  # Possible values: 'inventory', 'ledger'

create_tables_controller()  # Create tables if they don't exist

# Refresh Treeview based on the current view
def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    all_items = fetch_all_items_controller()

    if current_view == 'inventory':
        for array in all_items:
            my_tree.insert('', 'end', values=(array))
    elif current_view == 'ledger':
        for entry in ledgerData:
            my_tree.insert('', 'end', values=(entry))

    my_tree.pack()

# Validate Price and Quantity (Only Numbers)
def validate_number(P):
    return P.isdigit() or P == ""

# Clear Form
def clear_form():
    for var in placeholderArray:
        var.set("")

# Add Item to Inventory
def add_item():
    values = [var.get() for var in placeholderArray]
    
    # Validate Empty Fields
    if any(v.strip() == "" for v in values):
        messagebox.showerror("Error", "All fields must be filled out!")
        return

    # Validate Price & Quantity
    try:
        float(values[2])  # Price
        int(values[3])    # Quantity
    except ValueError:
        messagebox.showerror("Error", "Price must be a number, Quantity must be an integer!")
        return

    # Add to dummy data and refresh table
    new_id = len(dummyData) + 1
    dummyData.append([new_id] + values)
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
createItemBtn = Button(manageFrame, text="Create", width=10, bg=btnColor, fg="white", command=add_item)
updateBtn = Button(manageFrame, text="Update", width=10, bg=btnColor, fg="white")
deleteBtn = Button(manageFrame, text="Delete", width=10, bg=btnColor, fg="white")
selectBtn = Button(manageFrame, text="Select", width=10, bg=btnColor, fg="white")
findBtn = Button(manageFrame, text="Find", width=10, bg=btnColor, fg="white")
clearBtn = Button(manageFrame, text="Clear", width=10, bg=btnColor, fg="white", command=clear_form)
exportBtn = Button(manageFrame, text="Export Excel", width=10, bg=btnColor2, fg="white")
ledgerBtn = Button(manageFrame, text="Ledger", width=10, bg=btnColor2, fg="white", command=show_ledger)

# Layout
buttons = [createItemBtn, updateBtn, deleteBtn, selectBtn, findBtn, clearBtn, exportBtn, ledgerBtn]
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
    else:
        entry = Entry(entriesFrame, width=50, textvariable=placeholderArray[i], validate="key",
                      validatecommand=(window.register(validate_number), "%P") if label in ["Price", "Quantity"] else None)
    
    entry.grid(row=i, column=2, padx=10, pady=10)
    entry_fields.append(entry)

# Treeview Configuration
my_tree["columns"] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")

for col in my_tree["columns"]:
    my_tree.column(col, anchor=W, width=120)
    my_tree.heading(col, text=col)

my_tree.pack()

refreshTable()

window.resizable(False, False)
window.mainloop()
