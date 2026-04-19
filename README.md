# 🛒 Retail Product Sales Analytics & AI Dashboard

## 📌 Overview
This project presents a comprehensive **data science and business intelligence solution** for analyzing retail sales data across the United States (2023–2024).

It combines:
- Exploratory Data Analysis (EDA)
- Machine Learning Models
- Time-Series Forecasting
- Interactive Dashboard (Streamlit)
- AI-powered Chat Assistant (Ollama LLM)

The goal is to extract **actionable insights** for revenue growth, customer behavior, and business strategy.

---

## 🎯 Objectives
- Clean and preprocess large-scale retail data (200,000 transactions)
- Perform multi-dimensional EDA (category, region, time, distribution)
- Build predictive models (Regression, Clustering, Forecasting)
- Develop an interactive dashboard for decision-making
- Integrate AI assistant for real-time data insights

---

## 📊 Dataset Information
- **Records:** 200,000 transactions  
- **Time Period:** Jan 2023 – Dec 2024  
- **Regions:** East, West, Centre, South  
- **Categories:** Electronics, Home & Furniture, Clothing & Apparel, Accessories  
- **Sub-Categories:** 19  
- **Products:** 49  

### Key Metrics:
- 💰 Total Revenue: **$142.4M**
- 📈 Total Profit: **$31.5M**
- 🎯 Avg Profit Margin: **25.77%**

---

## 🧰 Tech Stack

### 💻 Programming & Libraries
- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Plotly
- Scikit-learn
- Statsmodels

### 🌐 Dashboard & AI
- Streamlit  
- Ollama (Local LLM - Gemma)

### 📦 Other Tools
- Squarify (Treemap)
- ydata-profiling

---

## 🔍 Project Workflow

### 1️⃣ Data Cleaning & Preprocessing
- Handled missing values (none found)
- Removed duplicates
- Converted date formats
- Feature engineering:
  - Year, Month, Quarter
  - Profit Margin
  - Day of Week

---

### 2️⃣ Exploratory Data Analysis (EDA)
- Category & Sub-category analysis
- Regional performance
- Seasonal trends
- Distribution analysis
- Correlation analysis

---

### 3️⃣ Machine Learning Models

#### 📈 Multiple Linear Regression
- Predicts revenue using:
  - Unit Price
  - Quantity
- **R² Score:** 0.83 (Strong model)

#### 🔵 K-Means Clustering
- Segments products into 4 clusters:
  - High-margin products
  - Premium products
  - Mid-tier electronics
  - Balanced performers

#### ⏳ Time-Series Forecasting (ARIMA)
- Forecasts future revenue trends
- Identifies seasonal spikes (Q4 peak)

---

## 📊 Dashboard Features

The Streamlit dashboard includes:

### ✅ KPI Metrics
- Total Revenue
- Total Profit
- Orders
- Profit Margin
- Units Sold

### 📦 Category Analysis
- Revenue breakdown
- Sub-category insights
- Treemap visualization

### 🌍 Regional Analysis
- Revenue by region
- Profit contribution
- Order distribution

### 📈 Time-Series Analysis
- Daily & monthly trends
- Year-over-year comparison
- Seasonal patterns

### 🏆 Product Rankings
- Top products by revenue & profit

### 📊 Distributions
- Revenue distribution
- Profit distribution

### 🔗 Correlation Analysis
- Revenue vs Profit
- Price vs Margin relationships

---

## 🤖 AI Chat Assistant

Integrated AI assistant using **Ollama (Gemma:2b model)**:

### Features:
- Answers dataset-related queries
- Generates insights instantly
- Can create charts dynamically
- Works locally (no API cost)

Example queries:
- "Which category generates highest profit?"
- "Show revenue by region"
- "What is the best performing product?"

---
