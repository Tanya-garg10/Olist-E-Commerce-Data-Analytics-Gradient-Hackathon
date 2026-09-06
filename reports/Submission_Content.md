# Hackathon Submission Content
## Gradient Learnings Data Analytics Hackathon
### Team Hackangers

---

## 📋 Submission Form Content

### Project Title
**Decoding Customer Experience on Brazil's Largest E-Commerce Marketplace**

### Team Name
Hackangers

### Problem Statement
Olist connects thousands of Brazilian sellers to customers through a unified marketplace. Despite strong growth, the platform faces unclear understanding of what drives poor customer experiences. This project analyzes 99,441 orders to identify the primary factors associated with 1-2 star reviews and deliver ranked, actionable business recommendations.

### Dataset Used
Brazilian E-Commerce Public Dataset by Olist (Kaggle)
- 9 relational tables, ~100,000 orders, 2016–2018
- Covers orders, payments, reviews, customers, products, sellers, and geography

### Business Objective
Analyze marketplace performance, delivery reliability, seller quality, product category satisfaction, and payment behavior to answer: *What is driving poor customer experience and where should Olist prioritize investment?*

### Key Approach
- Business Question → Data Preparation → Analysis → Visualization → Finding → Recommendation
- All results calculated directly from the dataset (no fabricated findings)
- Association clearly distinguished from causation throughout

### Top 5 Findings (Real Numbers)
1. Late orders average **2.26/5** vs **4.28/5** for early deliveries — a 2.02-point gap
2. **32.4% of 1-2 star orders involve late delivery** vs 2.9% of 4-5 star orders
3. Rio de Janeiro has a **12.1% late delivery rate** — nearly 3x São Paulo's 4.5%
4. **96.9% of customers never place a second order** — retention is near-zero
5. Office furniture averages just **3.48/5** — the lowest satisfaction category

### Top 3 Recommendations
1. Build a Late Delivery Early-Warning System (flag risk orders by Day 5, trigger escalation)
2. Implement Seller Accountability Scorecards with Performance Improvement Program thresholds
3. Launch post-delivery win-back email campaign for customers who rated 4-5 stars

### Tech Stack
Python 3.10, pandas, numpy, matplotlib, Google Colab, Git/GitHub

### Repository
https://github.com/YOUR_USERNAME/olist-data-analytics

### Suggested Repository Name
`olist-data-analytics`

---

## 🤖 AI Usage Disclosure

### Tools Used
- **Kiro (Claude-based AI assistant)** — used for notebook structure planning, code scaffolding, chart formatting templates, README and report drafting

### How AI Was Used
| Task | AI Involvement |
|------|---------------|
| Notebook section planning | AI suggested structure; team reviewed and approved |
| Code scaffolding | AI generated base code; team validated against actual data |
| Chart formatting | AI provided matplotlib templates; team customized |
| Report writing | AI drafted structure; team verified all numbers match actual calculations |
| Recommendations | AI suggested categories; team wrote based on real data findings |

### What AI Did NOT Do
- AI did not invent or hallucinate any numerical findings
- All statistics (review scores, late percentages, state comparisons, etc.) were calculated from the actual dataset in Python
- All business conclusions are based on real computed numbers, verified by the team

### Team's Own Contribution
- Data cleaning and preparation decisions
- Business interpretation of findings
- Recommendation prioritization and framing
- Verification of all computed numbers
- Final narrative and storytelling

---

## 📁 Deliverables Checklist

- [x] Google Colab notebook (16 sections, fully runnable)
- [x] Professional README.md
- [x] requirements.txt
- [x] .gitignore
- [x] Data directory with source instructions
- [x] Analysis report (Markdown, convertible to PDF)
- [x] 3-minute video script
- [x] Submission form content
- [x] AI usage disclosure
- [x] 10 saved visualization charts
- [x] Executive dashboard visualization

---

## 📊 Project Metrics Summary

| Metric | Value |
|--------|-------|
| Orders analyzed | 99,441 |
| Delivered orders | 96,478 |
| Total revenue analyzed | R$15,846,280 |
| Unique customers | 96,096 |
| Sellers | 3,095 |
| Product categories | 73 |
| Avg review score | 4.07 / 5 |
| Late delivery rate | 6.8% |
| Avg delivery time | 12.1 days |
| Repeat customer rate | 3.1% |
| Analysis sections | 16 |
| Visualizations | 10 charts |
| Recommendations | 8 ranked |
