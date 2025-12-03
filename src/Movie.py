"""
Movie.py
====================================
This is an example file with correct docstring examples

| Author: Bailey Klote
| Date: 2025 December 1
"""


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

def load_data():
    """Loads MovieLens 100k dataset ratings and movie titles.
    """
    ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
    movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', usecols=[0, 1], names=['movie_id', 'title'], header=None)
    return ratings, movies



def build_bipartite_graph(ratings):
    """creates a bipartite graph with users on one side, movies on the other
    """
    B = nx.Graph()
    user_ids = ratings['user_id'].unique().tolist()
    movie_ids = ratings['movie_id'].unique().tolist()

    # Add nodes for users and movies
    B.add_nodes_from(user_ids, bipartite=0)
    B.add_nodes_from(movie_ids, bipartite=1)

    # Add edges weighted by rating
    for _, row in ratings.iterrows():
        B.add_edge(row['user_id'], row['movie_id'], weight=row['rating'])

    return B, user_ids, movie_ids



def plot_bipartite_graph(B, user_ids, movie_ids, max_users=10, max_movies=10):
    """Randomly samples a few users and movies for visualization
    """

    sampled_users = random.sample(list(user_ids), max_users)
    sampled_movies = random.sample(list(movie_ids), max_movies)
    H = B.subgraph(sampled_users + sampled_movies)

    # Position: users on left, movies on right
    pos = {}
    for i, u in enumerate(sampled_users):
        pos[u] = (0, i)
    for i, m in enumerate(sampled_movies):
        pos[m] = (1, i)

    plt.figure(figsize=(10, 6))
    nx.draw(H, pos, with_labels=True,
            node_color=['skyblue' if n in sampled_users else 'lightgreen' for n in H.nodes()],
            node_size=500, edge_color='gray')
    plt.title("Sample Bipartite User-Movie Graph")
    plt.show()



def recommend_movies_ppr(B, movie_ids, movies, user_id, top_n=10):
    """Returns top-N movie recommendations for a use
    """

    # Personalization vector: start random walk from this user
    personalization = {n: 0 for n in B.nodes()}
    personalization[user_id] = 1

    # Compute Personalized PageRank
    ppr = nx.pagerank(B, personalization=personalization, alpha=0.85)

    # Keep scores for movies only
    movie_scores = {n: score for n, score in ppr.items() if n in movie_ids}
    top_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Map movie IDs to titles
    return [(movies[movies['movie_id'] == m]['title'].values[0], score) for m, score in top_movies]



def recommend_top_popular(ratings, movies, top_n=10):
    """Returns most rated movies as a simple popularity baseline"""
    popular_movies = ratings.groupby('movie_id')['rating'].count().sort_values(ascending=False)[:top_n]
    return [(movies[movies['movie_id'] == m]['title'].values[0], count) for m, count in popular_movies.items()]


if __name__ == "__main__":
    # Load data
    ratings, movies = load_data()

    # Build graph
    B, user_ids, movie_ids = build_bipartite_graph(ratings)

    # Plot a small sampled bipartite graph
    plot_bipartite_graph(B, user_ids, movie_ids)

    # Pick a user to generate recommendations
    user_to_recommend = 1

    # Personalized PageRank recommendations
    print("Personalized PageRank Recommendations:")
    for title, score in recommend_movies_ppr(B, movie_ids, movies, user_to_recommend):
        print(f"{title} (score: {score:.4f})")

    # Top-N popular movies baseline
    print("\nTop-N Popular Movies Baseline:")
    for title, count in recommend_top_popular(ratings, movies):
        print(f"{title} (ratings: {count})")