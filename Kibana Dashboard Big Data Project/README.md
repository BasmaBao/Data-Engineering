# Real-Time Data Pipeline with Kafka, Flink, Elasticsearch, and TMDB API

> **Basma El Baali**

### Overview:
This project aims to establish a data streaming pipeline with storage, processing, and visualization using:
- Kafka for asynchronous messaging
- Flink for processing data
- Hadoop for storage and backup
- Elasticsearch and Kibana for indexing and visualization

![test](https://github.com/user-attachments/assets/2c88b572-3865-4386-b6cf-a32047e76a5b)

- You can also use other tools as you like or add more tools, just make sure they are in sync with each other.

This is my documentation of the project I worked on. I'm using the TMDB API, but you can adjust or replace it with any other API as needed. Just ensure that the code is adjusted according to the specifications of the API you're working with. Remember, **<u>the technologies and JARs need to be compatible**</u>; otherwise, errors can occur. I've provided the code and step-by-step guide on how to work with them. *Make sure you don't skip any important steps.* Good luck!

## Project Part 1

### **`TMDB`** API

- **How to Get Your TMDB API Key:**

    To access data from the TMDB (The Movie Database) API, you need an API key. Here’s how you can get one:

    1. **Sign Up for an Account**: Go to the [TMDB website](https://www.themoviedb.org/) and create an account.
    2. **Generate an API Key**: Once logged in, go to the **API** section under your account settings:  
       [TMDB API Section](https://www.themoviedb.org/settings/api)
    3. **Create a New API Key**: Follow the instructions to create an API key. Once created, you'll receive a unique API key that you can use to make requests to the TMDB API.
    
    Here’s an example of how the key should be used:

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
    To create a Kafka topic named "my_topic", run the following command:

        ```bash
        bin/kafka-topics.sh --create --topic my_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
        ```

    - **List Topics**:  
    To list all existing topics, run:

        ```bash
        bin/kafka-topics.sh --list --bootstrap-server localhost:9092
        ```

    - **Produce Messages**:  
    Use the following command to produce messages to the "**my_topic**" topic:

        ```bash
        bin/kafka-console-producer.sh --topic my_topic --bootstrap-server localhost:9092
        ```

    - **Consume Messages**:  
    Open a new terminal and run the following command to consume messages from the "my_topic" topic:

        ```bash
        bin/kafka-console-consumer.sh --topic my_topic --bootstrap-server localhost:9092 --from-beginning
        ```

- **Server Properties**:
    - **Default Configuration**:

        ```python
        # Listener name, hostname, and port the broker will advertise to clients.
        # If not set, it uses the value for "listeners".
        advertised.listeners=PLAINTEXT://your.host.name:9092
        ```

    - **Custom Configuration**:

        ```python
        advertised.listeners=PLAINTEXT://ilyas-vm:9092
        ```

- ***My Kafka Info***:  
    After starting Zookeeper & Kafka, run the following commands:

        ```bash
        bin/zookeeper-server-start.sh config/zookeeper.properties
        bin/kafka-server-start.sh config/server.properties
        ```

    You should see the following output in the Kafka terminal:

        ```bash
        [2023-12-03 17:11:15,535] INFO Registered broker 0 at path /brokers/ids/0 with addresses: PLAINTEXT://ilyas-VirtualBox:9092, czxid (broker epoch): 124 (kafka.zk.KafkaZkClient)
        
        default topic: 'my-topic-test'
        bootstrap-server: 'ilyas-VirtualBox:9092'
        ```

---

This updated version includes clear instructions on how to obtain a TMDB API key and how to use it with an example.
