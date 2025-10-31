# 💸 Financial Clustering Engine (FCE)

The Financial Clustering Engine (FCE) simulates a customer segmentation pipeline for a financial institution. It demonstrates how raw banking data can be transformed into structured, analytics-ready insights using modern data engineering and machine learning tools. The pipeline extracts raw CSV data, cleans and clusters customer records, and outputs labeled segments that can drive strategic business decisions across marketing, product design, and risk management.

---

## 📌 Project Overview

This project builds a complete data pipeline from scratch, covering:

- ✅ Extract raw customer data from CSV
- ✅ Clean and normalize data using Python
- ✅ Apply K-Means clustering to segment customers
- ✅ Visualize clusters and save labeled outputs
- ✅ Enable business insights for marketing, retention, and product strategy
- ✅ Scale pipeline execution to AWS for cloud-based processing

---

## ⚙️ Technologies Used

### Core Libraries

- **pandas** – Data manipulation and analysis  
- **NumPy** – Numerical operations  
- **scikit-learn** – Machine learning models, preprocessing, evaluation  
- **matplotlib/seaborn** – Data visualization  

### Infrastructure & Automation

- **GitHub Actions** – CI/CD pipeline automation  
- **Git & GitHub** – Version control and collaboration  
- **AWS EC2** – Scalable cloud execution of the pipeline  
- **CSV File System** – Raw and processed data storage  

---

## 🔄 Full ETL Workflow

### 🧼 Data Extraction & Cleaning

- Load raw banking data from `dataset/raw/inu_bank.csv`.
- Drop incomplete or invalid records.
- Normalize column formats (e.g., dates, income, balances).
- Prepare features for clustering (e.g., age, income, spending score).

### 🎫 Clustering & Labeling

- Used the Elbow Method to determine optimal number of clusters.
- Applied K-Means clustering to segment customers.
- Labeled each customer with a segment ID.
- Visualized clusters using scatter plots.

### 📁 Output Storage

- Save elbow plot and cluster visualization to `dataset/processed/`
- Export labeled customer data and segment summaries as CSVs.

---

## 💼 Business Impact with Cluster-Specific Examples

The Financial Clustering Engine segments customers into four distinct groups based on behavioral and financial attributes. These clusters enable targeted business strategies across marketing, product development, risk management, and executive planning.

---

### Cluster 0: Steady Customers

**Traits:**
- Moderate income and spending.
- Consistent account activity.
- Low loan exposure.

**Business Opportunities:**
- **Cross-sell savings products**: Offer fixed deposit accounts or retirement plans to deepen engagement.
- **Loyalty programs**: Reward consistency with tiered benefits or cashback incentives.
- **Upsell insurance**: These customers are financially stable and likely to consider add-on services like health or travel insurance.

**Example:** 
A customer with ₦4.5M annual income and regular monthly deposits may be offered a fixed deposit account with loyalty bonuses and optional health insurance.

---

### Cluster 1: Wealthy Inactives

**Traits:**
- High income  
- Low transaction frequency  
- Minimal product usage  

**Business Opportunities:**
- **Reactivation campaigns**: Personalized outreach to re-engage dormant high-value clients  
- **Premium services**: Offer wealth management, private banking, or investment advisory  
- **Digital nudges**: Use app notifications to highlight unused benefits or exclusive offers

**Example:**  
An executive earning ₦12M annually but showing low engagement could be invited to a private wealth seminar or assigned a dedicated relationship manager.

---

### Cluster 2: Most-Active Customers

**Traits:**
- High transaction volume.  
- Moderate to high spending.  
- Frequent use of digital channels.  

**Business Opportunities:**
- **Referral programs**: Leverage their engagement to attract similar customers.
- **Real-time offers**: Push contextual promotions based on spending behavior.
- **Early adopters**: Ideal segment to test new digital products or features.

**Example:** 
A fintech-savvy customer who transacts daily may be offered early access to a budgeting app and rewarded for referring peers.

---

### Cluster 3: Loan-Heavy Customers

**Traits:**
- High loan balances.  
- Lower income-to-debt ratio. 
- Irregular repayment patterns.

**Business Opportunities:**
- **Risk mitigation**: Monitor closely for default risk and offer restructuring plans.  
- **Financial literacy**: Provide budgeting tools or debt counseling.
- **Targeted upsell**: Offer secured credit products with lower risk profiles.  

**Example:**  
A 35-year-old customer with ₦2.8M income and multiple active loans could be offered a consolidated loan with a lower interest rate and personalized repayment plan.

---

## 🚀 CI/CD Pipeline

The project includes a GitHub Actions workflow that automates:

- Dependency installation.
- ETL script execution.
- Output generation and validation.  

This ensures reproducibility and scalability across environments. The pipeline has also been scaled to run on **AWS EC2**, enabling cloud-based execution for larger datasets and production-grade deployment.
 
