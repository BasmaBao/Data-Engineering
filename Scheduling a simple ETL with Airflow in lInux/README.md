# Running a Simple ETL DAG with Airflow on Linux

This guide explains how to set up and run a simple ETL DAG using Apache Airflow on a Linux system. The DAG executes an ETL script that extracts data from a MySQL database, transforms it, and writes the transformed data to a CSV file. It is an application of the following youtube video: https://www.youtube.com/watch?v=RhNUbWynpwc

## Prerequisites

Before proceeding, ensure the following are installed and configured on your Linux machine:

1. **Apache Airflow** (tested with version 2.x):
   - Installation guide: [Airflow Official Documentation](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html).
2. **MySQL**:
   - MySQL server must be running locally.
   - A database named `etl_example` must exist with a table `data_try` containing sample data.
3. **Python 3.x** and the following Python libraries:
   - `pymysql`
   - `pandas`
4. **ETL Files** (provided in this repository):
   - `etl_script.py`
   - `wrapper_script.sh`
   - `MYSQL_DAG.py` (Airflow DAG file)

---

## Step-by-Step Instructions

### 1. Setup MySQL Database

Ensure MySQL is running, and a table exists with data for the ETL process:

1. Start MySQL service:

   ```bash
   sudo systemctl start mysql
   ```

2. Log into MySQL as the root user:

   ```bash
   mysql -u root -p
   ```

3. Create the database and table, and insert sample data:

   ```sql
   CREATE DATABASE etl_example;
   USE etl_example;

   CREATE TABLE data_try (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       age INT
   );

   INSERT INTO data_try (name, age) VALUES ('Alice', 25), ('Bob', 18), ('Charlie', 30);
   ```

---

### 2. Prepare the ETL Script

Place the provided `etl_script.py` file in a directory, for example:

```bash
mv etl_script.py /home/user/
```

This script will:
- Extract data from the `data_try` table in the MySQL database.
- Transform the data to include only rows where `age > 19`.
- Save the transformed data as a CSV file in `/home/user/test/extract/`.

---

### 3. Prepare the Wrapper Script

Save the following script as `wrapper_script.sh` in the same directory:

```bash
#!/bin/bash
python3 /home/user/etl_script.py
```

Make the script executable:

```bash
chmod +x /home/user/wrapper_script.sh
```

---

### 4. Configure the Airflow DAG

1. Copy the `MYSQL_DAG.py` file to the Airflow DAGs folder (usually located at `/home/airflow/airflow/dags/`):

   ```bash
   mv MYSQL_DAG.py /home/airflow/airflow/dags/
   ```

2. Ensure the `wrapper_script.sh` and `etl_script.py` paths in the DAG file are correct.

---

### 5. Start Airflow

1. Initialize the Airflow database (if not already done):

   ```bash
   airflow db init
   ```

2. Start the Airflow webserver and scheduler:

   ```bash
   airflow webserver --port 8080 &
   airflow scheduler &
   ```

3. Open the Airflow UI in your browser at `http://localhost:8080`.

---

### 6. Trigger the DAG

1. In the Airflow UI, activate the `MYSQL_DAG`.
2. Manually trigger the DAG or wait for it to execute as per the schedule (every 5 minutes).

---

## Output

The ETL process will:
1. Extract data from the MySQL database.
2. Filter rows where `age > 19`.
3. Write the filtered data to a timestamped CSV file in `/home/user/test/extract/`.

Example output file: `/home/user/test/extract/etl_output_20241205120000.csv`

---

## Troubleshooting

1. **MySQL Connection Issues**:
   - Verify the MySQL service is running: `sudo systemctl status mysql`.
   - Confirm the database credentials (`host`, `user`, `password`) in `etl_script.py` are correct.

2. **Permission Errors**:
   - Ensure the `wrapper_script.sh` has executable permissions: `chmod +x wrapper_script.sh`.
   - Verify write permissions for the output directory `/home/user/test/extract`.

3. **Airflow DAG Not Detected**:
   - Confirm the DAG file is in the correct folder (`/home/airflow/airflow/dags/`).
   - Restart the Airflow scheduler if needed.

4. **Python Module Errors**:
   - Install required Python libraries using `pip`:

     ```bash
     pip install pymysql pandas
     ```

---
