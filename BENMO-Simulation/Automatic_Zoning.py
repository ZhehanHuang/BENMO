#!/usr/bin/env python
# encoding: utf-8
"""
@author: Huang Zhehan
@contact: zhehanhuang@stu.xmu.edu.cn
@software: pycharm
@file: Automatic Zoning.py
@time: 2024/6/12 下午10:15
"""
import pickle
import numpy as np
import pandas as pd
import netCDF4 as nc
from scipy.ndimage import generic_filter
from tqdm.auto import tqdm
from tsfresh import extract_features
from scipy.spatial import Delaunay
from collections import deque
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import os
from torch_geometric.utils import to_dense_adj, add_self_loops
from community import community_louvain
from scipy.ndimage import label, generate_binary_structure, find_objects
from sklearn.preprocessing import normalize
from sklearn.cluster import SpectralClustering
import networkx as nx
from scipy.ndimage import binary_dilation
import geopandas as gpd
import scipy.sparse as sp

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def read_nc_data(self):
        self.data = nc.Dataset(self.file_path)
        return self.data

    def clear_data(self):
        if self.data is not None:
            self.data.close()
        self.data = None

    def extract_features(self, feature_names):
        if self.data is not None:
            user_input = input("Data is already loaded. Do you want to clear it and reload? (yes/no): ")
            if user_input.lower() == 'yes':
                self.clear_data()
                self.read_nc_data()
            else:
                pass
        else:
            self.read_nc_data()

        features = {}
        trim_vars = self.data.variables.keys()
        for feature_name in feature_names:
            if feature_name in trim_vars:
                features[feature_name] = np.ma.getdata(self.data.variables[feature_name][:])
            else:
                raise ValueError(f"No {feature_name} in database")

        return features

class DataPreprocessor:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.features = {}
        self.feature_names = []

    def extract_data_by_type(self, feature_names):
        self.feature_names = feature_names
        raw_features = self.data_loader.extract_features(feature_names)

        processing_map = {
            "temperature": lambda x: x[724:, :, :],
            "salinity": lambda x: x[724:, :, :],
            "density": lambda x: x[724:, :, :],
            "waterlevel": lambda x: x[724:, :, :],
            "grid_latitude": lambda x: x[:, :, 2],
            "grid_longitude": lambda x: x[:, :, 2],
            "tau_x": lambda x: x[724:, :, :],
            "tau_y": lambda x: x[724:, :, :],
            "velocity_x": lambda x: x[724:, :, :],
            "velocity_y": lambda x: x[724:, :, :],
            "depth": lambda x: x
        }

        for feature_name, process_func in processing_map.items():
            if feature_name in raw_features:
                self.features[feature_name] = process_func(raw_features[feature_name])

    def apply_grid_mask(self):
        grid = self.features["grid_latitude"]
        grid_mask = np.nan_to_num(grid, nan=0).astype(bool)
        grid_mask = grid_mask[np.newaxis, :, :]

        exclude_features = {"grid_latitude", "grid_longitude", "depth"}
        for feature in self.feature_names:
            if feature not in exclude_features:
                self.features[f"{feature}_masked"] = np.where(grid_mask, self.features[feature], np.nan)

        self.grid_mask_2d = grid_mask[0]

    def conditional_fill(self, slice, mask, size):
        def filter_func(window):
            if np.all(np.isnan(window)):
                return np.nan
            return np.nanmean(window)

        filled_slice = generic_filter(slice, filter_func, size=(size, size), mode='nearest')
        update_mask = np.isnan(slice) & mask
        slice[update_mask] = filled_slice[update_mask]
        return slice

    def fill_nan(self, feature_x, size, max_size, b):
        feature_filled = np.copy(feature_x)

        while size <= max_size:
            print(f"Applying filter with size: {size}")
            for t in tqdm(range(feature_filled.shape[0]), desc=f'Processing size {size}x{size}'):
                current_slice = feature_filled[t, :, :]
                current_slice = self.conditional_fill(current_slice, self.grid_mask_2d, size)
                feature_filled[t, :, :] = current_slice
            a = np.sum(np.isnan(feature_filled))
            if a == b:
                break
            size += 2

        if size > max_size:
            print("Reached maximum window size without fulfilling the condition.")
        else:
            print(f"Filling completed with window size: {size - 2}x{size - 2}")
        return feature_filled

    def preprocess_data(self, initial_size = 3, max_size = 21):
        self.apply_grid_mask()
        b = np.sum(np.isnan(self.features["temperature_masked"]))

        for feature in self.feature_names:
            if feature in self.features and np.sum(np.isnan(self.features[feature])) != b and feature not in {"grid_latitude", "grid_longitude", "depth"}:
                print(f"Filling {feature}")
                self.features[f"{feature}_filled"] = self.fill_nan(self.features[f"{feature}_masked"],
                                                                   size = initial_size, max_size = max_size, b = b)

        if "depth" in self.features:
            self.features["depth_masked"] = np.where(self.grid_mask_2d, self.features["depth"], np.nan)

