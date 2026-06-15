# Real-Time E-Commerce Data Engineering Pipeline - Execution Runbook

## Overview

This document explains how to start and execute the complete Real-Time E-Commerce Data Engineering Pipeline from a cold start (no containers running).

---

# Step 1: Navigate to Project Root

Open PowerShell and move to the project directory.

```powershell
cd D:\RealTime_Data_Engineering_Project
```

Verify project structure:

```powershell
dir
```

Expected folders and files:

```text
Airflow
Consumer
Databricks
Exports
Flask_api
Load_to_railway.py
docker-compose.yml
```

---

# Step 2: Start Kafka Ecosystem

The root Docker Compose file starts:

* Zookeeper
* Kafka
* MySQL

Run:

```powershell
docker compose up -d
```

Verify containers:

```powershell
docker ps
```

Expected containers:

```text
zookeeper
kafka
mysql
```

---

# Step 3: Verify Kafka Startup

Check Kafka logs:

```powershell
docker logs kafka --tail 20
```

Look for messages similar to:

```text
started
```

or

```text
Kafka Server started
```

---

# Step 4: Start Airflow

Navigate to the Airflow directory:

```powershell
cd Airflow
```

Start Airflow services:

```powershell
docker compose up -d
```

---

# Step 5: Verify Airflow Containers

Check container status:

```powershell
docker compose ps
```

Expected services:

```text
airflow-postgres-1
airflow-airflow-webserver-1
airflow-airflow-scheduler-1
```

All services should show:

```text
Up
```

---

# Step 6: Open Airflow UI

Open browser:

```text
http://localhost:8080
```

Login Credentials:

```text
Username: admin
Password: admin
```

---

# Step 7: Verify DAG Availability

Locate the DAG:

```text
ecommerce_pipeline
```

If visible:

✅ DAG loaded successfully

---

# Step 8: Start Flask Producer API

Open a new terminal.

Navigate to:

```powershell
cd D:\RealTime_Data_Engineering_Project\Flask_api
```

Install dependencies if required:

```powershell
pip install -r requirements.txt
```

Start Flask application:

```powershell
python app.py
```

Expected output:

```text
Running on http://127.0.0.1:5000
```

---

# Step 9:  Start Kafka Consumer

Open Terminal 2:

```powershell
cd Consumer

```powershell
python Consumer.py

Expected:

Listening to all topics...

Keep this terminal running.
---

# Step 10: Send Consumer, Product, Order data

Open PowerShell Terminal 3:

Invoke-RestMethod `
-Uri "http://127.0.0.1:5000/customer" `
-Method POST `
-ContentType "application/json" `
-Body '{
    "customer_id":"<sample_id>",
    "customer_name":"<sample_name>",
    "customer_city":"<sample_city>",
    "customer_state":"<sample_state>"
}'

Expected API response:

{
  "message": "Customer sent to Kafka successfully"
}

SAME PASS DATA FOR PRODUCT AND ORDER DATA
ALSO YOU CAN GENERATE DATA IN BULK LIKE THIS
[
  {
    "order_id":1001,
    "customer_id":101,
    "product_id":201,
    "quantity":2,
    "amount":110000
  },
  {
    "order_id":1002,
    "customer_id":102,
    "product_id":202,
    "quantity":3,
    "amount":3000
  },
  {
    "order_id":1003,
    "customer_id":103,
    "product_id":203,
    "quantity":1,
    "amount":2500
  }
]

---

# Step 11: Run Databricks ETL Notebooks

Execute notebooks in the following order:

```text
BRONZE_NOTEBOOK
        ↓
SILVER_NOTEBOOK
        ↓
GOLD_NOTEBOOK
```

Expected output:

```text
Exports/
├── dim_customer.csv
├── dim_product.csv
└── fact_orders.csv
```

---

# Step 12: Verify Export Files

Check generated files:

```powershell
dir D:\RealTime_Data_Engineering_Project\Exports
```

Expected:

```text
dim_customer.csv
dim_product.csv
fact_orders.csv
```

---

# Step 13: Trigger Airflow DAG

Open Airflow UI.

Select:

```text
ecommerce_pipeline
```

Click:

```text
Trigger DAG
```

Monitor execution flow:

```text
check_landing_zone
        ↓
validate_exports
        ↓
validate_customer_file
        ↓
validate_product_file
        ↓
validate_orders_file
        ↓
validate_row_counts
        ↓
load_to_mysql
        ↓
pipeline_success
```

Expected result:

✅ All tasks turn GREEN.

---

# Step 14: Verify Railway MySQL Load

Option 1:

Run manually:

```powershell
python Load_to_railway.py
```

Option 2:

Verify directly in Railway MySQL.

Run:

```sql
SELECT COUNT(*) FROM dim_customer;

SELECT COUNT(*) FROM dim_product;

SELECT COUNT(*) FROM fact_orders;
```

Expected result:

```text
Rows > 0
```

for all tables.

---

# Daily Startup Procedure

Once the project has been configured successfully, daily startup becomes:

## Start Infrastructure

```powershell
cd D:\RealTime_Data_Engineering_Project

docker compose up -d
```

## Start Airflow

```powershell
cd Airflow

docker compose up -d
```

## Run Components

1. Start Flask Producer
2. Start Kafka Consumer
3. Run Databricks Notebooks
4. Trigger Airflow DAG

---

# End-to-End Pipeline Flow

```text
Flask Producer
        ↓
Kafka Topics
        ↓
Kafka Consumer
        ↓
Landing Zone (JSON Files)
        ↓
Databricks Bronze Layer
        ↓
Databricks Silver Layer
        ↓
Databricks Gold Layer
        ↓
CSV Exports
        ↓
Apache Airflow
        ↓
Railway MySQL
```

---

# Success Criteria

The project is considered successful when:

✅ Kafka receives events

✅ Consumer stores JSON files

✅ Databricks generates export CSV files

✅ Airflow DAG completes successfully

✅ Railway MySQL tables contain data

✅ Pipeline Success task is GREEN
