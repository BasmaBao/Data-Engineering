from pyflink.table import TableEnvironment, EnvironmentSettings

# Create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Specify connector and format jars
t_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    "file:///home/user/Téléchargements/flink-sql-connector-kafka-3.4.0-1.20.jar"
)

# Define source table DDL
source_ddl = """
    CREATE TABLE source_table_movie (
	  
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
        'properties.bootstrap.servers' = 'PNS-VirtualBox:9092',
        'properties.group.id' = 'test',
        'scan.startup.mode' = 'latest-offset',
        'format' = 'json'
    )
"""

# Execute DDL statement to create the source table
t_env.execute_sql(source_ddl)

# Retrieve the source table
source_table = t_env.from_path('source_table_movie')

print("Source Table Schema:")
source_table.print_schema()

# Define a SQL query to select all columns from the source table
sql_query = "SELECT * FROM source_table_movie"

# Execute the query and retrieve the result table
result_table = t_env.sql_query(sql_query)

# Print the result table to the console
result_table.execute().print()
