import os
import glob
import pymysql
import pandas as pd
from sql_queries import *

def process_log_file(cur, filepath):
    """
    - Load data from a log file to the time, user and songplay data tables
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notnull(df), None)  # Replace NaN with None

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])

    # insert time data records
    time_data = [(tt.value, tt.hour, tt.day, tt.week, tt.month, tt.year, tt.weekday()) for tt in t]
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(data=time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

def process_data(cur, conn, filepath, func):
    """
    - Iterate over all files and populate data tables in sparkifydb
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it.
    
    - Runs ETL pipelines
    """
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'sparkifydb'
    }
    conn = pymysql.connect(**mysql_config, autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='/home/user/2024/ETLmysql/data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
