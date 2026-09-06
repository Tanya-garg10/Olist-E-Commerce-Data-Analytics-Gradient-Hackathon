# 🛒 Olist Brazilian E-Commerce: Business Analytics

> **Gradient Learnings Data Analytics Hackathon**  
> Team: Hackangers

## 📌 Project Title
**Decoding Customer Experience on Brazil's Largest E-Commerce Marketplace**

## 🏢 Problem Statement

Olist connects thousands of Brazilian sellers to customers through a unified marketplace. Despite strong order volume growth, the platform faces a critical challenge: **understanding what drives poor customer experiences and where to focus to sustain growth and satisfaction.**

The core questions:
- What is actually happening in the marketplace over time?
- Why do some customers give 1–2 star reviews?
- Which geographies, sellers, and categories carry the most risk?
- What practical actions should Olist take?

## 🎯 Business Objective

Analyze the Olist public e-commerce dataset to:
1. Quantify marketplace performance trends (orders, revenue, review scores)
2. Identify the primary drivers of low customer satisfaction
3. Surface geographic, seller, and category-level performance patterns
4. Deliver ranked, evidence-backed business recommendations

## 📦 Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| File | Description | Rows |
|------|------------|------|
| `olist_orders_dataset.csv` | Order headers, status, dates | 99,441 |
| `olist_order_items_dataset.csv` | Items per order, price, freight | 112,650 |
| `olist_order_payments_dataset.csv` | Payment details per order | 103,886 |
| `olist_order_reviews_dataset.csv` | Customer review scores & text | 100,000 |
| `olist_customers_dataset.csv` | Customer geography | 99,441 |
| `olist_products_dataset.csv` | Product metadata | 32,951 |
| `olist_sellers_dataset.csv` | Seller geography | 3,095 |
| `olist_geolocation_dataset.csv` | Zip code coordinates | 1,000,163 |
| `product_category_name_translation.csv` | PT→EN category names | 71 |

## ❓ Key Business Questions

1. Is the marketplace growing? Where are the inflection points?
2. How does delivery performance relate to customer satisfaction?
3. Which states have the worst delivery experience?
4. Which sellers need intervention?
5. Which product categories are dragging down ratings?
6. What factors are most strongly associated with 1–2 star reviews?
7. What can Olist do to measurably improve customer experience?

## 🔬 Methodology

Every analysis follows this structure:

```
Business Question → Data Preparation → Analysis → Visualization → Finding → Business Impact → Recommendation
```

Key principles:
- All findings calculated directly from the dataset (no fabricated numbers)
- Association clearly distinguished from causation
- Statistical rigor: group comparisons, distributions, effect sizes
- Business language used throughout (not statistical jargon)

## 🔑 Key Insights (Real Numbers)

| # | Insight | Evidence |
|---|---------|---------|
| 1 | Late deliveries devastate ratings | Late orders avg **2.26/5** vs **4.28/5** for early |
| 2 | Late delivery drives low reviews | **32.4%** of 1–2 star orders are late vs **2.9%** of 4–5 star |
| 3 | RJ is the highest-risk major state | **12.1% late rate** vs 4.5% for SP |
| 4 | 96.9% of customers never return | Only **2,997 / 96,096** unique customers bought twice |
| 5 | Office furniture has worst satisfaction | Avg score **3.48 / 5** (platform avg: 4.07) |
| 6 | Low-review orders pay more for freight | Avg R$27.74 vs R$22.04 (26% premium) |
| 7 | Credit card dominates at 76.1% share | Avg order value R$166.57 with avg 3.5 installments |

## 💡 Business Recommendations

| Priority | Recommendation |
|----------|---------------|
| 🔴 #1 | Late Delivery Early-Warning System (Day 5 trigger) |
| 🔴 #2 | Seller Accountability Scorecard with PIP thresholds |
| 🟠 #3 | RJ & High-Risk State Logistics Audit |
| 🟠 #4 | Post-Delivery Win-Back Email Campaign |
| 🟠 #5 | Category Quality Audits (office furniture, audio) |
| 🟡 #6 | Freight Cost Transparency at Checkout |
| 🟡 #7 | Geographically Optimized Seller Onboarding |
| 🟡 #8 | Automatic Compensation for Late Deliveries |

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Data:** pandas, numpy
- **Visualization:** matplotlib
- **Notebook:** Google Colab / Jupyter
- **Version Control:** Git / GitHub

## 📁 Project Structure

```
olist-data-analytics/
│
├── README.md                          ← This file
├── requirements.txt                   ← Python dependencies
├── .gitignore
│
├── notebooks/
│   └── Olist_Data_Analytics.ipynb     ← Main analysis notebook (16 sections)
│
├── data/
│   └── README.md                      ← Data source instructions
│
├── reports/
│   └── Analysis_Report.md             ← Professional analysis report
│
└── visuals/
    └── charts/                        ← All generated charts (auto-saved)
        ├── 01_kpi_overview.png
        ├── 02_marketplace_over_time.png
        ├── 03_delivery_satisfaction.png
        ├── 04_delivery_by_state.png
        ├── 05_seller_analysis.png
        ├── 06_category_analysis.png
        ├── 07_payment_analysis.png
        ├── 08_root_cause_analysis.png
        ├── 09_advanced_insights.png
        └── 10_executive_dashboard.png
```

## ▶️ How to Run

### Option A: Google Colab (Recommended)
1. Upload `Olist_Data_Analytics.ipynb` to [colab.research.google.com](https://colab.research.google.com)
2. Upload the dataset Excel file to the Colab session files
3. Update `DATA_FILE` variable in Cell 2 to match your filename
4. Run All → `Runtime > Run all`

### Option B: Local Jupyter
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/olist-data-analytics.git
cd olist-data-analytics

# Install dependencies
pip install -r requirements.txt

# Launch notebook
jupyter notebook notebooks/Olist_Data_Analytics.ipynb
```

### Data Setup
- Download the dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Place in `data/` directory or update `DATA_FILE` path in the notebook
- The notebook reads from a single consolidated Excel file with all 9 sheets

## 📄 License

Dataset: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (Olist/Kaggle)  
Code: MIT License
