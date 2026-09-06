# Data Directory

## Dataset Source
**Brazilian E-Commerce Public Dataset by Olist**  
Available at: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Why Data is Not Included
The raw dataset files are not included in this repository because:
1. Total size exceeds 100MB
2. The dataset is publicly available on Kaggle (free account required)
3. The Kaggle dataset license (CC BY-NC-SA 4.0) allows redistribution with attribution, but we respect the spirit of linking to the original source

## How to Get the Data

### Option 1: Download from Kaggle (Recommended)
1. Create a free Kaggle account at kaggle.com
2. Go to: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
3. Download and extract to this `data/` directory

### Option 2: Use the Pre-Consolidated Excel
If you received a consolidated Excel file (`olist_data.xlsx`) with all 9 sheets, place it here:
```
data/olist_data.xlsx
```

Then update the `DATA_FILE` variable in the notebook:
```python
DATA_FILE = '../data/olist_data.xlsx'
```

## Expected Files
```
data/
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_customers_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
├── olist_geolocation_dataset.csv
└── product_category_name_translation.csv
```

## Dataset Statistics
| Table | Rows | Columns |
|-------|------|---------|
| orders | 99,441 | 8 |
| order_items | 112,650 | 6 |
| order_payments | 103,886 | 5 |
| order_reviews | 100,000 | 7 |
| customers | 99,441 | 5 |
| products | 32,951 | 9 |
| sellers | 3,095 | 4 |
| geolocation | 1,000,163 | 5 |
| category_translation | 71 | 2 |
