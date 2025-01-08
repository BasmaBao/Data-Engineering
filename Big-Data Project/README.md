# Real-Time Data Pipeline with Kafka, Flink, Elasticsearch, and TMDB API

### Overview:
This project sets up a real-time data streaming pipeline designed to process, store, and visualize movie-related data. The system utilizes a combination of powerful tools:
- **Kafka** for handling real-time, data streams.
- **Flink** for performing data processing in real-time, enabling insights and analytics.
- **Elasticsearch** for indexing and querying large volumes of data efficiently.
- **Kibana** for visualizing the processed data through intuitive dashboards.
- **TMDB API** to fetch movie-related data like movie details, ratings, and reviews.

The goal is to create an efficient pipeline that ingests real-time movie data, processes it, and displays visual analytics using Elasticsearch and Kibana. You can customize and extend this setup with additional tools, but ensure compatibility among all the components.

![schema](imgs/schema.png)

This guide outlines the steps to implement and work with this pipeline, including the integration of the **TMDB API** for retrieving movie data. Feel free to modify or extend this setup to fit your project requirements, but be sure to ensure compatibility across tools and technologies. 

---

Let me know if you need further adjustments!

## Project Part 1

### **`TMDB`** API

- **How to Get Your TMDB API Key:**

    To access data from the TMDB (The Movie Database) API, you need an API key. Here’s how you can get one:

    1. **Sign Up for an Account**: Go to the [TMDB website](https://www.themoviedb.org/) and create an account.
    2. **Generate an API Key**: Once logged in, go to the **API** section under your account settings:  
       [TMDB API Section](https://www.themoviedb.org/settings/api)
    3. **Create a New API Key**: Follow the instructions to create an API key. Once created, you'll receive a unique API key that you can use to make requests to the TMDB API.

    ```bash
    "YOUR_TMDB_API_KEY"
    ```

    Replace `"YOUR_TMDB_API_KEY"` with the key you obtained from TMDB.

- **API Request Example**:  
    Once you have the API key, you can make requests to fetch data. For instance, to get details of a specific movie, you can use the following request:

    ```bash
    curl -X GET "https://api.themoviedb.org/3/movie/550?api_key=YOUR_TMDB_API_KEY"
    ```

    Replace `"550"` with the desired movie ID (e.g., ID for "Fight Club").

- **Kafka Info**:
    - **Start Zookeeper**:  
    Kafka uses Zookeeper for distributed coordination. Start Zookeeper by running the following command from the Kafka directory:

        ```bash
        bin/zookeeper-server-start.sh config/zookeeper.properties
        ```
        
    - **Start Kafka Server**:  
    Open a new terminal and start the Kafka server with the following command:

        ```bash
        bin/kafka-server-start.sh config/server.properties
        ```

    - **Create a Topic**:  
    To create a Kafka topic named "tmdb_movies", run the following command:

        ```bash
        bin/kafka-topics.sh --create --topic tmdb_movies --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
        ```

    - **List Topics**:  
    To list all existing topics, run:

        ```bash
        bin/kafka-topics.sh --list --bootstrap-server localhost:9092
        ```

    - **Produce Messages**:  
    Use the following command to produce messages to the "**tmdb_movies**" topic:

        ```bash
        bin/kafka-console-producer.sh --topic tmdb_movies --bootstrap-server localhost:9092
        ```

    - **Consume Messages**:  
    Open a new terminal and run the following command to consume messages from the "tmdb_movies" topic:

        ```bash
        bin/kafka-console-consumer.sh --topic tmdb_movies --bootstrap-server localhost:9092 --from-beginning
        ```

- **Server Properties**:
    - **Default Configuration**:

        ```python
        # Listener name, hostname, and port the broker will advertise to clients.
        # If not set, it uses the value for "listeners".
        advertised.listeners=PLAINTEXT://your.host.name:9092
        ```

- ***My Kafka Info***:  
    After starting Zookeeper & Kafka, run the following commands:

        ```bash
        bin/zookeeper-server-start.sh config/zookeeper.properties
        bin/kafka-server-start.sh config/server.properties
        ```

    You should see the following output in the Kafka terminal:

        ```bash
        [2023-12-03 17:11:15,535] INFO Registered broker 0 at path /brokers/ids/0 with addresses: PLAINTEXT://PNS-VirtualBox:9092, czxid (broker epoch): 124 (kafka.zk.KafkaZkClient)
        
        default topic: 'tmdb_movies'
        bootstrap-server: 'PNS-VirtualBox:9092'
        ```

  - Read API data
    
    ```python
import json
import requests
from kafka import KafkaProducer
from rich import print
from time import sleep

# TMDb API Key
API_KEY = "YOUR_KEY"
BASE_URL = "https://api.themoviedb.org/3"

    
  # Fetch Popular Movies
def fetch_popular_movies(page=1):
    """
    Fetches popular movies from TMDb.
    """
    endpoint = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error fetching popular movies. Status code: {response.status_code}")
        return []

# Fetch Detailed Movie Data
def fetch_movie_details(movie_id):
    """
    Fetches detailed data for a single movie.
    """
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for Movie ID {movie_id}. Status code: {response.status_code}")
        return {}

# Process Movie Data and Send to Kafka
def process_and_send_movies():
    """
    Processes movie data and sends to Kafka.
    """
    popular_movies = fetch_popular_movies()

    for movie in popular_movies:
        movie_id = movie["id"]
        movie_details = fetch_movie_details(movie_id)

        if movie_details:
            movie_data = {
                "Movie_ID": movie_id,
                "Title": movie["title"],
                "Release_Date": movie["release_date"],
                "Genres": [genre["name"] for genre in movie_details.get("genres", [])],
                "Vote_Average": movie["vote_average"],
                "Vote_Count": movie["vote_count"],
                "Popularity": movie["popularity"],
                "Budget": movie_details.get("budget", "N/A"),
                "Revenue": movie_details.get("revenue", "N/A"),
                "Production_Companies": [
                    company["name"] for company in movie_details.get("production_companies", [])
                ],
            }

            print(json.dumps(movie_data, indent=2))
            sleep(1)  # Simulate interval between sending messages
 
# Run the movie data processing
process_and_send_movies()
    ```
- Kafka Producer
    
    ```bash
  import json
import requests
from kafka import KafkaProducer
from rich import print
from time import sleep

# TMDb API Key
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"

# In-memory set to store movie IDs that have been processed
processed_movie_ids = set()

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['PNS-VirtualBox:9092'],
    value_serializer=lambda K: json.dumps(K).encode('utf-8')
)

# Fetch Popular Movies
def fetch_popular_movies(page=1):
    """
    Fetches popular movies from TMDb.
    """
    endpoint = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error fetching popular movies. Status code: {response.status_code}")
        return []

# Fetch Detailed Movie Data
def fetch_movie_details(movie_id):
    """
    Fetches detailed data for a single movie.
    """
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for Movie ID {movie_id}. Status code: {response.status_code}")
        return {}

# Process Movie Data and Send to Kafka
def process_and_send_movies():
    """
    Processes movie data and sends to Kafka.
    """
    popular_movies = fetch_popular_movies()

    for movie in popular_movies:
        movie_id = movie["id"]
        # Check if the movie has already been processed
            
        movie_details = fetch_movie_details(movie_id)

        if movie_details:
            movie_data = {
                "Movie_ID": movie_id,
                "Title": movie["title"],
                "Release_Date": movie["release_date"],
                "Genres": [genre["name"] for genre in movie_details.get("genres", [])],
                "Vote_Average": movie["vote_average"],
                "Vote_Count": movie["vote_count"],
                "Popularity": movie["popularity"],
                "Budget": movie_details.get("budget", "N/A"),
                "Revenue": movie_details.get("revenue", "N/A"),
                "Production_Companies": [
                    company["name"] for company in movie_details.get("production_companies", [])
                ],
            }

            # Send data to Kafka topic
            producer.send('tmdb_movies', value=movie_data)
            print(json.dumps(movie_data, indent=2)
            sleep(1)  # Simulate interval between sending messages

# Run the movie data processing
process_and_send_movies()

    ```
    
- Kafka Consumer
    
    ```bash
 # Import necessary libraries
from kafka import KafkaConsumer
from json import loads
from rich import print

# Create a Kafka consumer
consumer = KafkaConsumer(
    'tmdb_movies',  # Topic to consume messages from
    bootstrap_servers=['PNS-VirtualBox:9092'],  # Kafka server addresses
    auto_offset_reset='earliest',  # Reset offset to the latest available message
    enable_auto_commit=True,  # Enable auto commit of consumed messages
    group_id=None,  # Consumer group ID (None indicates an individual consumer)
    value_deserializer=lambda x: loads(x.decode('utf-8'))  # Deserialize the message value from JSON to Python object
)

# Process incoming messages
for message in consumer:
    data = message.value  # Get the value of the message (tweet)
    print(data)  # Print the tweet

    ```
    
    - check if the consumer got the data
        
        ```bash
        bin/kafka-console-consumer.sh --topic tmdb_movies-test --bootstrap-server ilyas-VirtualBox:9092 --from-beginning
        ```
       

