<div align="center">

# 🛒 Retail Product Sales Analytics & AI Dashboard

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Ollama-LLM-black?style=for-the-badge&logo=ollama&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>

<br/>

> **A full-stack data science solution** — EDA · Machine Learning · Forecasting · Interactive Dashboard · AI Chat Assistant

<br/>

| 💰 Total Revenue | 📈 Total Profit | 🎯 Avg Profit Margin | 📦 Transactions |
|:-:|:-:|:-:|:-:|
| **$142.4M** | **$31.5M** | **25.77%** | **200,000** |

</div>

---

## 📌 Overview

This project is a **comprehensive retail analytics platform** that combines modern data science techniques with business intelligence tooling to deliver actionable insights from 200,000 US retail transactions spanning 2023–2024.

It is built end-to-end — from raw data cleaning to a live AI-powered dashboard — making it suitable as both a **production-ready BI tool** and a **data science portfolio project**.

```
Raw CSV  →  Preprocessing  →  EDA  →  ML Models  →  Streamlit Dashboard  →  AI Chat
```

---

## 🎯 Objectives

| # | Goal |
|---|------|
| 1 | Clean and preprocess 200K+ retail transactions |
| 2 | Perform multi-dimensional EDA (category, region, time, distribution) |
| 3 | Build regression, clustering, and forecasting models |
| 4 | Develop an interactive dashboard for business decision-making |
| 5 | Integrate a local AI assistant for real-time data queries |

---

## 📊 Dataset

| Attribute | Details |
|-----------|---------|
| **Records** | 200,000 transactions |
| **Time Period** | Jan 2023 – Dec 2024 |
| **Regions** | East · West · Centre · South |
| **Categories** | Electronics · Home & Furniture · Clothing & Apparel · Accessories |
| **Sub-Categories** | 19 |
| **Unique Products** | 49 |

---

## 🧰 Tech Stack

<table>
<tr>
<td valign="top" width="33%">

### 🐍 Core Python
- `Python 3.10+`
- `Pandas` · `NumPy`
- `Matplotlib` · `Seaborn`
- `Plotly`
- `Scikit-learn`
- `Statsmodels`

</td>
<td valign="top" width="33%">

### 🌐 Dashboard & AI
- `Streamlit` — Interactive UI
- `Ollama` — Local LLM (Gemma:2b)
- `Plotly` — Interactive charts
- `Squarify` — Treemap

</td>
<td valign="top" width="33%">

### 📦 Analytics
- `ydata-profiling` — Auto EDA
- `ARIMA` — Time-series
- `K-Means` — Clustering
- `Linear Regression` — Forecasting

</td>
</tr>
</table>

---

## 🔍 Project Workflow

### 1️⃣ Data Cleaning & Preprocessing

- ✅ Verified zero missing values
- ✅ Removed duplicate records
- ✅ Standardised date formats
- ✅ Engineered features:
  - `Year` · `Month` · `Quarter` · `Day of Week`
  - `Profit Margin` = `(Profit / Revenue) × 100`

---

### 2️⃣ Exploratory Data Analysis (EDA)

Explored data across **5 analytical dimensions**:

| Dimension | What Was Analyzed |
|-----------|------------------|
| 📦 Category & Sub-category | Revenue and profit contribution per product group |
| 🌍 Regional | Performance across East, West, Centre, South |
| 📅 Seasonal | Monthly and quarterly trends, Q4 holiday spikes |
| 📉 Distribution | Revenue & profit spread using histograms and box plots |
| 🔗 Correlation | Revenue vs Profit, Unit Price vs Margin |

---

### 3️⃣ Machine Learning Models

#### 📈 Multiple Linear Regression — Revenue Prediction

Predicts revenue from unit price and quantity sold.

```
Features:  Unit Price  +  Quantity Sold
Target:    Revenue
R² Score:  0.83  ✅ (Strong predictive power)
```

---

#### 🔵 K-Means Clustering — Product Segmentation

Products clustered into **4 strategic segments**:

| Cluster | Segment Label | Characteristics |
|---------|--------------|-----------------|
| 0 | 🟢 High-Margin Products | Low volume, high profit % |
| 1 | 🔵 Premium Products | High price point, selective demand |
| 2 | 🟡 Mid-Tier Electronics | Moderate price & margin |
| 3 | 🟠 Balanced Performers | Stable revenue, consistent margin |

---

#### ⏳ Time-Series Forecasting — ARIMA

- Trains on 24 months of historical revenue data
- Forecasts future revenue trends
- Detects **Q4 seasonal spikes** (holiday demand)

---

## 📊 Dashboard Features

The **Streamlit dashboard** provides a fully interactive BI experience:

<details>
<summary><strong>📌 KPI Metrics Panel</strong></summary>

> Total Revenue · Total Profit · Total Orders · Profit Margin · Units Sold

</details>

<details>
<summary><strong>📦 Category Analysis</strong></summary>

> Revenue breakdown by category · Sub-category performance · Treemap visualization

</details>

<details>
<summary><strong>🌍 Regional Analysis</strong></summary>

> Revenue by region · Profit contribution per region · Order distribution map

</details>

<details>
<summary><strong>📈 Time-Series Analysis</strong></summary>

> Daily & monthly revenue trends · Year-over-year comparison · Seasonal pattern overlays

</details>

<details>
<summary><strong>🏆 Product Rankings</strong></summary>

> Top products ranked by revenue and profit · Underperforming SKU identification

</details>

<details>
<summary><strong>📊 Distribution & Correlation</strong></summary>

> Revenue distribution · Profit spread · Revenue vs Profit scatter · Price vs Margin analysis

</details>

---

## 🤖 AI Chat Assistant

An embedded **local AI assistant** powered by [Ollama](https://ollama.com/) (Qwen2.5 model) — **no API keys, no cost, fully private**.

### Capabilities

- 💬 Answers natural language questions about the dataset
- 📊 Generates charts dynamically on request
- 💡 Surfaces instant business insights

### Example Queries

```text
"Which category generates the highest profit margin?"
"Show me revenue breakdown by region."
"What is the best-performing product in Q4 2024?"
"Compare year-over-year growth for Electronics."
```

---

## 🚀 Getting Started

### Prerequisites

```bash
python >= 3.10
ollama  # install from https://ollama.com
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/retail-sales-analytics.git
cd retail-sales-analytics

# 2. Install dependencies
pip install -r requirements.txt.txt

# 3. Pull the Ollama model
ollama pull Qwen2.5

# 4. Launch the dashboard
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
retail-sales-analytics/
│
├── 📓 Product_Sales_Analysis.ipynb      # Full EDA + ML notebook
├── 🖥️  dashboard.py                     # Streamlit dashboard app
├── 🗜️  product_sales_dataset_final.zip  # Dataset (200K transactions, zipped)
├── 📄 requirements.txt.txt              # Python dependencies
└── 📖 README.md
```

---

## 📬 Contact

Have feedback or want to collaborate? Feel free to open an issue or reach out!

<div align="center">

⭐ **If you found this useful, give the repo a star!** ⭐

</div>
