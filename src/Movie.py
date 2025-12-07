"""
Movie.py
====================================
This is an example file with functions to build a bipartite user-movie graph from the MovieLens 100k dataset,
visualize it, and generate movie recommendations using Personalized PageRank.

| Author: Bailey Klote
| Date: 2025 December 1
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
def load_data():
    ratings = pd.read_csv(
        "ml-100k/u.data",
        sep="\t",
        names=["user_id", "movie_id", "rating", "timestamp"]
    )
    movies = pd.read_csv(
        "ml-100k/u.item",
        sep="|",
        encoding="latin-1",
        usecols=[0, 1],
        names=["movie_id", "title"],
        header=None
    )
    return ratings, movies

# ---------------------------------------------------------
# BUILD FULL BIPARTITE GRAPH (all users + all movies)
# ---------------------------------------------------------
def build_bipartite_graph(ratings):
    B = nx.Graph()

    user_ids = ratings["user_id"].unique().tolist()
    movie_ids = ratings["movie_id"].unique().tolist()

    # Add nodes with bipartite sets
    B.add_nodes_from(user_ids, bipartite=0)   # users
    B.add_nodes_from(movie_ids, bipartite=1)  # movies

    # Add edges weighted by rating
    for _, row in ratings.iterrows():
        B.add_edge(row["user_id"], row["movie_id"], weight=row["rating"])

    return B, user_ids, movie_ids

# ---------------------------------------------------------
# PLOT A SAMPLED BIPARTITE GRAPH WITH MOVIE TITLES
# ---------------------------------------------------------
def plot_bipartite_sample_titles(B, user_ids, movie_ids, movies,
                                 max_users=10, max_movies=10):
    """
    Plots a small, readable sample of the graph.
    Movie nodes are labeled with titles.
    """
    sampled_users = random.sample(user_ids, max_users)
    sampled_movies = random.sample(movie_ids, max_movies)

    H = B.subgraph(sampled_users + sampled_movies)

    # Position: users at x=0, movies at x=1
    pos = {}
    for i, u in enumerate(sampled_users):
        pos[u] = (0, i)
    for i, m in enumerate(sampled_movies):
        pos[m] = (1, i)

    plt.figure(figsize=(14, 7))

    # Draw user nodes
    nx.draw_networkx_nodes(
        H, pos,
        nodelist=sampled_users,
        node_color="skyblue",
        node_size=600,
        label="Users"
    )

    # Draw movie nodes
    nx.draw_networkx_nodes(
        H, pos,
        nodelist=sampled_movies,
        node_color="lightgreen",
        node_size=600,
        label="Movies"
    )

    # Draw edges
    nx.draw_networkx_edges(H, pos, edge_color="gray")

    # Movie labels
    movie_labels = {
        m: movies[movies.movie_id == m].title.values[0]
        for m in sampled_movies
    }
    nx.draw_networkx_labels(H, pos, labels=movie_labels, font_size=7)

    # User labels
    user_labels = {u: f"User {u}" for u in sampled_users}
    nx.draw_networkx_labels(H, pos, labels=user_labels, font_size=7)

    plt.title("Sample Bipartite Graph (Users ↔ Movie Titles)")
    plt.axis("off")
    plt.show()

# ---------------------------------------------------------
# PERSONALIZED PAGERANK RECOMMENDER
# ---------------------------------------------------------
def recommend_movies_ppr(B, movie_ids, movies, user_id, top_n=10):
    """
    Run Personalized PageRank for one user.
    """
    personalization = {n: 0 for n in B.nodes()}
    personalization[user_id] = 1  # random walk starts here

    ppr = nx.pagerank(B, alpha=0.85, personalization=personalization)

    movie_scores = {m: score for m, score in ppr.items() if m in movie_ids}

    top_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return [(movies[movies.movie_id == m].title.values[0], score)
            for m, score in top_movies]

# ---------------------------------------------------------
# POPULARITY BASELINE
# ---------------------------------------------------------
def recommend_top_popular(ratings, movies, top_n=10):
    """
    Returns most-rated movies (count of ratings).
    """
    counts = ratings.groupby("movie_id")["rating"].count().sort_values(ascending=False)[:top_n]
    return [(movies[movies.movie_id == m].title.values[0], count)
            for m, count in counts.items()]

# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
if __name__ == "__main__":
    ratings, movies = load_data()
    B, user_ids, movie_ids = build_bipartite_graph(ratings)

    # 1. Plot a readable sampled graph
    plot_bipartite_sample_titles(B, user_ids, movie_ids, movies)

    # 2. Run Personalized PageRank
    user = 1
    print("\n=== Personalized PageRank Recommendations ===")
    recommendations = recommend_movies_ppr(B, movie_ids, movies, user)
    for title, score in recommendations:
        print(f"{title} (score: {score:.4f})")

    # 3. Popularity baseline
    print("\n=== Popularity Baseline (Top Movies) ===")
    popular = recommend_top_popular(ratings, movies)
    for title, count in popular:
        print(f"{title} ({count} ratings)")

