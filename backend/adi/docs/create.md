# Database and Table Creation for Banking System

This code snippet demonstrates the creation and initialization of a simple banking system database. Below is a breakdown of each part of the code.

## 1. Drop Existing Database
```sql
DROP bank;
```
- This command attempts to drop (delete) the database named `bank`. If it exists, all data and structures within the database will be removed.

## 2. Create Database
```sql
CREATE DATABASE bank;
```
- This command creates a new database named `bank`.

## 3. Use Database
```sql
USE bank;
```
- This command sets the context to the `bank` database, allowing subsequent commands to operate within this database.

## 4. Create Users Table
```sql
CREATE TABLE users(
    accno int PRIMARY KEY,
    name char(20) NOT NULL,
    passwd varchar(30),
    balance float DEFAULT 0,
    branch char(3) DEFAULT "PAT",
);
```
- This command creates a table named `users` with the following columns:
  - `accno`: An integer that serves as the primary key (unique identifier for each user).
  - `name`: A fixed-length character field (20 characters) that cannot be null.
  - `passwd`: A variable-length character field (up to 30 characters) for storing user passwords.
  - `balance`: A floating-point number representing the user's account balance, defaulting to 0.
  - `branch`: A fixed-length character field (3 characters) with a default value of "PAT".

> **Note**: There is a syntax error due to a trailing comma after the last column definition. This should be removed for the code to execute correctly. 

## 5. Insert Records into Users Table
```sql
INSERT INTO
    users (accno, name, passwd)
VALUES
    (1, "Aditya Nandan", "1234"),
    (2, "Rohit Sharma", "sharma"),
    (3, "Ayush", "ay#123");
```
- This command inserts three records into the `users` table:
  - User 1: Account number 1, Name "Aditya Nandan", Password "1234"
  - User 2: Account number 2, Name "Rohit Sharma", Password "sharma"
  - User 3: Account number 3, Name "Ayush", Password "ay#123"

## 6. Select All Records from Users Table
```sql
SELECT
    *
FROM
    users;
```
- This command retrieves and displays all records from the `users` table.

## Summary
This code initializes a banking database by dropping any existing database named `bank`, creating a new database, and defining a `users` table with fields for account number, name, password, balance, and branch. It inserts three users into the `users` table and retrieves all user records. Note that there is a syntax error in the table creation statement that needs to be corrected for successful execution.