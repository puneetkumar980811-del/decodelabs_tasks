# Data Analysis Report

**Dataset:** Dataset for Data Analytics - Cleaned.xlsx — 891 orders, 14 columns
**Period:** 2023-01-01 → 2025-06-30

## 1. Basic Statistics

| Column | Count | Mean | Median | Std Dev | Min | Max |
|---|---|---|---|---|---|---|
| Quantity | 891 | 2.91 | 3.00 | 1.41 | 1.00 | 5.00 |
| UnitPrice | 891 | 360.60 | 371.29 | 196.75 | 11.39 | 699.93 |
| ItemsInCart | 891 | 5.46 | 5.00 | 2.28 | 1.00 | 10.00 |
| TotalPrice | 891 | 1,057.64 | 819.50 | 822.70 | 11.39 | 3,456.40 |

**Categorical counts (top 3 per column):**
- **Product:** Printer (139), Tablet (133), Chair (130)
- **PaymentMethod:** Cash (183), Gift Card (181), Credit Card (180)
- **OrderStatus:** Cancelled (192), Delivered (179), Pending (178)
- **ReferralSource:** Instagram (198), Email (195), Google (175)
- **CouponCode:** FREESHIP (313), WINTER15 (292), SAVE10 (286)

## 2. Trends Over Time

**Monthly orders & revenue:**
| Month | Orders | Revenue | Avg Basket |
|---|---|---|---|
| 2023-01 | 32 | $40,201 | $1,256.30 |
| 2023-02 | 25 | $25,882 | $1,035.30 |
| 2023-03 | 32 | $37,684 | $1,177.64 |
| 2023-04 | 23 | $20,900 | $908.70 |
| 2023-05 | 37 | $43,470 | $1,174.86 |
| 2023-06 | 31 | $33,779 | $1,089.66 |
| 2023-07 | 29 | $22,486 | $775.38 |
| 2023-08 | 37 | $37,710 | $1,019.19 |
| 2023-09 | 24 | $25,738 | $1,072.42 |
| 2023-10 | 41 | $49,379 | $1,204.36 |
| 2023-11 | 32 | $29,418 | $919.32 |
| 2023-12 | 34 | $34,036 | $1,001.07 |
| 2024-01 | 27 | $30,746 | $1,138.75 |
| 2024-02 | 23 | $28,618 | $1,244.27 |
| 2024-03 | 29 | $31,989 | $1,103.08 |
| 2024-04 | 40 | $38,137 | $953.43 |
| 2024-05 | 24 | $21,350 | $889.58 |
| 2024-06 | 34 | $44,510 | $1,309.13 |
| 2024-07 | 27 | $29,905 | $1,107.59 |
| 2024-08 | 21 | $20,926 | $996.48 |
| 2024-09 | 33 | $28,348 | $859.03 |
| 2024-10 | 26 | $33,185 | $1,276.34 |
| 2024-11 | 27 | $23,853 | $883.46 |
| 2024-12 | 30 | $27,092 | $903.08 |
| 2025-01 | 22 | $23,318 | $1,059.90 |
| 2025-02 | 27 | $27,516 | $1,019.10 |
| 2025-03 | 36 | $31,904 | $886.21 |
| 2025-04 | 24 | $25,218 | $1,050.76 |
| 2025-05 | 30 | $38,056 | $1,268.54 |
| 2025-06 | 34 | $37,004 | $1,088.34 |

**Yearly summary (2025 is partial — Jan to Jun only):**
- 2023: 377.0 orders, $400,685 revenue
- 2024: 341.0 orders, $358,660 revenue
- 2025: 173.0 orders, $183,015 revenue

**Seasonal index (avg orders/day vs peak month; full years 2023-2024 only):**
- Month 01: 88%
- Month 02: 79%
- Month 03: 91%
- Month 04: 97%
- Month 05: 91%
- Month 06: 100%
- Month 07: 83%
- Month 08: 86%
- Month 09: 88%
- Month 10: 100%
- Month 11: 91%
- Month 12: 95%

## 3. Outlier Detection (IQR method)
- **Quantity:** ok 0 outliers (bounds [-1.00, 7.00])
- **UnitPrice:** ok 0 outliers (bounds [-316.30, 1032.09])
- **ItemsInCart:** ok 0 outliers (bounds [-0.50, 11.50])
- **TotalPrice:** ! 6 outliers (bounds [-1332.24, 3329.16])

**Outlier order IDs:**
- TotalPrice: ORD200107, ORD200326, ORD200328, ORD200632, ORD200789, ORD201065

_Note: flagged outliers may be legitimate high-value orders rather than data errors — see Key Observations._

## 4. Distributions

**Order status:**
- Cancelled: 192 (21.5%)
- Delivered: 179 (20.1%)
- Pending: 178 (20.0%)
- Shipped: 171 (19.2%)
- Returned: 171 (19.2%)

**Payment method:**
- Cash: 183 (20.5%)
- Gift Card: 181 (20.3%)
- Credit Card: 180 (20.2%)
- Online: 178 (20.0%)
- Debit Card: 169 (19.0%)

**Product mix (% of orders):**
- Printer: 15.6%
- Tablet: 14.9%
- Chair: 14.6%
- Desk: 14.5%
- Laptop: 14.3%
- Phone: 13.1%
- Monitor: 13.0%

**Referral source:**
- Instagram: 198 (22.2%)
- Email: 195 (21.9%)
- Google: 175 (19.6%)
- Referral: 162 (18.2%)
- Facebook: 161 (18.1%)

**Revenue by product:**
- Printer: $154,092 (16.4% of revenue)
- Tablet: $142,063 (15.1% of revenue)
- Laptop: $140,870 (14.9% of revenue)
- Chair: $136,974 (14.5% of revenue)
- Monitor: $130,640 (13.9% of revenue)
- Desk: $119,238 (12.7% of revenue)
- Phone: $118,483 (12.6% of revenue)

**Coupon impact on average basket:**
- FREESHIP: $1,070.41 avg basket (n=313)
- SAVE10: $1,065.87 avg basket (n=286)
- WINTER15: $1,035.90 avg basket (n=292)

## Charts Generated
- `1_monthly_trend.png` saved
- `2_revenue_by_product.png` saved
- `3_price_distribution.png` saved
- `4_order_status.png` saved
- `5_quantity_distribution.png` saved
- `6_avg_basket_trend.png` saved

## 5. Key Observations
- ⚠️ **Cancellation risk:** 21.5% of orders are cancelled — worth investigating (payment failures? stock issues?).
- 📈 **Revenue trend:** strongest month was 2023-10 ($49,379); average basket is $1,057.64.
- 🏆 **Best product:** Printer generates the most revenue (16.4% of total).
- ↩️ **Returns:** 19.2% of orders are returned.
- 💰 **High-value orders:** 6 orders exceed the IQR upper bound ($3,456.40 max) — these are large baskets, not data errors (max possible = $699.93 x 5 units).