class TimeseriesExtractor:
    def __init__(self, features):
        self.features = features

    def normalization(self, arr):
        mean = np.nanmean(arr, axis=(1, 2), keepdims=True)
        std = np.nanstd(arr, axis=(1, 2), keepdims=True)
        normalized_arr = (arr - mean) / std
        return normalized_arr.astype(np.float32)

    def flatten(self, feature):
        flat = feature.reshape(feature.shape[0], -1)
        return flat

    def clean_nan(self, feature_flat):
        feature_df = pd.DataFrame(feature_flat)
        feature_clean = feature_df.dropna(how='all', axis=1)
        feature_clean_array = feature_clean.to_numpy()
        return (feature_clean_array)

    def extract_time_series_features(self, features_to_normalize, chunk_size=1000):
        normalized_features = {}

        for feature in features_to_normalize:
            filled_key = f"{feature}_filled"
            masked_key = f"{feature}_masked"
            if filled_key in self.features:
                normalized_features[feature] = self.normalization(self.features[filled_key])
            elif masked_key in self.features:
                normalized_features[feature] = self.normalization(self.features[masked_key])

        cleaned_features = {}
        for feature in normalized_features:
            flattened_feature = self.flatten(normalized_features[feature])
            cleaned_feature = []

            for i in range(0, flattened_feature.shape[0], chunk_size):
                chunk = flattened_feature[i:i + chunk_size]
                cleaned_chunk = self.clean_nan(chunk)
                cleaned_feature.append(cleaned_chunk)

            cleaned_features[feature] = np.vstack(cleaned_feature)

        node_features = np.stack([cleaned_features[feature] for feature in features_to_normalize], axis=-1)
        reshape_df = node_features.transpose(1, 0, 2).reshape(-1, len(features_to_normalize))
        reshape_df = pd.DataFrame(reshape_df)
        labels = np.repeat(np.arange(node_features.shape[1]), node_features.shape[0])
        reshape_df.insert(0, 'id', labels)
        time_sequence = np.tile(np.arange(node_features.shape[0]), node_features.shape[1])
        reshape_df.insert(1, 'time', time_sequence)

        reshape_df.columns = ["id", "time"] + features_to_normalize
        reshape_df = reshape_df.astype(np.float32)

        return reshape_df

    def batch_extract_features(self, reshape_df, batch_size = 100):
        final_features = pd.DataFrame()
        unique_ids = reshape_df['id'].unique()
        num_batches = len(unique_ids) // batch_size + (1 if len(unique_ids) % batch_size > 0 else 0)

        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = start_idx + batch_size
            batch_ids = unique_ids[start_idx:end_idx]
            batch_df = reshape_df[reshape_df['id'].isin(batch_ids)]
            batch_features = extract_features(batch_df, column_id="id", column_sort="time", n_jobs=5)
            final_features = pd.concat([final_features, batch_features])
            print(f"Batch No. {i + 1}/{num_batches} finished")

        all_zero_columns = final_features.apply(lambda x: all(x == 0))
        final_features_clean = final_features.drop(final_features.columns[all_zero_columns], axis=1)
        final_features_clean = final_features_clean.dropna(axis=1, how='all')

        return final_features_clean

    def save_features(self, path, features):
        features.to_csv(path, index=False)
        print(f"Features saved to {path}")

    def load_features(self, path):
        features = pd.read_csv(path)
        print(f"Features loaded from {path}")
        return features

