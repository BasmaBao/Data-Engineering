from pyflink.table import TableEnvironment, EnvironmentSettings

# Create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Specify connector and format jars
t_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    "file:///home/user/Téléchargements/flink-sql-connector-kafka-3.4.0-1.20.jar;"
    "file:///home/user/Téléchargements/flink-sql-connector-elasticsearch7-3.0.1-1.17.jar"
)

# Define source table DDL
# Define source table DDL
source_ddl = """
    CREATE TABLE source_table (
	     Movie_ID BIGINT,
            Title VARCHAR(255),
            Release_Date VARCHAR(255),
            Genres ARRAY<VARCHAR(255)>,
            Vote_Average DECIMAL(3, 1),
            Vote_Count INT,
            Popularity DECIMAL(10, 2),
            Budget BIGINT,
            Revenue BIGINT,
            Production_Companies ARRAY<VARCHAR(255)> -- Change to this format without spaces

    ) WITH (
        'connector' = 'kafka',
        'topic' = 'tmdb_movies',
        'properties.bootstrap.servers' = 'localhost:9092',
        'properties.group.id' = 'test_1',
        'scan.startup.mode' = 'latest-offset',
        'format' = 'json'
    )
"""

# Define sink table DDL
sink_ddl = """
    CREATE TABLE sink_table(
            Movie_ID BIGINT,
            Title VARCHAR(255),
            Release_Date VARCHAR(255),
            Genres ARRAY<VARCHAR(255)>,
            Vote_Average DECIMAL(3, 1),
            Vote_Count INT,
            Popularity DECIMAL(10, 2),
            Budget BIGINT,
            Revenue BIGINT,
            Production_Companies ARRAY<VARCHAR(255)> -- Change to this format without spaces
    ) WITH (        
        'connector' = 'elasticsearch-7',
        'index' = 'my_movie_data_406',
        'hosts' = 'http://localhost:9200',
        'format' = 'json'
    )
"""
# Execute DDL statements to create tables
t_env.execute_sql(source_ddl)
t_env.execute_sql(sink_ddl)

# Retrieve the source table
source_table = t_env.from_path('source_table')

print("Source Table Schema:")
source_table.print_schema()

# Process the data
result_table = t_env.sql_query("SELECT *  FROM source_table")

# Retrieve the sink table
sink_table = t_env.from_path('sink_table')

print("Sink Table Schema:")
sink_table.print_schema()

# Insert the processed data into the sink table
result_table.execute_insert('sink_table').wait()
