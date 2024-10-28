import networkx as nx
import pandas as pd
import random
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

# Sample size variables for easy adjustment
SAMPLE_SIZE_AVG_PATH_LENGTH = 100000  # Number of node pairs to sample for average path length
SAMPLE_SIZE_DIAMETER = 10             # Number of nodes to sample for BFS in approximate diameter

# Load the edge and node data
edges_df = pd.read_csv("data/edges.csv")
nodes_df = pd.read_csv("data/nodes.csv")

# Merge edges with node data to get modularity classes for each source and target
edges_with_clusters = edges_df.merge(nodes_df[['Id', 'modularity_class']], left_on='Source', right_on='Id', how='left') \
                              .rename(columns={'modularity_class': 'Source Cluster'}) \
                              .merge(nodes_df[['Id', 'modularity_class']], left_on='Target', right_on='Id', how='left') \
                              .rename(columns={'modularity_class': 'Target Cluster'})

# Identify within-cluster and cross-cluster edges
edges_with_clusters['Connection Type'] = edges_with_clusters.apply(
    lambda row: 'Within Cluster' if row['Source Cluster'] == row['Target Cluster'] else 'Cross Cluster', axis=1
)

# Count within-cluster and cross-cluster edges
within_cluster_edges = edges_with_clusters[edges_with_clusters['Connection Type'] == 'Within Cluster']
cross_cluster_edges = edges_with_clusters[edges_with_clusters['Connection Type'] == 'Cross Cluster']

# Calculate cluster density
total_edges = len(edges_with_clusters)
within_cluster_count = len(within_cluster_edges)
cross_cluster_count = len(cross_cluster_edges)
cluster_density = within_cluster_count / total_edges if total_edges > 0 else 0

print(f"Total Edges: {total_edges}")
print(f"Within-Cluster Edges: {within_cluster_count} ({(within_cluster_count / total_edges) * 100:.2f}%)")
print(f"Cross-Cluster Edges: {cross_cluster_count} ({(cross_cluster_count / total_edges) * 100:.2f}%)")
print(f"Cluster Density: {cluster_density}\n")

# Create the graph from the edge list
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target', create_using=nx.Graph())

# Filter to the largest connected component (WCC) for faster calculations
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()

# Use G_lcc for further calculations

# Calculate degree and eigenvector centrality
degree_dict = dict(G_lcc.degree())
eigenvector_centrality = nx.eigenvector_centrality(G_lcc, max_iter=1000)

# Top 10 connected users by degree
top_connected_users = pd.DataFrame(list(degree_dict.items()), columns=['Node', 'Degree'])
top_connected_users = top_connected_users.sort_values(by='Degree', ascending=False).head(10)
top_connected_users['Eigenvector Centrality'] = top_connected_users['Node'].map(eigenvector_centrality)
print("\nTop 10 Connected Users by Degree with Eigenvector Centrality:")
print(top_connected_users)

# Average Path Length with Parallel Sampling
def calculate_path_length_parallel(graph, sample_size):
    nodes = list(graph.nodes)
    def get_random_path(_):
        node1, node2 = random.sample(nodes, 2)
        try:
            return nx.shortest_path_length(graph, node1, node2)
        except nx.NetworkXNoPath:
            return None

    with ThreadPoolExecutor() as executor:
        lengths = list(tqdm(executor.map(get_random_path, range(sample_size)), total=sample_size, desc="Avg Path Length"))
    
    valid_lengths = [l for l in lengths if l is not None]
    return sum(valid_lengths) / len(valid_lengths) if valid_lengths else float('inf')

start_time = time.time()
approx_avg_path_length = calculate_path_length_parallel(G_lcc, SAMPLE_SIZE_AVG_PATH_LENGTH)
print(f"\nApproximate Average Path Length: {approx_avg_path_length}")
print(f"Time taken: {time.time() - start_time:.2f} seconds")

# Diameter Calculation with Sample BFS
print("\nCalculating approximate diameter with BFS...")
approx_diameter = max([max(nx.single_source_shortest_path_length(G_lcc, random.choice(list(G_lcc.nodes))).values()) for _ in tqdm(range(SAMPLE_SIZE_DIAMETER), desc="Diameter")])
print(f"Approximate Diameter: {approx_diameter}")
