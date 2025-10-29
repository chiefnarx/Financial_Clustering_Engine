from fce_etl.py import build_customer_features, run_clustering

def test_feature_output():
    # Create minimal dummy data
    account_df = ...
    transaction_df = ...
    loan_df = ...

    features = build_customer_features(account_df, transaction_df, loan_df)
    assert 'num_accounts' in features.columns
    assert 'avg_balance' in features.columns
    assert 'Customer_ID' in features.columns

def test_clustering_labels():
    # Use dummy features
    dummy_features = ...
    clustered = run_clustering(dummy_features, n_clusters=4)
    assert 'Cluster' in clustered.columns
    assert 'Segment' in clustered.columns
    assert clustered['Cluster'].nunique() == 4