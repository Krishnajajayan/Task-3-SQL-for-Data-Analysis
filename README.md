#  Northwind Orders & Customers Analysis using SQLite

This project explores customer and order data from the Northwind dataset using **SQLite** and **SQL queries**. It demonstrates key relational database concepts such as JOINs, aggregation, subqueries, views, and indexing.

---

## 📁 Dataset Files

- `orders.csv` — Contains customer order records
- `customers.csv` — Contains customer details

### orders.csv columns:
- orderID
- customerID
- employeeID
- orderDate
- requiredDate
- shippedDate
- shipperID
- freight

### customers.csv columns:
- customerID
- companyName
- contactName
- contactTitle
- city
- country

---

##  SQL Concepts Demonstrated

- INNER JOIN, LEFT JOIN, simulated RIGHT JOIN
- Aggregations with `COUNT`, `SUM`, `AVG`
- Subqueries and filtering
- Creating **views**
- Creating **indexes**
- Grouping and sorting data
- Date comparisons
- Monthly trend analysis

---

##  Key Questions Answered

1. Total orders per country
2. Customers and their order count
3. Orders with missing customers (simulated RIGHT JOIN)
4. Customers with above-average order counts
5. Freight analysis by country
6. Customers who never ordered
7. Orders per city
8. Top customers by freight paid
9. Late shipments
10. Monthly order trends
11. Countries with most late deliveries
12. Longest shipping delays
13. Average freight per employee

---

##  Views and Indexes

- **View**: `customer_order_summary`  
  Summarizes orders and freight per customer

- **Index**: `idx_customerid`  
  Created on `orders.customerID` for performance

---

##  What is SQLite?

> SQLite is a lightweight, serverless database engine embedded directly into applications.

- No need for a separate server
- Ideal for prototyping, small applications, and data analysis
- Entire database stored in a single file or memory
- Compatible with Python via `sqlite3`

---
