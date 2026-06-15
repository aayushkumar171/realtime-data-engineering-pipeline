# Real-Time Ecommerce Data Engineering Pipeline

## Overview

This project demonstrates a complete end-to-end Data Engineering pipeline built using modern data engineering tools and practices.

The pipeline simulates ecommerce transactions, processes them using Databricks and PySpark, orchestrates workflow execution with Apache Airflow, and loads curated data into a MySQL data warehouse hosted on Railway.

---

## Tech Stack

### Data Generation

* Python
* Faker

### Messaging Layer

* Apache Kafka
* Zookeeper

### Data Processing

* Databricks Community Edition
* PySpark

### Workflow Orchestration

* Apache Airflow

### Storage

* MySQL
* Railway MySQL

### Containerization

* Docker
* Docker Compose

---

## Architecture

```text
Ecommerce Data Generator
            │
            ▼
      Kafka Producer
            │
            ▼
       Kafka Topic
            │
            ▼
       Databricks
      (PySpark ETL)
            │
            ▼
       CSV Exports
            │
            ▼
       Apache Airflow
            │
            ▼
    Data Validation Layer
            │
            ▼
      Railway MySQL
```

---

## Workflow

### Step 1 – Generate Transactions

Python scripts generate ecommerce transaction data and publish records to Kafka.

---

### Step 2 – Consume Kafka Data

Databricks consumes Kafka events and stores them in Spark DataFrames.

---

### Step 3 – Transformation Layer

PySpark performs:

* Data Cleaning
* Fact Table Creation
* Dimension Table Creation
* Data Quality Checks

Generated tables:

* dim_customer
* dim_product
* fact_orders

---

### Step 4 – Export Layer

Databricks exports transformed datasets:

* Exports/dim_customer.csv
* Exports/dim_product.csv
* Exports/fact_orders.csv

---

### Step 5 – Airflow Orchestration

Airflow executes the pipeline:

1. Check project availability
2. Validate export files
3. Validate row counts
4. Execute Railway load process
5. Mark pipeline success

---

### Step 6 – Warehouse Load

The loader script:

* Creates tables if needed
* Clears existing data
* Loads fresh data
* Commits transaction

---

## Airflow DAG

Tasks:

```text
check_landing_zone
        │
        ▼
validate_exports
        │
        ▼
 ┌─────────────────────┐
 │ validate_customer   │
 │ validate_product    │
 │ validate_orders     │
 └─────────────────────┘
        │
        ▼
validate_row_counts
        │
        ▼
load_to_mysql
        │
        ▼
pipeline_success
```

---

## Data Quality Checks

Implemented validations:

* Export file existence
* Empty file detection
* Row count validation
* Load failure detection

---

## Key Features

* End-to-End Pipeline
* Real-Time Kafka Integration
* PySpark Transformations
* Airflow Orchestration
* Dockerized Infrastructure
* Railway Cloud Warehouse
* Data Validation Layer
* Idempotent Loading

---

## Future Enhancements

* Airflow-triggered Databricks execution
* Airflow Connections and Variables
* Incremental loading
* Power BI dashboard
* CI/CD with GitHub Actions
* Monitoring and alerting

---

## Author

Aayush Kumar
Data Engineering Project
