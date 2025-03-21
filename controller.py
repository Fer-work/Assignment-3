from datetime import datetime
from model import (add_item, delete_item, fetch_item, fetch_all_items, update_item, add_record, create_tables, fetch_all_records, fetch_last_record)

# Function to create tables
def create_tables_controller():
    return create_tables()

# Function to add an item and log it in the ledger
def add_item_controller(itemName, category, price, quantity):
    success = add_item(itemName, category, price, quantity)

    last_record = fetch_last_record()  # Fetch the last ledger entry
    print(last_record)
    last_balance_total = last_record[4] if last_record else 0  # Use previous total balance or 0 if first record

    new_balance_total = last_balance_total + (price * quantity)  # Correct balance calculation

    if success:
        total_cost = price * quantity
        add_record("Added " + itemName, total_cost, 0, new_balance_total, datetime.now().strftime("%Y-%m-%d"))
    return success

# Function to delete an item and log it in the ledger
def delete_item_controller(item_id):
    deletedItem = fetch_item(item_id)
    if not deletedItem:
        print(f"Error: Item with ID {item_id} not found.")
        return False
    
    deletedItemName = deletedItem[1]
    total_cost = deletedItem[3] * deletedItem[4]  # price * quantity

    last_record = fetch_last_record()
    last_balance_total = last_record[4] if last_record else 0  # Use previous total balance or 0 if first record

    new_balance_total = last_balance_total - total_cost

    success = delete_item(item_id)
    if success:
        add_record("Deleted " + deletedItemName, 0, total_cost, new_balance_total, datetime.now().strftime("%Y-%m-%d"))
    return success


# Function to update an item and log it in the ledger
# Function to update an item and log it in the ledger
def update_item_controller(item_id, itemName, category, price, quantity):
    item = fetch_item(item_id)
    
    if not item:  # Handle case where item doesn't exist
        print(f"Error: Item with ID {item_id} not found.")
        return False

    old_total_cost = round(item[3] * item[4], 2)  # old price * old quantity
    success = update_item(item_id, itemName, category, price, quantity)

    if success:
        new_total_cost = round(price * quantity, 2)  # new price * new quantity
        cost_difference = round(new_total_cost - old_total_cost, 2)

        last_record = fetch_last_record()
        last_balance_total = round(last_record[4], 2) if last_record else 0.0  # Previous balance or 0 if first record
        new_balance_total = round(last_balance_total + cost_difference, 2)
        
        if cost_difference > 0:
            add_record(f"Updated (Increase) {itemName}", cost_difference, 0, new_balance_total, datetime.now().strftime("%Y-%m-%d"))
        elif cost_difference < 0:
            add_record(f"Updated (Decrease) {itemName}", 0, abs(cost_difference), new_balance_total, datetime.now().strftime("%Y-%m-%d"))
        else:
            add_record(f"Updated (No Change) {itemName}", 0, 0, new_balance_total, datetime.now().strftime("%Y-%m-%d"))

    return success

# Function to fetch all items
def fetch_all_items_controller():
    return fetch_all_items()

# Function to fetch all records
def fetch_all_records_controller():
    return fetch_all_records()