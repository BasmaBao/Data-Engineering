import pymysql
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # Connect to MySQL server (default or existing database not required for CREATE DATABASE)
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root'
    }
    conn = pymysql.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()
    
    # Create sparkifydb with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb;")
    cur.execute("CREATE DATABASE sparkifydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    
    # Close connection to the MySQL server
    conn.close()
    
    # Connect to the newly created sparkifydb
    mysql_config['database'] = 'sparkifydb'
    conn = pymysql.connect(**mysql_config)
    cur = conn.cursor()
    
    return cur, conn

def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