class SpatialBuilder:
    def __init__(self, _grid_x, _grid_y):
        self.grid_x = _grid_x
        self.grid_y = _grid_y
        self.grid_x_clean = self.reshape_grid(_grid_x)
        self.grid_y_clean = self.reshape_grid(_grid_y)
        self.grid_coor = np.array((self.grid_x_clean[:, 0], self.grid_y_clean[:, 0])).T

    def reshape_grid(self, grid):
        grid_flat = grid.reshape(-1)
        grid_df = pd.DataFrame(grid_flat)
        grid_clean = grid_df.dropna(how='all', axis=0)
        grid_clean_array = grid_clean.to_numpy()
        return grid_clean_array

    def construct_adjacency_matrix_delaunay(self):
        grid_coor = np.array((self.grid_x.flatten(), self.grid_y.flatten())).T
        mask = ~np.isnan(grid_coor).any(axis=1)
        grid_coor = grid_coor[mask]

        tri = Delaunay(grid_coor)

        num_nodes = len(grid_coor)
        rows, cols = [], []

        for simplex in tri.simplices:
            for i in simplex:
                for j in simplex:
                    if i != j:
                        rows.append(i)
                        cols.append(j)

        data = np.ones(len(rows), dtype=np.int8)
        adjacency_matrix = sp.coo_matrix((data, (rows, cols)), shape=(num_nodes, num_nodes))
        return adjacency_matrix

    def generate_adjacency_matrix_from_boolean_grid(self, grid, method="D8"):
        rows, cols = grid.shape
        num_nodes = rows * cols

        sea_nodes_indices = np.where(grid.ravel())[0]

        full_adjacency_matrix = sp.lil_matrix((num_nodes, num_nodes), dtype=int)

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # D4
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # D8
        ] if method == "D8" else [
            (0, 1), (0, -1), (1, 0), (-1, 0)  # D4
        ]

        for i in range(rows):
            for j in range(cols):
                if grid[i, j]:
                    node_index = i * cols + j
                    for dr, dc in directions:
                        r, c = i + dr, j + dc
                        if 0 <= r < rows and 0 <= c < cols and grid[r, c]:
                            neighbor_index = r * cols + c
                            full_adjacency_matrix[node_index, neighbor_index] = 1

        filtered_adjacency_matrix = full_adjacency_matrix[sea_nodes_indices, :][:, sea_nodes_indices]
        return filtered_adjacency_matrix.tocsr()

    def combine_adjacency_matrices(self, adj1, adj2):
        combined_adj = adj1 + adj2
        combined_adj.data = np.clip(combined_adj.data, 0, 1)  # 确保值在0到1之间
        return combined_adj

class SpatialFeatureExtractor:
    def __init__(self, grid_bool, grid_x, grid_y):
        self.grid_bool = grid_bool
        self.grid_x = grid_x
        self.grid_y = grid_y

    def find_edge_coordinates(self):
        padded_grid = np.pad(self.grid_bool, pad_width=1, mode='constant', constant_values=False)
        edge_x_list = []
        edge_y_list = []

        rows, cols = self.grid_bool.shape
        for i in range(rows):
            for j in range(cols):
                if self.grid_bool[i, j]:
                    neighbors = [
                        padded_grid[i:i + 3, j:j + 3]
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                                       (-1, -1), (-1, 1), (1, -1), (1, 1)]
                    ]
                    if any(~neighbor.all() for neighbor in neighbors):
                        edge_x_list.append(self.grid_x[i, j])
                        edge_y_list.append(self.grid_y[i, j])

        return np.array(edge_x_list), np.array(edge_y_list)

    def calculate_distances_to_edge(self, edge_x, edge_y):
        distances_land = np.full(self.grid_bool.shape, np.inf)

        for i in range(self.grid_bool.shape[0]):
            for j in range(self.grid_bool.shape[1]):
                if self.grid_bool[i, j]:
                    dist = np.sqrt((self.grid_x[i, j] - edge_x) ** 2 + (self.grid_y[i, j] - edge_y) ** 2)
                    distances_land[i, j] = np.min(dist)

        return distances_land

    def bfs(self, start_points):
        rows, cols = self.grid_bool.shape
        distance_matrix = np.full(self.grid_bool.shape, np.nan)

        queue = deque()
        for start_point in start_points:
            if self.grid_bool[start_point]:
                queue.append(start_point)
                distance_matrix[start_point] = 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            row, col = queue.popleft()

            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols and self.grid_bool[r, c] and np.isnan(distance_matrix[r, c]):
                    queue.append((r, c))
                    distance_matrix[r, c] = distance_matrix[row, col] + 1

        return distance_matrix

    def integrate_spatial_features(self, final_features, depth):
        edge_x, edge_y = self.find_edge_coordinates()
        distances_land = self.calculate_distances_to_edge(edge_x, edge_y)

        start_points = [(r, 3) for r in range(9, 53)]
        distance_sea = self.bfs(start_points)

        distance_land_flat = distances_land.reshape(-1)
        distance_sea_flat = distance_sea.reshape(-1)

        distance_land_clean = distance_land_flat[~np.isinf(distance_land_flat)]
        distance_sea_clean = distance_sea_flat[~np.isnan(distance_sea_flat)]

        distance_land_nor = (distance_land_clean - np.mean(np.abs(distance_land_clean))) / np.std(distance_land_clean)
        distance_sea_nor = (distance_sea_clean - np.mean(np.abs(distance_sea_clean))) / np.std(distance_sea_clean)

        final_features["distance_land_nor"] = distance_land_nor
        final_features["distance_sea_nor"] = distance_sea_nor

        depth_flat = depth.reshape(-1)
        depth_clean = depth_flat[~np.isnan(depth_flat)]
        depth_nor = (depth_clean - np.mean(np.abs(depth_clean))) / np.std(depth_clean)

        final_features["depth_nor"] = depth_nor

        return final_features

