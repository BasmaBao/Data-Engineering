# CREATE TABLES

user_table_create = ("""
CREATE TABLE users
(user_id int  PRIMARY KEY, 
 first_name varchar(255),
 last_name varchar(255),
 gender varchar(255),
 level varchar(255));
""")

song_table_create = ("""
CREATE TABLE songs
(song_id varchar(255) PRIMARY KEY, 
 title varchar(255),
 artist_id varchar(255),
 year int NULL,
 duration float);
""")

artist_table_create = ("""
CREATE TABLE artists
(artist_id varchar(255) PRIMARY KEY, 
 name varchar(255),
 location varchar(255),
 latitude float,
 longitude float);
""")

time_table_create = ("""
CREATE TABLE time
(start_time bigint PRIMARY KEY, 
 hour int NULL,
 day int NULL,
 week int NULL,
 month int NULL,
 year int NULL,
 weekday int NULL);
""")

songplay_table_create = ("""
CREATE TABLE songplays
(songplay_id int  PRIMARY KEY, 
 level varchar(255), 
 session_id int NULL, 
 location varchar(255), 
 user_agent varchar(255),
 song_id VARCHAR(255), 
 artist_id VARCHAR(255), 
 start_time BIGINT, 
 user_id INT, 
 FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE RESTRICT, 
 FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE RESTRICT, 
 FOREIGN KEY (start_time) REFERENCES time(start_time) ON DELETE RESTRICT, 
 FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT);
""")

# DROP TABLES

user_drop_table = "DROP TABLE IF EXISTS  users;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_drop_table, song_table_drop, artist_table_drop, time_table_drop]

#Insert queries
songplay_table_insert= ("""INSERT IGNORE INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, 
                              session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

song_table_insert = ("""
INSERT IGNORE INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s);
""")

artist_table_insert = ("""
INSERT IGNORE INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s);
""")


time_table_insert = ("""
INSERT IGNORE INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
level = VALUES(level);
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, artists.artist_id FROM songs
JOIN artists ON songs.artist_id=artists.artist_id
WHERE songs.title=%s AND artists.name=%s AND songs.duration=%s; 
""") 


