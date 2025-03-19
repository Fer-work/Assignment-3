from datetime import datetime
from model import (add_item, delete_item, fetch_item, fetch_all_items, update_item, add_record, create_tables)

# Function to create tables
def create_tables_controller():
    return create_tables()

# Function to add an item and log it in the ledger
def add_item_controller(itemName, category, price, quantity):
    success = add_item(itemName, category, price, quantity)
    if success:
        total_cost = price * quantity
        add_record("Added item", total_cost, 0, datetime.now().strftime("%Y-%m-%d"))
    return success

# Function to delete an item and log it in the ledger
def delete_item_controller(item_id):
    item = fetch_item(item_id)
    
    if not item:  # Handle case where item doesn't exist
        print(f"Error: Item with ID {item_id} not found.")
        return False
    
    success = delete_item(item_id)
    if success:
        total_cost = item[3] * item[4]  # price * quantity
        add_record("Deleted item", 0, total_cost, datetime.now().strftime("%Y-%m-%d"))  # Debit since value is removed
    return success

# Function to update an item and log it in the ledger
def update_item_controller(item_id, itemName, category, price, quantity):
    item = fetch_item(item_id)
    
    if not item:  # Handle case where item doesn't exist
        print(f"Error: Item with ID {item_id} not found.")
        return False

    old_total_cost = item[3] * item[4]  # price * quantity (before update)
    success = update_item(item_id, itemName, category, price, quantity)

    if success:
        new_total_cost = price * quantity
        cost_difference = new_total_cost - old_total_cost
        
        # Log only if there's a change in value
        if cost_difference > 0:
            add_record("Updated item (Increase)", cost_difference, 0, datetime.now().strftime("%Y-%m-%d"))
        elif cost_difference < 0:
            add_record("Updated item (Decrease)", 0, abs(cost_difference), datetime.now().strftime("%Y-%m-%d"))
        else:
            add_record("Updated item (No Change)", 0, 0, datetime.now().strftime("%Y-%m-%d"))

    return success

# Function to fetch all items
def fetch_all_items_controller():
    return fetch_all_items()
