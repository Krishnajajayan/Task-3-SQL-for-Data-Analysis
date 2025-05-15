#Import libraries
import pandas as pd
import sqlite3

#Load datasets
orders=pd.read_csv('orders.csv')
orders.head()

customers=pd.read_csv('customers.csv', encoding='latin-1')
customers.head()

#Create SQLite In-Memory Database
conn = sqlite3.connect(':memory:')

#Load DataFrames into SQLite
orders.to_sql('orders', conn, index=False, if_exists='replace')
customers.to_sql('customers', conn, index=False, if_exists='replace')

#Total orders per country
query1 = """
SELECT country, COUNT(orderID) AS total_orders
FROM customers
JOIN orders ON customers.customerID = orders.customerID
GROUP BY country
ORDER BY total_orders DESC;
"""
print("\n--- Total orders per country ---")
print(pd.read_sql_query(query1, conn).head(10))

#LEFT JOIN: All customers with their order count
query2 = """
SELECT companyName, COUNT(orderID) AS order_count
FROM customers
LEFT JOIN orders ON customers.customerID = orders.customerID
GROUP BY companyName
ORDER BY order_count DESC;
"""
print("\n--- LEFT JOIN: Customers and their order count ---")
print(pd.read_sql_query(query2, conn).head(10))

#RIGHT JOIN simulated: All orders with customer info
query3 = """
SELECT orders.orderID, customers.companyName, orders.orderDate
FROM orders
LEFT JOIN customers ON orders.customerID = customers.customerID
ORDER BY orders.orderDate;
"""
print("\n--- RIGHT JOIN simulated: Orders with customer info ---")
print(pd.read_sql_query(query3, conn).head(10))

#Customers with above-average order count (using subquery)
query4 = """
SELECT companyName, total_orders FROM (
    SELECT customers.companyName, COUNT(orders.orderID) AS total_orders
    FROM customers
    JOIN orders ON customers.customerID = orders.customerID
    GROUP BY customers.customerID
)
WHERE total_orders > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(orderID) AS order_count
        FROM orders
        GROUP BY customerID
    )
)
ORDER BY total_orders DESC;
"""
print("\n--- Customers with above-average order count ---")
print(pd.read_sql_query(query4, conn).head(10))

#Freight analysis per country (AVG and SUM)
query5 = """
SELECT country, AVG(freight) AS avg_freight, SUM(freight) AS total_freight
FROM customers
JOIN orders ON customers.customerID = orders.customerID
GROUP BY country
ORDER BY avg_freight DESC;
"""
print("\n--- Freight analysis per country ---")
print(pd.read_sql_query(query5, conn).head(10))

#Create view for customer order summary
conn.execute("""
CREATE VIEW IF NOT EXISTS customer_order_summary AS
SELECT customers.customerID, companyName, COUNT(orderID) AS total_orders, SUM(freight) AS total_freight
FROM customers
JOIN orders ON customers.customerID = orders.customerID
GROUP BY customers.customerID;
""")
print("\n--- View 'customer_order_summary' created ---")

#Create index to optimize queries on customerID in orders
conn.execute("CREATE INDEX IF NOT EXISTS idx_customerid ON orders(customerID);")
print("\n--- Index 'idx_customerid' created on orders(customerID) ---")

#Find customers who never placed an order
query6 = """
SELECT companyName, country
FROM customers
WHERE customerID NOT IN (
    SELECT DISTINCT customerID FROM orders
);
"""
print("\n--- Customers who never placed an order ---")
print(pd.read_sql_query(query6, conn).head(10))

#Count orders per city
query7 = """
SELECT city, COUNT(orderID) AS total_orders
FROM customers
JOIN orders ON customers.customerID = orders.customerID
GROUP BY city
ORDER BY total_orders DESC;
"""
print("\n--- Number of orders per city ---")
print(pd.read_sql_query(query7, conn).head(10))

#Top 5 customers by total freight paid
query8 = """
SELECT companyName, SUM(freight) AS total_freight
FROM customers
JOIN orders ON customers.customerID = orders.customerID
GROUP BY companyName
ORDER BY total_freight DESC
LIMIT 5;
"""
print("\n--- Top 5 customers by total freight paid ---")
print(pd.read_sql_query(query8, conn))

#Orders shipped later than required date (late deliveries)
query9 = """
SELECT orderID, orderDate, requiredDate, shippedDate
FROM orders
WHERE DATE(shippedDate) > DATE(requiredDate);
"""
print("\n--- Orders shipped later than required date ---")
print(pd.read_sql_query(query9, conn).head(10))

#Monthly order counts by year and month
query10 = """
SELECT
    strftime('%Y', orderDate) AS year,
    strftime('%m', orderDate) AS month,
    COUNT(orderID) AS order_count
FROM orders
GROUP BY year, month
ORDER BY year, month;
"""
print("\n--- Monthly order counts (year and month) ---")
print(pd.read_sql_query(query10, conn).head(10))

#Countries with most late deliveries
query11 = """
SELECT country, COUNT(*) AS late_orders
FROM customers
JOIN orders ON customers.customerID = orders.customerID
WHERE DATE(shippedDate) > DATE(requiredDate)
GROUP BY country
ORDER BY late_orders DESC;
"""
print("\n--- Countries with most late deliveries ---")
print(pd.read_sql_query(query11, conn).head(10))

#Customer with longest shipping delay
query12 = """
SELECT companyName, orderID, julianday(shippedDate) - julianday(orderDate) AS shipping_days
FROM customers
JOIN orders ON customers.customerID = orders.customerID
WHERE shippedDate IS NOT NULL AND orderDate IS NOT NULL
ORDER BY shipping_days DESC
LIMIT 1;
"""
print("\n--- Customer with longest shipping delay ---")
print(pd.read_sql_query(query12, conn))

#Average freight cost by employee who handled the order
query13 = """
SELECT employeeID, AVG(freight) AS avg_freight
FROM orders
GROUP BY employeeID
ORDER BY avg_freight DESC;
"""
print("\n--- Average freight cost by employee ---")
print(pd.read_sql_query(query13, conn))
