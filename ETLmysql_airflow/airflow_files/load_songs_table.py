import os
import glob
import pymysql
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """
    - Load data from a song file to the song and artist data tables
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notnull(df), None)  # Replace NaN with None

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    song_data = [None if pd.isna(val) else val for val in song_data]  # Handle NaN values
    cur.execute(song_table_insert, song_data)

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

    process_data(cur, conn, filepath='/home/user/2024/ETLmysql/data/song_data', func=process_song_file)

    conn.close()


if __name__ == "__main__":
    main()


