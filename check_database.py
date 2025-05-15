import sqlite3

def check_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('shipment_database.db')
    cursor = conn.cursor()
    
    # Check the product table
    cursor.execute("SELECT COUNT(*) FROM product")
    product_count = cursor.fetchone()[0]
    print(f"Number of products in database: {product_count}")
    
    # Check the shipment table
    cursor.execute("SELECT COUNT(*) FROM shipment")
    shipment_count = cursor.fetchone()[0]
    print(f"Number of shipments in database: {shipment_count}")
    
    # Show sample products
    print("\nSample products (up to 5):")
    cursor.execute("SELECT id, name FROM product LIMIT 5")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Name: {row[1]}")
    
    # Show sample shipments
    print("\nSample shipments (up to 5):")
    cursor.execute("""
        SELECT s.id, p.name, s.quantity, s.origin, s.destination 
        FROM shipment s
        JOIN product p ON s.product_id = p.id
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Product: {row[1]}, Quantity: {row[2]}, Origin: {row[3][:8]}..., Destination: {row[4][:8]}...")
    
    # Count by product
    print("\nProduct counts in shipments:")
    cursor.execute("""
        SELECT p.name, COUNT(s.id) as shipment_count, SUM(s.quantity) as total_quantity
        FROM product p
        JOIN shipment s ON p.id = s.product_id
        GROUP BY p.name
        ORDER BY total_quantity DESC
        LIMIT 10
    """)
    for row in cursor.fetchall():
        print(f"  Product: {row[0]}, Shipments: {row[1]}, Total Quantity: {row[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_database() 