class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_dim, out_dim):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, out_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

class GCNTrainer:
    def __init__(self, data, num_features, hidden_dim=64, out_dim=16, lr=0.0005, margin=1.0, device='cpu'):
        self.data = data
        self.model = GCN(num_features, hidden_dim, out_dim).to(device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.margin = margin
        self.device = device
        self.data = self.data.to(device)
        self.edge_index = self.data.edge_index.to(device)

    def structural_loss(self, embeddings, edge_index):
        N = embeddings.size(0)
        adjacency_matrix = torch.zeros((N, N), device=self.device)
        adjacency_matrix[edge_index[0], edge_index[1]] = 1

        positive_pairs = edge_index.t()
        negative_pairs = []

        for _ in range(positive_pairs.size(0)):
            while True:
                u = torch.randint(0, N, (1,), device=self.device).item()
                v = torch.randint(0, N, (1,), device=self.device).item()
                if u != v and adjacency_matrix[u, v] == 0:
                    negative_pairs.append([u, v])
                    break

        negative_pairs = torch.tensor(negative_pairs, device=self.device)

        positive_loss = (embeddings[positive_pairs[:, 0]] - embeddings[positive_pairs[:, 1]]).pow(2).sum(1).mean()

        negative_distances = (embeddings[negative_pairs[:, 0]] - embeddings[negative_pairs[:, 1]]).pow(2).sum(1)
        negative_loss = torch.clamp(self.margin - torch.sqrt(negative_distances), min=0).pow(2).mean()

        total_loss = positive_loss + negative_loss

        return total_loss

    def train(self, epochs=1000):
        self.model.train()
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            embeddings = self.model(self.data)
            loss = self.structural_loss(embeddings, self.edge_index)
            loss.backward()
            self.optimizer.step()
            print(f"Epoch {epoch+1}, Loss: {loss.item()}")
        return self.model, embeddings

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)
        print(f"Model saved to {path}")

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        print(f"Model loaded from {path}")

class Cluster:
    def __init__(self, embeddings, edge_index):
        self.embeddings = embeddings.detach().cpu().numpy()
        edge_index_with_loops = add_self_loops(edge_index)[0]
        adj_matrix = to_dense_adj(edge_index_with_loops)[0].numpy()
        self.normalized_adj_matrix = normalize(adj_matrix, norm='l1', axis=1)

    def cluster_graph(self, method='louvain', k=5, embeddings=None, normalized_adj_matrix=None):
        if embeddings is None:
            embeddings = self.embeddings
        if normalized_adj_matrix is None:
            normalized_adj_matrix = self.normalized_adj_matrix

        if method == 'louvain':
            G = nx.from_scipy_sparse_matrix(normalized_adj_matrix)
            partition = community_louvain.best_partition(G)
            N = len(G.nodes())
            community_labels = np.zeros(N, dtype=int)
            for node, com_id in partition.items():
                community_labels[node] = com_id + 1
        elif method == 'spectral':
            sc = SpectralClustering(n_clusters=k, affinity='precomputed', assign_labels='discretize', random_state=0)
            community_labels = sc.fit_predict(normalized_adj_matrix)
        else:
            raise ValueError("Unsupported clustering method. Choose 'louvain' or 'spectral'.")

        return community_labels

