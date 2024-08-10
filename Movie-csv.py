import csv
import requests

# Hardcoded API key but not safe don't you do it
API_KEY = "acea7f75358a27d433ae144f3beeb313"


def search_tmdb(query):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get("results", [])


def get_movie_details(movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(base_url, params=params)
    return response.json()


def save_to_csv(filename, movies):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Title', 'Average Rating', 'Release Date', 'Runtime'])
        
        if file.tell() == 0:
            writer.writeheader()
        for movie in movies:
            writer.writerow({
                'ID': movie['id'],
                'Title': movie['title'],
                'Average Rating': movie['vote_average'],
                'Release Date': movie['release_date'],
                'Runtime': movie.get('runtime', '')  # Add runtime only if available
            })


def calculate_total_runtime(filename):
    total_runtime = 0
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                runtime = row.get('Runtime', '')
                if runtime.isdigit():
                    total_runtime += int(runtime)
    except FileNotFoundError:
        pass
    return total_runtime

def main():
    while True:
        query = input("Enter your search query for movies: ")
        try:
            results = search_tmdb(query)
            print(f"Search results for '{query}':")
            for idx, result in enumerate(results, start=1):
                print(f"{idx}. {result['title']} ({result['release_date']})")
            selected_idx = int(input("Enter the number of the movie to get its details: "))
            if selected_idx < 1 or selected_idx > len(results):
                print("Invalid selection.")
                continue
            selected_movie = results[selected_idx - 1]
            movie_id = selected_movie['id']
            result = get_movie_details(movie_id)
            print(f"Details for {result['title']}:")
            print(f"ID: {result['id']}")
            print(f"Overview: {result['overview']}")
            print(f"Average rating: {result['vote_average']}")
            print(f"Release date: {result['release_date']}")
            print(f"Runtime: {result.get('runtime', '')} minutes")
            choice = input("Press 'q' to quit, 'c' to continue, or 's' to save movie details to CSV: ")
            if choice.lower() == 'q':
                break
            elif choice.lower() == 's':
                filename = "movies.csv"
                save_to_csv(filename, [result])  # Only save the selected movie details
                print(f"Movie details saved to {filename}")
        except Exception as e:
            print("An error occurred:", e)

    
    total_runtime = calculate_total_runtime("movies.csv")
    print(f"Total Runtime of movies in CSV file: {total_runtime}minutes )))")
    print('''Exiting program..Ok bye''')

if __name__ == "__main__":
    main()
