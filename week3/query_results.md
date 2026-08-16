# SQL Query Results

**Database:** orders.db  |  **Queries:** `queries.sql`

## Q1. Basic SELECT — peek at the raw data (column selection + LIMIT)

| OrderID | Date | Product | Quantity | UnitPrice | TotalPrice | OrderStatus |
|---|---|---|---|---|---|---|
| ORD200112 | 2023-01-01 | Monitor | 1 | 410.60 | 410.60 | Cancelled |
| ORD200236 | 2023-01-01 | Monitor | 1 | 318.81 | 318.81 | Pending |
| ORD200373 | 2023-01-02 | Laptop | 3 | 341.15 | 1,023.45 | Pending |
| ORD200645 | 2023-01-02 | Laptop | 2 | 150.05 | 300.10 | Cancelled |
| ORD200000 | 2023-01-04 | Monitor | 5 | 570.62 | 2,853.10 | Shipped |
| ORD200698 | 2023-01-04 | Laptop | 2 | 388.22 | 776.44 | Delivered |
| ORD200371 | 2023-01-05 | Phone | 5 | 307.76 | 1,538.80 | Pending |
| ORD200491 | 2023-01-05 | Phone | 5 | 420.70 | 2,103.50 | Pending |
| ORD200472 | 2023-01-06 | Chair | 3 | 508.12 | 1,524.36 | Cancelled |
| ORD200034 | 2023-01-07 | Chair | 4 | 576.52 | 2,306.08 | Pending |

## Q2. WHERE — filter rows: how many orders were actually delivered?

| OrderID | Product | TotalPrice | OrderStatus |
|---|---|---|---|
| ORD200789 | Tablet | 3,456.40 | Delivered |
| ORD200632 | Laptop | 3,390.80 | Delivered |
| ORD201065 | Printer | 3,334.00 | Delivered |
| ORD200361 | Printer | 3,299.25 | Delivered |
| ORD200511 | Monitor | 2,876.20 | Delivered |
| ORD200578 | Monitor | 2,830.35 | Delivered |
| ORD200883 | Printer | 2,807.40 | Delivered |
| ORD200781 | Phone | 2,621.30 | Delivered |
| ORD200587 | Monitor | 2,573.00 | Delivered |
| ORD200446 | Laptop | 2,547.90 | Delivered |

## Q3. WHERE with multiple conditions (AND / IN) — high-value orders that were NOT completed (cancelled, returned, or pending)

| OrderID | Product | TotalPrice | OrderStatus | PaymentMethod |
|---|---|---|---|---|
| ORD200328 | Tablet | 3,370.20 | Cancelled | Online |
| ORD200326 | Laptop | 3,352.40 | Returned | Gift Card |
| ORD201031 | Phone | 3,322.55 | Pending | Debit Card |
| ORD200367 | Laptop | 3,293.85 | Pending | Gift Card |
| ORD200527 | Chair | 3,267.35 | Cancelled | Credit Card |
| ORD200768 | Tablet | 3,267.30 | Cancelled | Cash |
| ORD200889 | Monitor | 3,253.60 | Cancelled | Credit Card |
| ORD200802 | Chair | 3,223.20 | Cancelled | Gift Card |
| ORD200957 | Monitor | 3,219.45 | Returned | Cash |
| ORD200086 | Printer | 3,215.15 | Cancelled | Online |

## Q4. ORDER BY — the 10 most expensive orders in the dataset

| OrderID | Date | Product | Quantity | UnitPrice | TotalPrice |
|---|---|---|---|---|---|
| ORD200789 | 2023-08-17 | Tablet | 5 | 691.28 | 3,456.40 |
| ORD200632 | 2023-05-02 | Laptop | 5 | 678.16 | 3,390.80 |
| ORD200328 | 2023-02-28 | Tablet | 5 | 674.04 | 3,370.20 |
| ORD200107 | 2023-03-27 | Printer | 5 | 670.75 | 3,353.75 |
| ORD200326 | 2024-07-01 | Laptop | 5 | 670.48 | 3,352.40 |
| ORD201065 | 2023-10-30 | Printer | 5 | 666.80 | 3,334.00 |
| ORD201031 | 2023-02-28 | Phone | 5 | 664.51 | 3,322.55 |
| ORD200463 | 2023-05-26 | Laptop | 5 | 662.78 | 3,313.90 |
| ORD200361 | 2024-06-29 | Printer | 5 | 659.85 | 3,299.25 |
| ORD200367 | 2024-04-25 | Laptop | 5 | 658.77 | 3,293.85 |

## Q5. GROUP BY + COUNT — how many orders in each status?

| OrderStatus | order_count |
|---|---|
| Cancelled | 192 |
| Delivered | 179 |
| Pending | 178 |
| Returned | 171 |
| Shipped | 171 |

