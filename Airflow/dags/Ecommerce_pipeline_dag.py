from airflow.decorators import dag, task
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import pandas as pd


default_args = {
    "owner": "aayush",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}


@dag(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "kafka", "databricks", "mysql"]
)
def ecommerce_pipeline():

    @task
    def check_landing_zone():

        project_path = Path("/opt/project")

        if not project_path.exists():
            raise FileNotFoundError(
                f"Project folder not found: {project_path}"
            )

        print(f"Project folder verified: {project_path}")

        return str(project_path)

    @task
    def validate_exports(project_path):

        export_path = Path(project_path) / "Exports"

        required_files = [
            "dim_customer.csv",
            "dim_product.csv",
            "fact_orders.csv"
        ]

        for file in required_files:

            file_path = export_path / file

            if not file_path.exists():
                raise FileNotFoundError(
                    f"{file} not found at {file_path}"
                )

        print("All export files verified")

        return str(export_path)

    @task
    def validate_customer_file(export_path):

        file_path = Path(export_path) / "dim_customer.csv"

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(
                "dim_customer.csv is empty"
            )

        print(f"Customer rows found: {len(df)}")

        return len(df)

    @task
    def validate_product_file(export_path):

        file_path = Path(export_path) / "dim_product.csv"

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(
                "dim_product.csv is empty"
            )

        print(f"Product rows found: {len(df)}")

        return len(df)

    @task
    def validate_orders_file(export_path):

        file_path = Path(export_path) / "fact_orders.csv"

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(
                "fact_orders.csv is empty"
            )

        print(f"Order rows found: {len(df)}")

        return len(df)

    @task
    def validate_row_counts(
        customer_count,
        product_count,
        order_count
    ):

        print(f"Customers: {customer_count}")
        print(f"Products: {product_count}")
        print(f"Orders: {order_count}")

        if customer_count <= 0:
            raise ValueError(
                "Customer count validation failed"
            )

        if product_count <= 0:
            raise ValueError(
                "Product count validation failed"
            )

        if order_count <= 0:
            raise ValueError(
                "Order count validation failed"
            )

        print("Row count validation passed")

    @task
    def load_to_mysql():

        print("Starting Railway MySQL load...")

        result = subprocess.run(
            [
                "python",
                "/opt/project/Load_to_railway.py"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:

            print("ERROR OUTPUT:")
            print(result.stderr)

            raise Exception(
                "Railway MySQL load failed"
            )

        print("Railway MySQL load completed successfully")

    @task
    def pipeline_success():

        print("=" * 50)
        print("Ecommerce Pipeline Completed Successfully")
        print("=" * 50)

    project_path = check_landing_zone()

    export_path = validate_exports(
        project_path
    )

    customer_count = validate_customer_file(
        export_path
    )

    product_count = validate_product_file(
        export_path
    )

    order_count = validate_orders_file(
        export_path
    )

    validation = validate_row_counts(
        customer_count,
        product_count,
        order_count
    )

    mysql_load = load_to_mysql()

    success = pipeline_success()

    (
        export_path
        >> [
            customer_count,
            product_count,
            order_count
        ]
        >> validation
        >> mysql_load
        >> success
    )


ecommerce_pipeline()