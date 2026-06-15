CREATE DATABASE IF NOT EXISTS ecommerce_dw;

USE ecommerce_dw;

CREATE TABLE Dim_Customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT UNIQUE,
    customer_name VARCHAR(100),
    customer_city VARCHAR(100),
    customer_state VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Dim_Product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT UNIQUE,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE Fact_Orders (
    order_key INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT UNIQUE,
    customer_id INT,
    product_id INT,
    quantity INT,
    amount DECIMAL(10,2),
    order_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);