import psycopg2
from datetime import datetime

# Database connection details (Replace these with your Neon.Tech credentials)
DB_NAME = 'neondb'
DB_USER = 'neondb_owner'
DB_PASSWORD = 'npg_xfdGCbUaA3i4'
DB_HOST = 'ep-shrill-cloud-a8m3s22c.eastus2.azure.neon.tech'

def connection():
    """Establishes a database connection and returns the connection object."""
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER,
        password=DB_PASSWORD, host=DB_HOST
    )

def create_tables():
    """Creates tables if they do not exist."""
    try:
        conn = connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ledgerPy (
                id SERIAL PRIMARY KEY, 
                operationName VARCHAR(100) NOT NULL,
                debit FLOAT NOT NULL,
                credit FLOAT NOT NULL,
                totalBalance FLOAT NOT NULL,
                date DATE NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS inventoryPy (
                id SERIAL PRIMARY KEY,
                itemName TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                price FLOAT NOT NULL,
                quantity INT NOT NULL,
                dateAdded DATE NOT NULL
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        return "Tables created successfully."
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")

def add_item(itemName, category, price, quantity):
    """Adds a new item to the inventory."""
    try:
        conn = connection()
        cur = conn.cursor()

        dateAdded = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO inventoryPy (itemName, category, price, quantity, dateAdded)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (itemName, category, price, quantity, dateAdded))
        
        item_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "id": item_id}
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")
    
def fetch_item(item_id):
    """Fetches a single item from the inventory."""
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventoryPy WHERE id = %s;", (item_id,))
        item = cur.fetchone()
        cur.close()
        conn.close()
        return item
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")

def fetch_all_items():
    """Fetches all items from the inventory."""
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventoryPy ORDER BY dateAdded DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")
    

def delete_item(item_id):
    """Deletes an item from the inventory."""
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM inventoryPy WHERE id = %s RETURNING id;", (item_id,))
        deleted_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted_id:
            return {"success": True, "id": deleted_id[0]}
        else:
            return {"success": False, "message": "Item not found."}
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")

def update_item(item_id, itemName, category, price, quantity):
    """Updates an item's details in the inventory."""
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE inventoryPy 
            SET itemName = %s, category = %s, price = %s, quantity = %s 
            WHERE id = %s
            RETURNING id;
        """, (itemName, category, price, quantity, item_id))
        
        updated_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if updated_id:
            return {"success": True, "id": updated_id[0]}
        else:
            return {"success": False, "message": "Item not found."}
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")

def add_record(operationName, debit, credit, date):
    """Adds a financial record to the ledger."""
    try:
        totalBalance = debit - credit  # Compute balance

        conn = connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ledgerPy (operationName, debit, credit, totalBalance, date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (operationName, debit, credit, totalBalance, date))
        
        record_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "id": record_id}
    
    except Exception as e:
        raise Exception(f"Database Error: {str(e)}")
