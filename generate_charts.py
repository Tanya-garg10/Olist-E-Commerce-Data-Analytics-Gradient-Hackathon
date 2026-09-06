"""
Chart generation script for Olist Data Analytics project.
Run this script to generate all 10 charts into visuals/charts/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import os
import warnings
warnings.filterwarnings('ignore')

# ── Config ─────────────────────────────────────────────────────────────────────
DATA_FILE = '../Document from singhlink4.xlsx'   # relative to script location
OUTDIR    = 'visuals/charts/'

os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

BLUE   = '#2E86AB'; GREEN  = '#27AE60'; RED    = '#E74C3C'; ORANGE = '#F39C12'
PURPLE = '#8E44AD'; TEAL   = '#1ABC9C'; GRAY   = '#7F8C8D'; DARK   = '#2C3E50'

# ── Load Data ──────────────────────────────────────────────────────────────────
print('Loading data...')
xl         = pd.ExcelFile(DATA_FILE)
orders     = xl.parse('orders')
items      = xl.parse('order_items')
payments   = xl.parse('order_payments')
reviews    = xl.parse('order_reviews')
customers  = xl.parse('customers')
products   = xl.parse('products')
sellers    = xl.parse('sellers')
geo        = xl.parse('geolocation')
cat_trans  = xl.parse('category_translation')

# ── Preprocessing ──────────────────────────────────────────────────────────────
print('Preprocessing...')
date_cols = ['order_purchase_timestamp','order_approved_at',
             'order_delivered_carrier_date','order_delivered_customer_date',
             'order_estimated_delivery_date']
for c in date_cols:
    orders[c] = pd.to_datetime(orders[c], errors='coerce')

products = products.merge(cat_trans, on='product_category_name', how='left')
products['category_en'] = products['product_category_name_english'].fillna(
    products['product_category_name'])

delivered = orders[
    (orders['order_status'] == 'delivered') &
    (orders['order_delivered_customer_date'].notna()) &
    (orders['order_estimated_delivery_date'].notna())
].copy()
delivered['delivery_days'] = (
    delivered['order_delivered_customer_date'] -
    delivered['order_purchase_timestamp']).dt.days
delivered['delay_days'] = (
    delivered['order_delivered_customer_date'] -
    delivered['order_estimated_delivery_date']).dt.days
delivered = delivered[delivered['delivery_days'].between(0, 365)]
delivered['delivery_status'] = delivered['delay_days'].apply(
    lambda x: 'Early' if x < 0 else ('On Time' if x == 0 else 'Late'))

items_agg = items.groupby('order_id').agg(
    item_count=('order_item_id','count'),
    order_revenue=('price','sum'),
    freight_total=('freight_value','sum')
).reset_index()

pay_agg = payments.groupby('order_id').agg(
    payment_value=('payment_value','sum'),
    payment_installments=('payment_installments','max'),
    payment_type=('payment_type', lambda x: x.mode()[0])
).reset_index()

rev_agg = reviews.groupby('order_id').agg(
    review_score=('review_score','mean')
).reset_index()

main = delivered.copy()
main = main.merge(items_agg,  on='order_id', how='left')
main = main.merge(pay_agg,    on='order_id', how='left')
main = main.merge(rev_agg,    on='order_id', how='left')
main = main.merge(
    customers[['customer_id','customer_unique_id','customer_state','customer_zip_code_prefix']],
    on='customer_id', how='left')

items_full = items.merge(products[['product_id','product_category_name','category_en']],
                         on='product_id', how='left')
items_full = items_full.merge(sellers[['seller_id','seller_state']], on='seller_id', how='left')
items_full = items_full.merge(rev_agg, on='order_id', how='left')
items_full = items_full.merge(
    delivered[['order_id','delivery_days','delay_days','delivery_status']],
    on='order_id', how='left')

main['month']      = main['order_purchase_timestamp'].dt.to_period('M')
main['low_review'] = main['review_score'] <= 2

platform_avg_review = rev_agg[rev_agg['order_id'].isin(delivered['order_id'])]['review_score'].mean()

# ── KPIs ───────────────────────────────────────────────────────────────────────
total_orders      = len(orders)
delivered_orders  = len(delivered)
total_revenue     = pay_agg[pay_agg['order_id'].isin(delivered['order_id'])]['payment_value'].sum()
avg_order_value   = pay_agg[pay_agg['order_id'].isin(delivered['order_id'])]['payment_value'].mean()
avg_review_score  = platform_avg_review
late_pct          = 100 * (delivered['delivery_status']=='Late').sum() / len(delivered)
on_time_pct       = 100 - late_pct
avg_delivery_days = delivered['delivery_days'].mean()
cancel_pct        = 100 * len(orders[orders['order_status'].isin(['canceled','unavailable'])]) / total_orders
total_sellers     = len(sellers)
total_unique_cust = customers['customer_unique_id'].nunique()
total_categories  = products['category_en'].nunique()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1: KPI Overview
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 1: KPI Overview...')
fig, axes = plt.subplots(3, 4, figsize=(18, 9))
fig.patch.set_facecolor('#F8F9FA')

kpis = [
    ('Total Orders',       f'{total_orders:,}',              BLUE),
    ('Delivered Orders',   f'{delivered_orders:,}',          GREEN),
    ('Total Revenue',      f'R$ {total_revenue/1e6:.2f}M',   TEAL),
    ('Avg Order Value',    f'R$ {avg_order_value:.2f}',      BLUE),
    ('Avg Review Score',   f'{avg_review_score:.2f} / 5',    GREEN),
    ('On-Time Delivery %', f'{on_time_pct:.1f}%',            GREEN),
    ('Late Delivery %',    f'{late_pct:.1f}%',               RED),
    ('Avg Delivery Days',  f'{avg_delivery_days:.1f} days',  ORANGE),
    ('Cancel / Unavail %', f'{cancel_pct:.2f}%',             ORANGE),
    ('Total Sellers',      f'{total_sellers:,}',             PURPLE),
    ('Unique Customers',   f'{total_unique_cust:,}',         PURPLE),
    ('Product Categories', f'{total_categories}',            TEAL),
]

for ax, (label, value, color) in zip(axes.flatten(), kpis):
    ax.set_facecolor('white'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.add_patch(plt.Rectangle((0.02,0.02),0.96,0.96,fill=True,facecolor='white',
                                edgecolor=color,linewidth=2.5,transform=ax.transAxes,clip_on=False))
    ax.text(0.5,0.62,value,ha='center',va='center',fontsize=20,fontweight='bold',color=color,transform=ax.transAxes)
    ax.text(0.5,0.28,label,ha='center',va='center',fontsize=9.5,color=DARK,transform=ax.transAxes)
    ax.axhline(y=0.08,xmin=0.05,xmax=0.95,color=color,linewidth=3,alpha=0.4)

fig.suptitle('Olist Marketplace — Key Performance Indicators',fontsize=18,fontweight='bold',color=DARK,y=1.01)
plt.tight_layout()
plt.savefig(OUTDIR+'01_kpi_overview.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 2: Marketplace Over Time
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 2: Marketplace Over Time...')
monthly = main.groupby('month').agg(
    orders        = ('order_id',       'count'),
    revenue       = ('order_revenue',  'sum'),
    avg_order_val = ('payment_value',  'mean'),
    avg_review    = ('review_score',   'mean'),
).reset_index()
monthly['month_str'] = monthly['month'].astype(str)
monthly = monthly.iloc[1:-1].reset_index(drop=True)

fig, axes = plt.subplots(2, 2, figsize=(18, 10))
fig.suptitle('Marketplace Performance Over Time (Monthly)', fontsize=16, fontweight='bold', color=DARK)

x = range(len(monthly))
xticks  = list(range(0, len(monthly), 3))
xlabels = [monthly['month_str'].iloc[i] for i in xticks]

ax = axes[0,0]
ax.fill_between(x, monthly['orders'], alpha=0.25, color=BLUE)
ax.plot(x, monthly['orders'], color=BLUE, linewidth=2.5, marker='o', markersize=4)
ax.set_title('Monthly Order Volume', fontweight='bold')
ax.set_ylabel('Number of Orders')
ax.set_xticks(xticks); ax.set_xticklabels(xlabels, rotation=45, ha='right')
peak_idx = monthly['orders'].idxmax()
ax.annotate(f"Peak: {monthly['orders'].max():,}\n{monthly['month_str'].iloc[peak_idx]}",
            xy=(peak_idx, monthly['orders'].max()),
            xytext=(max(0,peak_idx-4), monthly['orders'].max()-800),
            arrowprops=dict(arrowstyle='->', color=RED),
            fontsize=8.5, color=RED, fontweight='bold')

ax = axes[0,1]
ax.fill_between(x, monthly['revenue']/1e3, alpha=0.25, color=GREEN)
ax.plot(x, monthly['revenue']/1e3, color=GREEN, linewidth=2.5, marker='o', markersize=4)
ax.set_title('Monthly Revenue (R$ thousands)', fontweight='bold')
ax.set_ylabel('Revenue (R$ 000s)')
ax.set_xticks(xticks); ax.set_xticklabels(xlabels, rotation=45, ha='right')

ax = axes[1,0]
colors_review = [RED if v < 3.8 else GREEN for v in monthly['avg_review']]
ax.bar(x, monthly['avg_review'], color=colors_review, alpha=0.8)
ax.axhline(y=monthly['avg_review'].mean(), color=BLUE, linestyle='--',
           linewidth=1.5, label=f"Avg: {monthly['avg_review'].mean():.2f}")
ax.set_ylim(3, 5)
ax.set_title('Monthly Average Review Score', fontweight='bold')
ax.set_ylabel('Avg Review Score (1-5)')
ax.set_xticks(xticks); ax.set_xticklabels(xlabels, rotation=45, ha='right')
ax.legend()

ax = axes[1,1]
ax.plot(x, monthly['avg_order_val'], color=ORANGE, linewidth=2.5, marker='s', markersize=4)
ax.fill_between(x, monthly['avg_order_val'], alpha=0.15, color=ORANGE)
ax.set_title('Monthly Average Order Value (R$)', fontweight='bold')
ax.set_ylabel('Avg Order Value (R$)')
ax.set_xticks(xticks); ax.set_xticklabels(xlabels, rotation=45, ha='right')

plt.tight_layout()
plt.savefig(OUTDIR+'02_marketplace_over_time.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 3: Delivery Satisfaction
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 3: Delivery Satisfaction...')
delivery_review = main.groupby('delivery_status').agg(
    count      = ('order_id',     'count'),
    avg_review = ('review_score', 'mean'),
    pct_low    = ('low_review',   'mean')
).reset_index()
delivery_review['pct_low'] *= 100

status_order  = ['Early', 'On Time', 'Late']
status_colors = [GREEN, BLUE, RED]
dr = delivery_review.set_index('delivery_status').reindex(status_order)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Delivery Performance & Customer Satisfaction', fontsize=16, fontweight='bold', color=DARK)

ax = axes[0]
bars = ax.bar(status_order, dr['avg_review'], color=status_colors, width=0.5, edgecolor='white', linewidth=1.5)
ax.set_ylim(0, 5.5)
ax.set_title('Avg Review Score by Delivery Status', fontweight='bold')
ax.set_ylabel('Average Review Score (1-5)')
for bar, val in zip(bars, dr['avg_review']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.08,
            f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')
ax.axhline(y=4.07, color=GRAY, linestyle='--', linewidth=1.2, label='Platform Avg: 4.07')
ax.legend()

ax = axes[1]
bars2 = ax.bar(status_order, dr['pct_low'], color=status_colors, width=0.5, edgecolor='white', linewidth=1.5)
ax.set_title('% Low Reviews (≤2) by Delivery Status', fontweight='bold')
ax.set_ylabel('% Orders with Low Review')
for bar, val in zip(bars2, dr['pct_low']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')

ax = axes[2]
sample = main.dropna(subset=['delay_days','review_score']).sample(min(5000,len(main)), random_state=42)
scatter_colors = sample['delivery_status'].map({'Early': GREEN, 'On Time': BLUE, 'Late': RED})
ax.scatter(sample['delay_days'], sample['review_score'], c=scatter_colors, alpha=0.25, s=12)
ax.set_xlabel('Delay Days (negative = arrived early)')
ax.set_ylabel('Review Score')
ax.set_title('Delay Days vs Review Score', fontweight='bold')
ax.axvline(x=0, color=DARK, linestyle='--', linewidth=1, alpha=0.6, label='Est. delivery date')
patches = [mpatches.Patch(color=c, label=s) for s, c in zip(status_order, status_colors)]
ax.legend(handles=patches, fontsize=8)

plt.tight_layout()
plt.savefig(OUTDIR+'03_delivery_satisfaction.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 4: Delivery by State
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 4: Delivery by State...')
state_delivery = main.groupby('customer_state').agg(
    orders       = ('order_id',       'count'),
    avg_review   = ('review_score',   'mean'),
    avg_delay    = ('delay_days',     'mean'),
    avg_del_days = ('delivery_days',  'mean'),
    late_pct     = ('delivery_status', lambda x: 100*(x=='Late').sum()/len(x))
).reset_index().sort_values('late_pct', ascending=False)

top_states = state_delivery[state_delivery['orders'] >= 100]

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Delivery Performance by Customer State', fontsize=16, fontweight='bold', color=DARK)

ax = axes[0]
plot_data = top_states.head(15).sort_values('late_pct')
bar_colors = [RED if v>10 else ORANGE if v>6 else GREEN for v in plot_data['late_pct']]
ax.barh(plot_data['customer_state'], plot_data['late_pct'], color=bar_colors, edgecolor='white')
ax.axvline(x=late_pct, color=DARK, linestyle='--', linewidth=1.5, label=f'Platform Avg: {late_pct:.1f}%')
ax.set_title('Late Delivery % by State (min 100 orders)', fontweight='bold')
ax.set_xlabel('Late Delivery %')
ax.legend()

ax = axes[1]
vol_states = state_delivery[state_delivery['orders']>=100].sort_values('orders',ascending=False).head(15).sort_values('avg_del_days')
bar_colors2 = [RED if v>20 else ORANGE if v>15 else GREEN for v in vol_states['avg_del_days']]
ax.barh(vol_states['customer_state'], vol_states['avg_del_days'], color=bar_colors2, edgecolor='white')
ax.axvline(x=avg_delivery_days, color=DARK, linestyle='--', linewidth=1.5,
           label=f'Platform Avg: {avg_delivery_days:.1f}d')
ax.set_title('Avg Delivery Days — Top 15 States by Volume', fontweight='bold')
ax.set_xlabel('Average Delivery Days')
ax.legend()

plt.tight_layout()
plt.savefig(OUTDIR+'04_delivery_by_state.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 5: Seller Analysis
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 5: Seller Analysis...')
seller_perf = items_full.groupby('seller_id').agg(
    orders      = ('order_id',       'nunique'),
    revenue     = ('price',          'sum'),
    avg_review  = ('review_score',   'mean'),
    avg_delay   = ('delay_days',     'mean'),
    late_pct    = ('delivery_status', lambda x: 100*(x=='Late').sum()/len(x)),
    avg_freight = ('freight_value',  'mean'),
    seller_state= ('seller_state',   'first')
).reset_index()

seller_min = seller_perf[seller_perf['orders'] >= 20].copy()
seller_min['segment'] = 'Average'
seller_min.loc[(seller_min['avg_review']>=4.3)&(seller_min['orders']>=50),'segment']='Top Performer'
seller_min.loc[(seller_min['avg_review']<3.5)|(seller_min['late_pct']>20),'segment']='At Risk'
seller_min.loc[(seller_min['orders']>=100)&(seller_min['avg_review']<4.0),'segment']='High Vol Low Sat'

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Seller Performance Analysis', fontsize=16, fontweight='bold', color=DARK)

ax = axes[0]
seg_colors = {'Top Performer': GREEN, 'At Risk': RED, 'High Vol Low Sat': ORANGE, 'Average': BLUE}
for seg, grp in seller_min.groupby('segment'):
    ax.scatter(grp['orders'], grp['avg_review'],
               s=np.clip(grp['revenue']/2000, 20, 300),
               color=seg_colors[seg], alpha=0.6, label=seg)
ax.set_xlabel('Number of Orders')
ax.set_ylabel('Average Review Score')
ax.set_title('Seller Orders vs Review Score\n(bubble = revenue)', fontweight='bold')
ax.axhline(y=4.07, color=GRAY, linestyle='--', linewidth=1.2, label='Platform Avg')
ax.legend(fontsize=8)

ax = axes[1]
state_sellers = seller_perf.groupby('seller_state').agg(
    seller_count=('seller_id','count'),
    total_orders=('orders','sum')
).reset_index().sort_values('seller_count',ascending=False).head(10)
ax.bar(state_sellers['seller_state'], state_sellers['seller_count'], color=PURPLE, alpha=0.8)
ax.set_title('Seller Count by State (Top 10)', fontweight='bold')
ax.set_xlabel('Seller State'); ax.set_ylabel('Number of Sellers')

plt.tight_layout()
plt.savefig(OUTDIR+'05_seller_analysis.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 6: Category Analysis
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 6: Category Analysis...')
cat_perf = items_full.groupby('category_en').agg(
    orders      = ('order_id',       'count'),
    revenue     = ('price',          'sum'),
    avg_price   = ('price',          'mean'),
    avg_freight = ('freight_value',  'mean'),
    avg_review  = ('review_score',   'mean'),
    late_pct    = ('delivery_status', lambda x: 100*(x=='Late').sum()/len(x))
).reset_index()
cat_perf = cat_perf[cat_perf['orders'] >= 50].copy()
cat_perf['review_vs_avg'] = cat_perf['avg_review'] - platform_avg_review

top_by_volume  = cat_perf.nlargest(15,'orders')
low_review_cat = cat_perf.nsmallest(10,'avg_review')

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
fig.suptitle('Product Category Performance Analysis', fontsize=16, fontweight='bold', color=DARK)

ax = axes[0,0]
tv = top_by_volume.sort_values('orders')
ax.barh(tv['category_en'], tv['orders'], color=BLUE, alpha=0.85)
ax.set_title('Top 15 Categories by Order Volume', fontweight='bold')
ax.set_xlabel('Number of Orders')

ax = axes[0,1]
tv_sorted = top_by_volume.sort_values('avg_review')
bar_colors = [RED if v<platform_avg_review else GREEN for v in tv_sorted['avg_review']]
ax.barh(tv_sorted['category_en'], tv_sorted['avg_review'], color=bar_colors, alpha=0.85)
ax.axvline(x=platform_avg_review, color=DARK, linestyle='--', linewidth=1.5,
           label=f'Platform Avg: {platform_avg_review:.2f}')
ax.set_xlim(3, 5)
ax.set_title('Avg Review Score — Top 15 Categories', fontweight='bold')
ax.set_xlabel('Average Review Score')
ax.legend()

ax = axes[1,0]
lr = low_review_cat.sort_values('avg_review')
ax.barh(lr['category_en'], lr['avg_review'], color=RED, alpha=0.75)
ax.axvline(x=platform_avg_review, color=BLUE, linestyle='--', linewidth=1.5,
           label=f'Platform Avg: {platform_avg_review:.2f}')
ax.set_xlim(2.5, 5)
ax.set_title('10 Lowest-Rated Categories (min 50 orders)', fontweight='bold')
ax.set_xlabel('Average Review Score')
ax.legend()

ax = axes[1,1]
scatter = ax.scatter(cat_perf['avg_freight'], cat_perf['avg_review'],
                     s=np.clip(cat_perf['orders']/20,20,400),
                     c=cat_perf['late_pct'], cmap='RdYlGn_r',
                     alpha=0.7, edgecolors='gray', linewidth=0.5)
plt.colorbar(scatter, ax=ax, label='Late Delivery %')
ax.set_xlabel('Avg Freight Cost (R$)')
ax.set_ylabel('Avg Review Score')
ax.set_title('Freight Cost vs Review Score\n(bubble=orders, color=late%)', fontweight='bold')
ax.axhline(y=platform_avg_review, color=GRAY, linestyle='--', linewidth=1, alpha=0.7)

plt.tight_layout()
plt.savefig(OUTDIR+'06_category_analysis.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 7: Payment Analysis
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 7: Payment Analysis...')
pay_full = pay_agg.merge(rev_agg, on='order_id', how='left')
pay_full = pay_full[pay_full['payment_type'] != 'not_defined']

pt_summary = pay_full.groupby('payment_type').agg(
    count       = ('order_id',             'count'),
    avg_value   = ('payment_value',        'mean'),
    avg_review  = ('review_score',         'mean'),
    avg_install = ('payment_installments', 'mean')
).reset_index().sort_values('count', ascending=False)
pt_summary['share_pct'] = 100 * pt_summary['count'] / pt_summary['count'].sum()

pay_colors = {'credit_card': BLUE, 'boleto': GREEN, 'voucher': ORANGE, 'debit_card': PURPLE}
pt_order   = list(pt_summary['payment_type'])
colors_list= [pay_colors.get(p, GRAY) for p in pt_order]

fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle('Payment Behavior Analysis', fontsize=16, fontweight='bold', color=DARK)

ax = axes[0,0]
wedge_colors = [pay_colors.get(p, GRAY) for p in pt_order]
ax.pie(pt_summary['count'], labels=pt_order, colors=wedge_colors,
       autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9.5})
ax.set_title('Payment Method Distribution', fontweight='bold')

ax = axes[0,1]
bars = ax.bar(pt_order, pt_summary['avg_value'], color=colors_list, alpha=0.85)
ax.set_title('Avg Order Value by Payment Type (R$)', fontweight='bold')
ax.set_ylabel('Avg Order Value (R$)')
for bar, val in zip(bars, pt_summary['avg_value']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
            f'R${val:.0f}', ha='center', fontsize=9)

ax = axes[1,0]
cc = pay_full[pay_full['payment_type']=='credit_card']
cc_inst = cc[cc['payment_installments'].between(1,12)]
inst_summary = cc_inst.groupby('payment_installments').agg(
    count=('order_id','count'), avg_value=('payment_value','mean')
).reset_index()
ax.bar(inst_summary['payment_installments'], inst_summary['avg_value'],
       color=BLUE, alpha=0.8)
ax.set_title('Credit Card: Avg Order Value by Installments', fontweight='bold')
ax.set_xlabel('Number of Installments')
ax.set_ylabel('Avg Order Value (R$)')

ax = axes[1,1]
bars4 = ax.bar(pt_order, pt_summary['avg_review'], color=colors_list, alpha=0.85)
ax.axhline(y=4.07, color=DARK, linestyle='--', linewidth=1.5, label='Platform Avg: 4.07')
ax.set_ylim(3.5, 4.5)
ax.set_title('Avg Review Score by Payment Type\n(association only, not causation)', fontweight='bold')
ax.set_ylabel('Avg Review Score')
for bar, val in zip(bars4, pt_summary['avg_review']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
            f'{val:.3f}', ha='center', fontsize=9)
ax.legend()

plt.tight_layout()
plt.savefig(OUTDIR+'07_payment_analysis.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 8: Root Cause Analysis
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 8: Root Cause Analysis...')
low  = main[main['low_review'] == True]
high = main[main['low_review'] == False]

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Root Cause Analysis — Factors Associated with Low Review Scores (≤2)',
             fontsize=15, fontweight='bold', color=DARK)

ax = axes[0,0]
ax.hist(high['delay_days'].clip(-30,50), bins=40, alpha=0.6, color=GREEN, label='High Review (>2)', density=True)
ax.hist(low['delay_days'].clip(-30,50),  bins=40, alpha=0.6, color=RED,   label='Low Review (≤2)',  density=True)
ax.axvline(x=0, color=DARK, linestyle='--', linewidth=1.2, label='Est. Delivery')
ax.set_xlabel('Delay Days'); ax.set_ylabel('Density')
ax.set_title('Delivery Delay Distribution', fontweight='bold')
ax.legend(fontsize=8)

ax = axes[0,1]
low_status  = low['delivery_status'].value_counts(normalize=True)*100
high_status = high['delivery_status'].value_counts(normalize=True)*100
status_cats = ['Early','On Time','Late']
low_vals  = [low_status.get(s,0)  for s in status_cats]
high_vals = [high_status.get(s,0) for s in status_cats]
x = np.arange(len(status_cats))
ax.bar(x-0.2, high_vals, 0.4, label='High Review', color=GREEN, alpha=0.8)
ax.bar(x+0.2, low_vals,  0.4, label='Low Review',  color=RED,   alpha=0.8)
ax.set_xticks(x); ax.set_xticklabels(status_cats)
ax.set_title('Delivery Status Split', fontweight='bold')
ax.set_ylabel('% of Orders')
ax.legend()
for xi,(hv,lv) in enumerate(zip(high_vals,low_vals)):
    ax.text(xi-0.2,hv+0.3,f'{hv:.1f}%',ha='center',fontsize=7)
    ax.text(xi+0.2,lv+0.3,f'{lv:.1f}%',ha='center',fontsize=7)

ax = axes[0,2]
main_clean = main.dropna(subset=['delivery_days','review_score'])
bins=[0,5,10,15,20,25,30,999]
labels_bins=['0-5','6-10','11-15','16-20','21-25','26-30','30+']
main_clean = main_clean.copy()
main_clean['del_bin'] = pd.cut(main_clean['delivery_days'],bins=bins,labels=labels_bins)
bin_review = main_clean.groupby('del_bin',observed=True)['review_score'].mean()
ax.plot(labels_bins, bin_review.values, marker='o', color=ORANGE, linewidth=2.5)
ax.set_xlabel('Delivery Days (binned)'); ax.set_ylabel('Avg Review Score')
ax.set_title('Review Score by Delivery Time Bucket', fontweight='bold')
ax.set_ylim(3, 5)
ax.fill_between(labels_bins, bin_review.values, 3, alpha=0.2, color=ORANGE)

ax = axes[1,0]
ax.hist(high['freight_total'].clip(0,100), bins=30, alpha=0.6, color=GREEN, label='High Review', density=True)
ax.hist(low['freight_total'].clip(0,100),  bins=30, alpha=0.6, color=RED,   label='Low Review',  density=True)
ax.set_xlabel('Freight Cost (R$)'); ax.set_ylabel('Density')
ax.set_title(f'Freight Cost Distribution\nLow avg=R${low["freight_total"].mean():.2f} | High avg=R${high["freight_total"].mean():.2f}', fontweight='bold')
ax.legend()

ax = axes[1,1]
impact_data = {
    'Late Delivery\n(% orders)':  (100*(low['delivery_status']=='Late').mean(), 100*(high['delivery_status']=='Late').mean()),
    'Delivery Days\n(norm)':       (low['delivery_days'].mean()/30, high['delivery_days'].mean()/30),
    'Freight Cost\n(norm)':        (low['freight_total'].mean()/100, high['freight_total'].mean()/100),
    'Order Value\n(norm)':         (low['payment_value'].mean()/500, high['payment_value'].mean()/500),
}
cats=[k for k in impact_data]; low_n=[v[0] for v in impact_data.values()]; high_n=[v[1] for v in impact_data.values()]
x=np.arange(len(cats))
ax.bar(x-0.2,high_n,0.4,label='High Review',color=GREEN,alpha=0.8)
ax.bar(x+0.2,low_n, 0.4,label='Low Review', color=RED,  alpha=0.8)
ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=8)
ax.set_title('Normalized Factor Comparison',fontweight='bold')
ax.legend(fontsize=8)

ax = axes[1,2]
score_counts = main['review_score'].round().value_counts().sort_index()
colors_score = [RED, RED, ORANGE, GREEN, GREEN]
ax.bar(score_counts.index, score_counts.values, color=colors_score[:len(score_counts)], alpha=0.85)
ax.set_xlabel('Review Score'); ax.set_ylabel('Number of Orders')
ax.set_title(f'Overall Review Score Distribution\n(Mean={main["review_score"].mean():.2f})',fontweight='bold')
for score,count in zip(score_counts.index,score_counts.values):
    ax.text(score,count+200,f'{100*count/len(main):.1f}%',ha='center',fontsize=9)

plt.tight_layout()
plt.savefig(OUTDIR+'08_root_cause_analysis.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 9: Advanced Insights
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 9: Advanced Insights...')
repeat_analysis  = customers.groupby('customer_unique_id').size().reset_index(name='order_count')
repeat_customers = repeat_analysis[repeat_analysis['order_count'] > 1]
single_customers = repeat_analysis[repeat_analysis['order_count'] == 1]

main['day_of_week'] = main['order_purchase_timestamp'].dt.day_name()
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow_perf  = main.groupby('day_of_week').agg(
    orders=('order_id','count'), avg_review=('review_score','mean')
).reindex(dow_order)

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle('Advanced Insights', fontsize=15, fontweight='bold', color=DARK)

ax = axes[0]
labels_r = [f'One-Time\n({len(single_customers):,})', f'Repeat\n({len(repeat_customers):,})']
ax.pie([len(single_customers),len(repeat_customers)], labels=labels_r,
       colors=[BLUE,GREEN], autopct='%1.1f%%', startangle=90,
       textprops={'fontsize':11})
ax.set_title('Customer Retention\n(Repeat vs One-Time)', fontweight='bold')

ax = axes[1]
ax.bar(dow_order, dow_perf['orders'], color=BLUE, alpha=0.75)
ax2 = ax.twinx()
ax2.plot(dow_order, dow_perf['avg_review'], color=RED, linewidth=2.5, marker='o', markersize=6)
ax.set_ylabel('Number of Orders', color=BLUE)
ax2.set_ylabel('Avg Review Score', color=RED)
ax.set_title('Order Volume & Review Score by Day of Week', fontweight='bold')
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig(OUTDIR+'09_advanced_insights.png', bbox_inches='tight', dpi=150)
plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# CHART 10: Executive Dashboard
# ══════════════════════════════════════════════════════════════════════════════
print('Generating chart 10: Executive Dashboard...')
fig = plt.figure(figsize=(22, 18))
fig.patch.set_facecolor('#F0F2F6')
gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.55, wspace=0.4)

ax_title = fig.add_subplot(gs[0, :])
ax_title.set_facecolor(DARK)
ax_title.text(0.5, 0.65, 'OLIST MARKETPLACE — EXECUTIVE INSIGHT DASHBOARD',
              ha='center', va='center', fontsize=18, fontweight='bold',
              color='white', transform=ax_title.transAxes)
ax_title.text(0.5, 0.2,
              'Brazilian E-Commerce Analytics | 99,441 Orders | 2016-2018 | Gradient Learnings Hackathon',
              ha='center', va='center', fontsize=10, color='#BDC3C7', transform=ax_title.transAxes)
ax_title.axis('off')

ax_a = fig.add_subplot(gs[1, :2])
x = range(len(monthly))
ax_a.fill_between(x, monthly['orders'], alpha=0.3, color=BLUE)
ax_a.plot(x, monthly['orders'], color=BLUE, linewidth=2)
xticks = list(range(0, len(monthly), 4))
ax_a.set_xticks(xticks)
ax_a.set_xticklabels([monthly['month_str'].iloc[i] for i in xticks], rotation=45, fontsize=7)
ax_a.set_title('Monthly Order Volume', fontweight='bold', fontsize=10)
ax_a.set_ylabel('Orders')

ax_b = fig.add_subplot(gs[1, 2:])
dr_vals = []
for s in status_order:
    row = delivery_review[delivery_review['delivery_status']==s]
    dr_vals.append(row['avg_review'].values[0] if len(row)>0 else 0)
bars = ax_b.bar(status_order, dr_vals, color=status_colors, width=0.5, alpha=0.85)
ax_b.set_ylim(0, 5.5)
ax_b.set_title('Avg Review Score by Delivery Status', fontweight='bold', fontsize=10)
ax_b.set_ylabel('Avg Review Score')
ax_b.axhline(y=4.07, color=GRAY, linestyle='--', linewidth=1)
for bar, val in zip(bars, dr_vals):
    ax_b.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.08,
              f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')

ax_c = fig.add_subplot(gs[2, :2])
top10_cat = cat_perf.nlargest(10,'orders').sort_values('orders')
bar_c_colors = [RED if v<platform_avg_review else GREEN for v in top10_cat['avg_review']]
ax_c.barh(top10_cat['category_en'], top10_cat['orders'], color=bar_c_colors, alpha=0.85)
ax_c.set_title('Top 10 Categories by Volume\n(green=above avg review)', fontweight='bold', fontsize=10)
ax_c.set_xlabel('Orders')

ax_d = fig.add_subplot(gs[2, 2:])
top10_states = state_delivery[state_delivery['orders']>=500].nlargest(10,'late_pct').sort_values('late_pct')
bar_d_colors = [RED if v>10 else ORANGE if v>6 else GREEN for v in top10_states['late_pct']]
ax_d.barh(top10_states['customer_state'], top10_states['late_pct'], color=bar_d_colors, alpha=0.85)
ax_d.axvline(x=late_pct, color=DARK, linestyle='--', linewidth=1.2)
ax_d.set_title('Late Delivery % by State (Top Risk)', fontweight='bold', fontsize=10)
ax_d.set_xlabel('Late Delivery %')

ax_insights = fig.add_subplot(gs[3, :])
ax_insights.set_facecolor('#FFFFFF')
ax_insights.axis('off')

insights = [
    ('DELIVERY IS #1 DRIVER', RED,    'Late orders avg 2.26/5\nvs 4.28/5 for Early'),
    ('RJ HIGH RISK', ORANGE,          '12.1% late rate vs\n4.5% for SP'),
    ('96.9% ONE-TIME BUYERS', PURPLE, 'Only 3.1% return for\nrepeat purchases'),
    ('CREDIT CARD DOMINATES', BLUE,   '76.1% share, avg\nR$167 per order'),
    ('13.1% LOW REVIEWS', RED,        '12,655 orders rated\n1-2 stars'),
    ('OFFICE FURNITURE', ORANGE,      'Lowest avg score\n3.48 of 5'),
]
for i, (title, color, body) in enumerate(insights):
    x_pos = (i % 3) * 0.345 + 0.01
    y_pos = 0.53 if i < 3 else 0.02
    ax_insights.add_patch(plt.Rectangle((x_pos, y_pos), 0.32, 0.43,
                                         fill=True, facecolor=color, alpha=0.12,
                                         edgecolor=color, linewidth=2,
                                         transform=ax_insights.transAxes, clip_on=False))
    ax_insights.text(x_pos+0.16, y_pos+0.32, title, ha='center', va='center',
                     fontsize=9, fontweight='bold', color=color, transform=ax_insights.transAxes)
    ax_insights.text(x_pos+0.16, y_pos+0.14, body, ha='center', va='center',
                     fontsize=9, color=DARK, transform=ax_insights.transAxes)

plt.savefig(OUTDIR+'10_executive_dashboard.png', bbox_inches='tight', dpi=150)
plt.close()

print('\nAll 10 charts generated successfully!')
print(f'Saved to: {OUTDIR}')