class PostProcessor:
    def __init__(self, grid_bool, community_labels, original_shape=(281, 256)):
        self.grid_bool = grid_bool
        self.community_labels = community_labels
        self.original_shape = original_shape

    def restore_grid(self):
        restored_grid = np.full(self.original_shape, np.nan)
        grid_bool_flat = self.grid_bool.reshape(-1)
        valid_indices = np.where(grid_bool_flat)[0]

        for original_index, label in zip(valid_indices, self.community_labels):
            row, col = divmod(original_index, self.original_shape[1])
            restored_grid[row, col] = label

        return restored_grid

    def dynamic_majority_filter(self, data, initial_size=5, max_size=None, max_iterations=20):
        rows, cols = data.shape
        max_size = max_size if max_size else max(rows, cols)

        def find_majority(r, c, size, max_size):
            half_size = size // 2
            r_start, r_end = max(0, r - half_size), min(rows, r + half_size + 1)
            c_start, c_end = max(0, c - half_size), min(cols, c + half_size + 1)
            neighborhood = current_data[r_start:r_end, c_start:c_end].flatten()
            valid_values = neighborhood[neighborhood != -1]

            if valid_values.size > 0:
                unique, counts = np.unique(valid_values, return_counts=True)
                max_count = np.max(counts)
                candidates = unique[counts == max_count]
                if len(candidates) == 1:
                    return candidates[0]
                else:
                    return None if size < max_size else np.random.choice(candidates)
            return -1

        current_data = data.copy()
        changes = True
        iteration = 0
        with tqdm(total=max_iterations, desc="Filtering Progress") as pbar:
            for iteration in range(max_iterations):
                changes = False
                next_data = np.full(data.shape, -1)
                for r in range(rows):
                    for c in range(cols):
                        if current_data[r, c] == -1:
                            continue
                        size = initial_size
                        majority = None
                        while majority is None and size <= max_size:
                            majority = find_majority(r, c, size, max_size)
                            size += 2
                        if majority is not None and majority != current_data[r, c]:
                            next_data[r, c] = majority
                            changes = True
                        else:
                            next_data[r, c] = current_data[r, c]
                current_data = next_data
                if not changes:
                    print(f"No changes occurred after iteration {iteration}. Stopping early.")
                    break
                print(f"After iteration {iteration}: Changes occurred = {changes}")
                pbar.update(1)

        return current_data

    def custom_rule_smoothing(self, data, threshold_size=100):
        smoothed_data = data.copy()
        classes = np.unique(data[data >= 0])

        for class_value in classes:
            class_mask = (data == class_value)
            structure = generate_binary_structure(2, 1)
            labeled_array, num_features = label(class_mask, structure=structure)
            slices = find_objects(labeled_array)
            for i in range(1, num_features + 1):
                region = (labeled_array == i)
                region_size = np.sum(region)
                if region_size < threshold_size:
                    slice_i = slices[i - 1]
                    boundary_mask = binary_dilation(region[slice_i], structure=structure) & ~region[slice_i]
                    boundary_values = data[slice_i][boundary_mask]
                    if boundary_values.size == 0:
                        continue
                    unique, counts = np.unique(boundary_values, return_counts=True)
                    if unique[0] == -1:
                        unique, counts = unique[1:], counts[1:]
                    if counts.size > 0:
                        max_count_index = np.argmax(counts)
                        most_common_value = unique[max_count_index]
                        smoothed_data[region] = most_common_value
                    else:
                        continue
        return smoothed_data

