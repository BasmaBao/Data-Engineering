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
        if movie_id in processed_movie_ids:
            continue  # Skip already processed movie
            
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
            print(json.dumps(movie_data, indent=2))
            
            # Add movie ID to processed set to avoid re-sending
            processed_movie_ids.add(movie_id)
            
            sleep(1)  # Simulate interval between sending messages

# Run the movie data processing
process_and_send_movies()
