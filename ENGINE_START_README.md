# Project Runbook

## Prerequisites

Install:

* Docker Desktop
* Databricks Community Edition
* Python 3.12+
* Git

---

# Step 1: Start Kafka Infrastructure

Move to project root:

```bash
cd D:\RealTime_Data_Engineering_Project
```

Start Kafka stack:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Expected:

```text
zookeeper
kafka
mysql
```

---

# Step 2: Generate Streaming Data

Run producer:

```bash
python Producer.py
```

Expected:

```text
Message sent successfully
```

---

# Step 3: Run Databricks Pipeline

Open Databricks notebook.

Execute notebook cells in order.

Pipeline performs:

* Kafka Read
* Bronze Layer
* Silver Layer
* Gold Layer
* CSV Export

Expected exports:

```text
Exports/
├── dim_customer.csv
├── dim_product.csv
└── fact_orders.csv
```

Verify:

```bash
dir Exports
```

---

# Step 4: Start Airflow

Move to Airflow directory:

```bash
cd Airflow
```

Start services:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Expected:

```text
airflow-postgres-1
airflow-airflow-scheduler-1
airflow-airflow-webserver-1
```

---

# Step 5: Open Airflow UI

Open browser:

```text
http://localhost:8080
```

Login:

```text
Username: admin
Password: admin
```

---

# Step 6: Trigger DAG

Open DAG:

```text
ecommerce_pipeline
```

Trigger:

```text
Trigger DAG
```

Expected flow:

```text
check_landing_zone
validate_exports
validate_customer_file
validate_product_file
validate_orders_file
validate_row_counts
load_to_mysql
pipeline_success
```

All tasks should turn green.

---

# Step 7: Verify Railway Load

Run:

```bash
python Load_to_railway.py
```

or verify directly in Railway.

Queries:

```sql
SELECT COUNT(*) FROM dim_customer;

SELECT COUNT(*) FROM dim_product;

SELECT COUNT(*) FROM fact_orders;
```

Expected:

```text
Row counts match exported CSV files
```

---

# Troubleshooting

## Export File Missing

Verify:

```bash
dir Exports
```

Required:

```text
dim_customer.csv
dim_product.csv
fact_orders.csv
```

---

## Airflow Not Starting

Check:

```bash
docker logs airflow-airflow-webserver-1
```

---

## Scheduler Issues

Check:

```bash
docker logs airflow-airflow-scheduler-1
```

---

## Railway Connection Failure

Verify:

```bash
python Load_to_railway.py
```

Check:

* Host
* Port
* Username
* Password

---

# Shutdown Project

Stop Airflow:

```bash
cd Airflow

docker compose down
```

Stop Kafka Infrastructure:

```bash
cd ..

docker compose down
```

---

# Restart Project

Kafka:

```bash
docker compose up -d
```

Airflow:

```bash
cd Airflow

docker compose up -d
```

---

# Successful Run Checklist

* Kafka running
* MySQL running
* Databricks notebook completed
* Export files generated
* Airflow running
* DAG successful
* Railway tables populated

Pipeline Status: Production Ready
