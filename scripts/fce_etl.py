import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
os.makedirs("dataset/processed", exist_ok=True)

# Step 1: Load and clean data
def load_and_clean_data(filepath):
    cleaned_df = pd.read_csv(filepath)

    cleaned_df.fillna({
        'Loan_ID': 'None',
        'Loan_Amount': 0.00,
        'Loan_Type': 'None',
        'Interest_Rate': 0.0
    }, inplace=True)

    cleaned_df['Start_Date'] = pd.to_datetime(cleaned_df['Start_Date'], errors='coerce')
    cleaned_df['End_Date'] = pd.to_datetime(cleaned_df['End_Date'], errors='coerce')

    cleaned_df['Transaction_Date'] = pd.to_datetime(cleaned_df['Transaction_Date']).dt.strftime('%d-%m-%Y %H:%M')
    cleaned_df['Opening_Date'] = pd.to_datetime(cleaned_df['Opening_Date']).dt.strftime('%d-%m-%Y %H:%M')
    cleaned_df['Start_Date'] = pd.to_datetime(cleaned_df['Start_Date']).dt.strftime('%d-%m-%Y %H:%M')
    cleaned_df['End_Date'] = pd.to_datetime(cleaned_df['End_Date']).dt.strftime('%d-%m-%Y %H:%M')

    cleaned_df[['First_Name', 'Last_Name']] = cleaned_df['Full_Name'].str.split(expand=True)
    cleaned_df.drop(columns=['Full_Name'], inplace=True)

    cleaned_df = cleaned_df[['Transaction_ID', 'Transaction_Type', 'Amount', 'Transaction_Date',
                             'Customer_ID', 'First_Name', 'Last_Name', 'Email', 'Phone', 'Account_ID', 'Account_Type',
                             'Balance', 'Opening_Date', 'Loan_ID', 'Loan_Amount', 'Loan_Type',
                             'Start_Date', 'End_Date', 'Interest_Rate']]

    return cleaned_df

# Step 2: Split into normalized tables
def split_into_tables(split_df):
    customer_df = split_df[['Customer_ID', 'First_Name', 'Last_Name', 'Email', 'Phone']].copy().drop_duplicates().reset_index(drop=True)
    account_df = split_df[['Account_ID', 'Account_Type', 'Balance', 'Opening_Date', 'Customer_ID']].copy().drop_duplicates().reset_index(drop=True)
    transaction_df = split_df[['Transaction_ID', 'Transaction_Type', 'Amount', 'Transaction_Date', 'Customer_ID']].copy().drop_duplicates().reset_index(drop=True)
    loan_df = split_df[['Loan_ID', 'Loan_Amount', 'Loan_Type', 'Start_Date', 'End_Date', 'Interest_Rate', 'Customer_ID']].copy().drop_duplicates().reset_index(drop=True)

    return customer_df, account_df, transaction_df, loan_df

# Step 3: Merge tables for unified view
def merge_tables(customer_df, account_df, transaction_df, loan_df):
    merged_df = customer_df \
        .merge(account_df, on='Customer_ID', how='left') \
        .merge(transaction_df, on='Customer_ID', how='left') \
        .merge(loan_df, on='Customer_ID', how='left')
    return merged_df

# Step 4: Build customer features
def build_customer_features(account_df, transaction_df, loan_df):
    grouped = account_df.groupby('Customer_ID')
    num_accounts = grouped.size()
    avg_balance = grouped['Balance'].mean()

    account_features = pd.DataFrame({
        'Customer_ID': num_accounts.index,
        'num_accounts': num_accounts.values,
        'avg_balance': avg_balance.values
    })

    grouped = transaction_df.groupby('Customer_ID')
    num_transactions = grouped.size()
    avg_transactions = grouped['Amount'].mean()

    transaction_features = pd.DataFrame({
        'Customer_ID': num_transactions.index,
        'num_transactions': num_transactions.values,
        'avg_transactions': avg_transactions.values
    })

    grouped = loan_df.groupby('Customer_ID')
    num_loans = grouped.size()
    avg_loans = grouped['Loan_Amount'].mean()

    loan_features = pd.DataFrame({
        'Customer_ID': num_loans.index,
        'num_loans': num_loans.values,
        'avg_loans': avg_loans.values
    })

    customer_features = account_features \
        .merge(transaction_features, on='Customer_ID', how='left') \
        .merge(loan_features, on='Customer_ID', how='left')

    return customer_features

# Step 5: Run clustering
def run_kmeans_clustering(customer_features, n_clusters=4):
    scaler = StandardScaler()
    X = customer_features.drop(columns=['Customer_ID'])
    X_scaled = scaler.fit_transform(X)

    scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    scaled_df['Customer_ID'] = customer_features['Customer_ID'].values

    inertia_scores = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertia_scores.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), inertia_scores, marker='o')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.savefig("dataset/processed/elbow_plot.png")
    plt.close()
    # plt.show()

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_scaled)
    scaled_df['Cluster'] = kmeans.labels_

    return scaled_df

# Step 6: Label and visualize segments
def label_and_plot_segments(scaled_df):
    cluster_names = {
        0: "Steady Customers",
        1: "Wealthy Inactives",
        2: "Most-Active Customers",
        3: "Loan-Heavy Customers"
    }

    scaled_df['Segment'] = scaled_df['Cluster'].map(cluster_names)
    segment_summary = scaled_df.groupby('Segment').mean()

    print("\nClustering complete. Segment summary:\n")
    print(segment_summary)

    plt.figure(figsize=(8, 6))
    for segment in scaled_df['Segment'].unique():
        segment_data = scaled_df[scaled_df['Segment'] == segment]
        plt.scatter(
            segment_data['num_transactions'],
            segment_data['avg_loans'],
            label=segment,
            alpha=0.6
        )

    plt.title('Customer Clusters: avg_loans vs num_transactions')
    plt.xlabel('Number of Transactions (scaled)')
    plt.ylabel('Average Loans (scaled)')
    plt.legend()
    plt.grid(True)
    plt.savefig("dataset/processed/cluster_plot.png")
    plt.close()
    # plt.show()

    return scaled_df, segment_summary

# Final pipeline
def main():
    cleaned_df = load_and_clean_data("dataset/raw/inu_bank.csv")
    customer_df, account_df, transaction_df, loan_df = split_into_tables(cleaned_df)
    merged_df = merge_tables(customer_df, account_df, transaction_df, loan_df)
    customer_features = build_customer_features(account_df, transaction_df, loan_df)
    scaled_df = run_kmeans_clustering(customer_features)
    labeled_df, segment_summary = label_and_plot_segments(scaled_df)

    return labeled_df, segment_summary

# Run the pipeline and capture results
if __name__ == "__main__":
    labeled_df, segment_summary = main()
    print("\nFinal Segment Summary:\n")
    print(segment_summary)


labeled_df.to_csv("dataset/processed/labeled_customers.csv", index=False)
segment_summary.to_csv("dataset/processed/segment_summary.csv")