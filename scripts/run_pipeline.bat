@echo off
cd C:\Users\luk\Financial_Clustering_Engine
call fceenv\Scripts\activate.bat
python scripts\fce_etl.py
aws s3 cp dataset\processed\cluster_plot.png s3://fce-pipeline-output/
aws s3 cp dataset\processed\elbow_plot.png s3://fce-pipeline-output/
aws s3 cp dataset\processed\labeled_customers.csv s3://fce-pipeline-output/
aws s3 cp dataset\processed\segment_summary.csv s3://fce-pipeline-output/