## Q6. GROUP BY + SUM — total revenue per product (best sellers first)

| Product | order_count | units_sold | revenue |
|---|---|---|---|
| Printer | 139 | 415 | 154,092.31 |
| Tablet | 133 | 375 | 142,062.91 |
| Laptop | 127 | 386 | 140,869.64 |
| Chair | 130 | 399 | 136,974.18 |
| Monitor | 116 | 332 | 130,640.49 |
| Desk | 129 | 366 | 119,237.76 |
| Phone | 117 | 321 | 118,483.26 |

## Q7. GROUP BY + AVG — average basket size per payment method

| PaymentMethod | order_count | avg_basket | total_revenue |
|---|---|---|---|
| Credit Card | 180 | 1,162.50 | 209,250.88 |
| Gift Card | 181 | 1,053.81 | 190,739.54 |
| Cash | 183 | 1,044.31 | 191,109.57 |
| Debit Card | 169 | 1,012.95 | 171,188.14 |
| Online | 178 | 1,011.64 | 180,072.42 |

## Q8. GROUP BY + HAVING — which referral sources produced more than 150 orders, and what revenue did each bring in?

| ReferralSource | order_count | revenue | avg_basket |
|---|---|---|---|
| Instagram | 198 | 212,627.74 | 1,073.88 |
| Google | 175 | 198,869.08 | 1,136.39 |
| Email | 195 | 195,234.84 | 1,001.20 |
| Facebook | 161 | 173,951.15 | 1,080.44 |
| Referral | 162 | 161,677.74 | 998.01 |

## Q9. WHERE + GROUP BY + ORDER BY — monthly revenue trend for the full year 2024 (strftime extracts the month; demonstrates filtering before grouping)

| month | order_count | revenue | avg_basket |
|---|---|---|---|
| 2024-01 | 27 | 30,746.18 | 1,138.75 |
| 2024-02 | 23 | 28,618.13 | 1,244.27 |
| 2024-03 | 29 | 31,989.34 | 1,103.08 |
| 2024-04 | 40 | 38,137.04 | 953.43 |
| 2024-05 | 24 | 21,349.82 | 889.58 |
| 2024-06 | 34 | 44,510.36 | 1,309.13 |
| 2024-07 | 27 | 29,904.84 | 1,107.59 |
| 2024-08 | 21 | 20,926.05 | 996.48 |
| 2024-09 | 33 | 28,347.96 | 859.03 |
| 2024-10 | 26 | 33,184.72 | 1,276.34 |
| 2024-11 | 27 | 23,853.41 | 883.46 |
| 2024-12 | 30 | 27,092.32 | 903.08 |

## Q10. Aggregates with WHERE — summary comparison: delivered vs cancelled orders

| OrderStatus | order_count | revenue | avg_basket | avg_quantity |
|---|---|---|---|---|
| Cancelled | 192 | 215,330.40 | 1,121.51 | 2.97 |
| Delivered | 179 | 189,126.24 | 1,056.57 | 2.94 |

## Q11. Coupon performance — average basket and revenue per coupon code

| CouponCode | order_count | revenue | avg_basket |
|---|---|---|---|
| FREESHIP | 313 | 335,036.99 | 1,070.41 |
| SAVE10 | 286 | 304,840.02 | 1,065.87 |
| WINTER15 | 292 | 302,483.54 | 1,035.90 |

## Q12. GROUP BY — average items in cart per product (order size by product)

| Product | order_count | avg_items_in_cart | avg_units_per_line |
|---|---|---|---|
| Chair | 130 | 5.63 | 3.07 |
| Tablet | 133 | 5.54 | 2.82 |
| Monitor | 116 | 5.48 | 2.86 |
| Printer | 139 | 5.43 | 2.99 |
| Desk | 129 | 5.40 | 2.84 |
| Laptop | 127 | 5.39 | 3.04 |
| Phone | 117 | 5.32 | 2.74 |

## Q13. Aggregations — overall summary of the whole dataset (no GROUP BY)

| total_orders | unique_customers | total_revenue | avg_basket | min_order | max_order |
|---|---|---|---|---|---|
| 891 | 886 | 942,360.55 | 1,057.64 | 11.39 | 3,456.40 |

## Q14. WHERE + GROUP BY — which products are cancelled most often? (cancelled share of each product's orders)

| Product | cancelled_orders | total_orders |
|---|---|---|
| Laptop | 30 | 127 |
| Chair | 29 | 130 |
| Desk | 28 | 129 |
| Tablet | 28 | 133 |
| Monitor | 27 | 116 |
| Printer | 26 | 139 |
| Phone | 24 | 117 |