def save_intermediate_result(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_intermediate_result(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def normalize_adjacency_matrix(adj):
    adj = sp.coo_matrix(adj)
    rowsum = np.array(adj.sum(1))
    d_inv_sqrt = np.power(rowsum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).tocoo()

if __name__ == "__main__":
    file_path = "E:/try/output/trim-SSW.nc"
    feature_names = ["temperature", "salinity", "density", "waterlevel", "grid_latitude", "grid_longitude",
                     "tau_x", "tau_y", "velocity_x", "velocity_y", "depth"]
    features_to_normalize = ["temperature", "salinity", "density", "waterlevel",
                             "tau_x", "tau_y", "velocity_x", "velocity_y"]

    data_loader = DataLoader(file_path)
    data_loader.read_nc_data()

    data_preprocessor = DataPreprocessor(data_loader)

    if os.path.exists('intermediate_features.pkl'):
        data_preprocessor.features = load_intermediate_result('intermediate_features.pkl')
    else:
        data_preprocessor.extract_data_by_type(feature_names)
        data_preprocessor.preprocess_data()
        save_intermediate_result(data_preprocessor.features, 'intermediate_features.pkl')

    ts_feature_extractor = TimeseriesExtractor(data_preprocessor.features)
    load_choice = input("Do you want to load existing features? (yes/no): ")
    if load_choice.lower() == 'yes':
        load_path = input("Please enter the path to load the features from: ")
        if os.path.exists(load_path):
            final_features_ts = ts_feature_extractor.load_features(load_path)
        else:
            print("Invalid path. Exiting.")
            exit()
    else:
        reshape_df = ts_feature_extractor.extract_time_series_features(features_to_normalize)
        final_features_ts = ts_feature_extractor.batch_extract_features(reshape_df)

        save_choice = input("Do you want to save the extracted features? (yes/no): ")
        if save_choice.lower() == 'yes':
            save_path = input("Please enter the path to save the features: ")
            ts_feature_extractor.save_features(save_path, final_features_ts)

    grid_x = data_preprocessor.features["grid_latitude"]
    grid_y = data_preprocessor.features["grid_longitude"]
    grid_bool = np.where(np.isnan(grid_x), False, True)
    depth = data_preprocessor.features["depth_masked"]

    spatial_feature_extractor = SpatialFeatureExtractor(grid_bool, grid_x, grid_y)
    final_features = spatial_feature_extractor.integrate_spatial_features(final_features_ts, depth)

    spatial_builder = SpatialBuilder(grid_x, grid_y)
    adj_matrix_delaunay = spatial_builder.construct_adjacency_matrix_delaunay()
    choice = input("Please enter 'D4' or 'D8' to choose the adjacency matrix construction method: ")
    if choice == 'D4':
        adj_matrix_grid = spatial_builder.generate_adjacency_matrix_from_boolean_grid(grid_bool, method="D4")
        print("D4 method selected to construct the adjacency matrix.")
    elif choice == 'D8':
        adj_matrix_grid = spatial_builder.generate_adjacency_matrix_from_boolean_grid(grid_bool, method="D8")
        print("D8 method selected to construct the adjacency matrix.")
    else:
        print("Invalid input. Please enter 'D4' or 'D8'.")
        adj_matrix_grid = sp.csr_matrix(adj_matrix_delaunay.shape, dtype=int)
    combined_adj = spatial_builder.combine_adjacency_matrices(adj_matrix_delaunay, adj_matrix_grid)
    normalized_adj = normalize_adjacency_matrix(combined_adj)

    final_features_tensor = torch.tensor(final_features.values, dtype=torch.float)
    rows, cols = combined_adj.nonzero()
    edge_index = torch.tensor([rows, cols], dtype=torch.long)
    data = Data(x=final_features_tensor, edge_index=edge_index)

    num_features = data.num_features
    gnn_trainer = GCNTrainer(data, num_features, hidden_dim = 64, out_dim = 16)

    load_choice = input("Do you want to load an existing model? (yes/no): ")
    if load_choice.lower() == 'yes':
        load_path = input("Please enter the path to load the model from: ")
        if os.path.exists(load_path):
            gnn_trainer.load_model(load_path)
            embeddings = gnn_trainer.model(data)
        else:
            print("Invalid path. Exiting.")
            exit()
    else:
        trained_model, embeddings = gnn_trainer.train(epochs=1000)

        save_choice = input("Do you want to save the trained model? (yes/no): ")
        if save_choice.lower() == 'yes':
            save_path = input("Please enter the path to save the model: ")
            gnn_trainer.save_model(save_path)

    method_input = input("Enter the clustering method ('louvain' or 'spectral'): ").strip().lower()
    if method_input == 'spectral':
        k_input = input("Enter the number of clusters for Spectral Clustering: ").strip()
        try:
            k = int(k_input)
        except ValueError:
            print("Invalid number of clusters. Using default value of 5.")
            k = 5
    else:
        k = None
    cluster = Cluster(embeddings, data.edge_index)
    community_labels = cluster.cluster_graph(method=method_input, k=k, normalized_adj_matrix=normalized_adj)

    post_processor = PostProcessor(grid_bool, community_labels)
    restored_grid = post_processor.restore_grid()
    restored_grid[np.isnan(restored_grid)] = -1
    filtered_data = post_processor.dynamic_majority_filter(restored_grid)
    smoothed_data = post_processor.custom_rule_smoothing(filtered_data)
    smoothed_data = smoothed_data.astype(float)
    smoothed_data[smoothed_data == -1] = np.nan

    flattened_grid = smoothed_data.flatten(order='F')
    flattened_grid_clean = flattened_grid[~np.isnan(flattened_grid)]

    grid_shp = gpd.read_file(r"./grd/grid.shp")
    grid_shp['class'] = flattened_grid_clean
    grid_shp.to_file(r"./grd/modified_gridD8.shp")
