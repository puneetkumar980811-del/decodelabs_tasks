-- ============================================================================
-- SQL INSIGHTS — e-commerce orders dataset (table: orders, 891 rows)
-- Demonstrates: SELECT, WHERE, ORDER BY, GROUP BY, COUNT, SUM, AVG
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q1. Basic SELECT — peek at the raw data (column selection + LIMIT)
-- ----------------------------------------------------------------------------
SELECT OrderID, Date, Product, Quantity, UnitPrice, TotalPrice, OrderStatus
FROM orders
ORDER BY Date
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q2. WHERE — filter rows: how many orders were actually delivered?
-- ----------------------------------------------------------------------------
SELECT OrderID, Product, TotalPrice, OrderStatus
FROM orders
WHERE OrderStatus = 'Delivered'
ORDER BY TotalPrice DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q3. WHERE with multiple conditions (AND / IN) — high-value orders that were
--     NOT completed (cancelled, returned, or pending)
-- ----------------------------------------------------------------------------
SELECT OrderID, Product, TotalPrice, OrderStatus, PaymentMethod
FROM orders
WHERE TotalPrice >= 2000
  AND OrderStatus IN ('Cancelled', 'Returned', 'Pending')
ORDER BY TotalPrice DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q4. ORDER BY — the 10 most expensive orders in the dataset
-- ----------------------------------------------------------------------------
SELECT OrderID, Date, Product, Quantity, UnitPrice, TotalPrice
FROM orders
ORDER BY TotalPrice DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q5. GROUP BY + COUNT — how many orders in each status?
-- ----------------------------------------------------------------------------
SELECT OrderStatus, COUNT(*) AS order_count
FROM orders
GROUP BY OrderStatus
ORDER BY order_count DESC;

-- ----------------------------------------------------------------------------
-- Q6. GROUP BY + SUM — total revenue per product (best sellers first)
-- ----------------------------------------------------------------------------
SELECT Product,
       COUNT(*)                  AS order_count,
       SUM(Quantity)             AS units_sold,
       SUM(TotalPrice)           AS revenue
FROM orders
GROUP BY Product
ORDER BY revenue DESC;

-- ----------------------------------------------------------------------------
-- Q7. GROUP BY + AVG — average basket size per payment method
-- ----------------------------------------------------------------------------
SELECT PaymentMethod,
       COUNT(*)      AS order_count,
       AVG(TotalPrice) AS avg_basket,
       SUM(TotalPrice) AS total_revenue
FROM orders
GROUP BY PaymentMethod
ORDER BY avg_basket DESC;

-- ----------------------------------------------------------------------------
-- Q8. GROUP BY + HAVING — which referral sources produced more than 150 orders,
--     and what revenue did each bring in?
-- ----------------------------------------------------------------------------
SELECT ReferralSource,
       COUNT(*)      AS order_count,
       SUM(TotalPrice) AS revenue,
       AVG(TotalPrice) AS avg_basket
FROM orders
GROUP BY ReferralSource
HAVING COUNT(*) > 150
ORDER BY revenue DESC;

-- ----------------------------------------------------------------------------
-- Q9. WHERE + GROUP BY + ORDER BY — monthly revenue trend for the full year 2024
--     (strftime extracts the month; demonstrates filtering before grouping)
-- ----------------------------------------------------------------------------
SELECT strftime('%Y-%m', Date) AS month,
       COUNT(*)                AS order_count,
       SUM(TotalPrice)         AS revenue,
       AVG(TotalPrice)         AS avg_basket
FROM orders
WHERE Date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY month
ORDER BY month;

-- ----------------------------------------------------------------------------
-- Q10. Aggregates with WHERE — summary comparison: delivered vs cancelled orders
-- ----------------------------------------------------------------------------
SELECT OrderStatus,
       COUNT(*)            AS order_count,
       SUM(TotalPrice)     AS revenue,
       AVG(TotalPrice)     AS avg_basket,
       AVG(Quantity)       AS avg_quantity
FROM orders
WHERE OrderStatus IN ('Delivered', 'Cancelled')
GROUP BY OrderStatus
ORDER BY order_count DESC;

-- ----------------------------------------------------------------------------
-- Q11. Coupon performance — average basket and revenue per coupon code
-- ----------------------------------------------------------------------------
SELECT CouponCode,
       COUNT(*)      AS order_count,
       SUM(TotalPrice) AS revenue,
       AVG(TotalPrice) AS avg_basket
FROM orders
GROUP BY CouponCode
ORDER BY avg_basket DESC;

-- ----------------------------------------------------------------------------
-- Q12. GROUP BY — average items in cart per product (order size by product)
-- ----------------------------------------------------------------------------
SELECT Product,
       COUNT(*)        AS order_count,
       AVG(ItemsInCart) AS avg_items_in_cart,
       AVG(Quantity)    AS avg_units_per_line
FROM orders
GROUP BY Product
ORDER BY avg_items_in_cart DESC;

-- ----------------------------------------------------------------------------
-- Q13. Aggregations — overall summary of the whole dataset (no GROUP BY)
-- ----------------------------------------------------------------------------
SELECT COUNT(*)                  AS total_orders,
       COUNT(DISTINCT CustomerID) AS unique_customers,
       SUM(TotalPrice)           AS total_revenue,
       AVG(TotalPrice)           AS avg_basket,
       MIN(TotalPrice)           AS min_order,
       MAX(TotalPrice)           AS max_order
FROM orders;

-- ----------------------------------------------------------------------------
-- Q14. WHERE + GROUP BY — which products are cancelled most often?
--      (cancelled share of each product's orders)
-- ----------------------------------------------------------------------------
SELECT Product,
       SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
       COUNT(*)                                                    AS total_orders
FROM orders
GROUP BY Product
ORDER BY cancelled_orders DESC;
