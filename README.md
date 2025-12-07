This project builds a graph-based movie recommender using the MovieLens 100K dataset, comparing:

Personalized PageRank (PPR) – a graph-based personalized recommendation algorithm

Top-N Most Popular Movies – a simple non-personalized baseline

The dataset is represented as a bipartite graph:
User nodes:	943 MovieLens users
Movie nodes:	1,682 movies
Edges:	A user rated a movie
Edge weight	Rating score (1–5)

Files used:
u.data → user–movie ratings
u.item → movie titles

The full graph contains:
943 users
1,682 movies
100,000 edges

To dense to display so I did:
10 random users
10 random movies
Edges between them
Movie nodes labeled with titles

A. Personalized PageRank (PPR)
- recommend_movies_ppr()
How it works:
Start a random walk from the target user.
Move to movies they rated.
Move to other users who rated the same movies.
Continue spreading through the network.
Rank movies by how often the walk lands on them.

=== Personalized PageRank Recommendations ===
Toy Story (1995) (score: 0.1532)
Star Wars (1977) (score: 0.0032)
Twelve Monkeys (1995) (score: 0.0029)
Return of the Jedi (1983) (score: 0.0029)
Leaving Las Vegas (1995) (score: 0.0028)
English Patient, The (1996) (score: 0.0028)
Fargo (1996) (score: 0.0027)
Mighty Aphrodite (1995) (score: 0.0027)
Stand by Me (1986) (score: 0.0027)
Willy Wonka and the Chocolate Factory (1971) (score: 0.0025)

B. Popularity Baseline
- recommend_top_popular()
How it works:
Count how many ratings each movie received
Recommend the top N most-rated movies
- recommend_top_popular()

=== Popularity Baseline (Top Movies) ===
Star Wars (1977) (583 ratings)
Contact (1997) (509 ratings)
Fargo (1996) (508 ratings)
Return of the Jedi (1983) (507 ratings)
Liar Liar (1997) (485 ratings)
English Patient, The (1996) (481 ratings)
Scream (1996) (478 ratings)
Toy Story (1995) (452 ratings)
Air Force One (1997) (431 ratings)
Independence Day (ID4) (1996) (429 ratings)

Functions:

- load_data()

Loads MovieLens ratings (u.data) and movie titles (u.item)

- build_bipartite_graph(ratings)

Creates a NetworkX graph

Adds user nodes (bipartite=0)

Adds movie nodes (bipartite=1)

Adds edges with weight = rating

Returns the graph, user IDs, and movie IDs

- plot_bipartite_sample_titles()

Randomly selects a small subset of users and movies

Plots users on the left, movies on the right

Draws edges between them

Labels movie nodes with titles


