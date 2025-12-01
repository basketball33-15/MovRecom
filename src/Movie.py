"""
Movie.py
====================================
This is an example file with correct docstring examples

| Author: Bailey Klote
| Date: 2025 December 1
"""

import pandas as pd

# Load ratings
ratings = pd.read_csv("ml-100k/u.data", sep="\t",
                      names=["user_id", "movie_id", "rating", "timestamp"])

# Load movies
movies = pd.read_csv("ml-100k/u.item", sep="|", encoding="latin-1", header=None)

# Load users
users = pd.read_csv("ml-100k/u.user", sep="|",
                    names=["user_id", "age", "gender", "occupation", "zip_code"])

# Load genres
genres = pd.read_csv("ml-100k/u.genre", sep="|", names=["genre", "id"], encoding="latin-1")

# Quick check: print first 5 rows
print("Ratings:\n", ratings.head())
print("Movies:\n", movies.head())
print("Users:\n", users.head())
print("Genres:\n", genres.head())






if __name__ == '__main__':
    """Runs if file called as script as opposed to being imported as a library
    """
    bob = SayHello('Bob')
    bobLen = bob.greet(', welcome!')
    print(bobLen)