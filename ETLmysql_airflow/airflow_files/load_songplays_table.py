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


    # insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'],
                         row['location'], row['userAgent'])
        songplay_data = [None if pd.isna(val) else val for val in songplay_data]  # Handle NaN values
        cur.execute(songplay_table_insert, songplay_data)


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
    print("connected successfully!")

    process_data(cur, conn, filepath='/home/user/2024/ETLmysql/data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
