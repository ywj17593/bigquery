import numpy as np
from service_migration import dataset_query, env
import matplotlib.pyplot as plt
import networkx as nx

#####################  hyper parameters  ####################
BS_NUMBER = 5
THRESHOLD = 10000
MAX_STEP = 5


def create_graph():
    # Create connection matrix and graph of the base stations
    dataset = dataset_query.dataset_input("machine_list")
    base_station_dataset = dataset.sample(n=BS_NUMBER)
    cost_array = np.arange(BS_NUMBER ** 2).reshape(BS_NUMBER, BS_NUMBER)
    for i in range(BS_NUMBER):
        for j in range(BS_NUMBER):
            loc_1 = (base_station_dataset.iloc[i]["latitude"], base_station_dataset.iloc[i]["longitude"])
            loc_2 = (base_station_dataset.iloc[j]["latitude"], base_station_dataset.iloc[j]["longitude"])
            cost_array[i][j] = env.distance(loc_1, loc_2)
    connection_array = np.where(cost_array < THRESHOLD, 1, 0)

    # Select tasks related to selected base stations
    dataset = dataset_query.dataset_input("cluster_job_combined_notnull")
    job_dataset = dataset[dataset["cpu_id"].isin(base_station_dataset["machineId"])]

    G = nx.Graph()
    for i in range(BS_NUMBER):
        G.add_node(i, name=base_station_dataset.iloc[i]["machineId"])
        for j in range(BS_NUMBER):
            if connection_array[i][j] == 1:
                G.add_edge(i, j, name=cost_array[i][j])
    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    node_labels = nx.get_node_attributes(G, 'name')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(G, 'name')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return BS_NUMBER, MAX_STEP, cost_array, connection_array, job_dataset, base_station_dataset
