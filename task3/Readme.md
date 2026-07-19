# Sales Data Analysis (Pandas)

A Jupyter Notebook project that loads a raw e-commerce sales dataset, cleans
it, filters and groups it in meaningful ways, and pulls out real business
insights — backed by four supporting charts.

---

## Dataset

`sales_data.csv` — a simulated e-commerce sales dataset with **1000+ orders**
across 4 regions, 5 product categories, and 5 payment modes. It's
intentionally messy to make the cleaning steps meaningful:

- Inconsistent text casing (`north` vs `North`, extra whitespace)
- Missing values in `OrderDate`, `Quantity`, `CustomerAge`, `Rating`
- Duplicate rows

| Column | Description |
|---|---|
| OrderID | Unique order identifier |
| OrderDate | Date of the order |
| Region | North / South / East / West |
| Category | Product category |
| Product | Product name |
| Quantity | Units ordered |
| UnitPrice | Price per unit (Rs) |
| Revenue | Quantity × UnitPrice |
| PaymentMode | UPI / Credit Card / Debit Card / Cash on Delivery / Net Banking |
| CustomerAge | Customer age (some missing) |
| Rating | Customer rating 1–5 (some missing) |

---

## Requirements

```bash
pip install pandas numpy matplotlib
```

To run the notebook itself you'll also need Jupyter:

```bash
pip install notebook
```

---

## How to Run

1. Keep `sales_data.csv` in the same folder as `sales_data_analysis.ipynb`
2. Open the folder in VS Code or Jupyter
3. Run all cells (VS Code: **Run All**; Jupyter: **Cell → Run All**)
4. Four `.png` charts are saved automatically in the same folder

---

## What the Notebook Does

1. **Load** — reads the CSV with `pandas.read_csv()`, inspects shape, dtypes, and summary stats
2. **Identify issues** — explicitly checks missing values, duplicate rows, and inconsistent text
3. **Clean**
   - Drops duplicate rows
   - Standardizes text casing/whitespace in `Region`, `Category`, `PaymentMode`
   - Parses `OrderDate` into proper datetime, drops unparseable rows
   - Fills missing `Quantity` with the column median
   - Recomputes `Revenue` for consistency after cleaning
4. **Filter** — examples include top 5% high-value orders, region + payment mode combos, and low-rated orders
5. **Group & aggregate** — total revenue by region, revenue/avg order value/count by category, monthly revenue trend, payment mode by region
6. **Insights** — top region, top category, best month, average rating, revenue share of high-value orders
7. **Visualize** — bar chart, horizontal bar chart, line chart, and pie chart, each saved as a `.png`

---

## Output Files

| File | Description |
|---|---|
| `revenue_by_region.png` | Total revenue per region |
| `revenue_by_category.png` | Total revenue per category |
| `monthly_revenue_trend.png` | Revenue trend across 2025 |
| `rating_distribution.png` | Customer rating breakdown |

---

## Key Insights (from this run)

- Revenue is fairly close across regions, with one region consistently ahead
- A small share of high-value orders (top 5%) contributes a disproportionate share of total revenue
- One category clearly leads in both total revenue and order volume
- A measurable share of orders are low-rated (1–2), worth digging into by product/category

---

## Project Structure

```
sales_data.csv               # raw dataset
sales_data_analysis.ipynb    # notebook: clean, filter, group, visualize
revenue_by_region.png
revenue_by_category.png
monthly_revenue_trend.png
rating_distribution.png
README.md
```
<img width="1522" height="823" alt="Screenshot 2026-07-18 210736" src="https://github.com/user-attachments/assets/8c95e044-8316-4383-af17-0bd24d129453" />
<img width="1527" height="855" alt="Screenshot 2026-07-18 210805" src="https://github.com/user-attachments/assets/d8cd3406-e59b-46ff-a512-010f04244c81" />
<img width="1535" height="852" alt="Screenshot 2026-07-18 210834" src="https://github.com/user-attachments/assets/8c27c036-a8af-4f27-a9f5-5f2cb50eebb8" />

---

## Author

Hemakanth Reddy
[GitHub](https://github.com/Hemakanthreddy) · [LinkedIn](https://linkedin.com/in/hemakanth-reddy)

## Report
[Sales_Data_Analysis_Report.docx](https://github.com/user-attachments/files/30160423/Sales_Data_Analysis_Report.docx)
