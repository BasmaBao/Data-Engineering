# Real-Time Data Pipeline with Kafka, Flink, Elasticsearch, and TMDB API

> **Basma El Baali**

### Overview:
This project sets up a real-time data streaming pipeline designed to process, store, and visualize movie-related data. The system utilizes a combination of powerful tools:
- **Kafka** for handling real-time, data streams.
- **Flink** for performing data processing in real-time, enabling insights and analytics.
- **Elasticsearch** for indexing and querying large volumes of data efficiently.
- **Kibana** for visualizing the processed data through intuitive dashboards.
- **TMDB API** to fetch movie-related data like movie details, ratings, and reviews.

The goal is to create an efficient pipeline that ingests real-time movie data, processes it, and displays visual analytics using Elasticsearch and Kibana. You can customize and extend this setup with additional tools, but ensure compatibility among all the components.

![imgs](schema.png)

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

