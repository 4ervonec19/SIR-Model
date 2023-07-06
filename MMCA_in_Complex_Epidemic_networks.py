import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import statistics

lambda_letter = 0.15
delta = 0.6
mu = 0.4
beta_array = np.linspace(0, 1, 20)

beta = 0.1
gamma = 0.0

amount_nodes = 500
time = 100

distribution = nx.utils.powerlaw_sequence(amount_nodes, exponent=2.5, seed=None)

def markov_chain_approach(time, beta):
    graph_real_layer = nx.expected_degree_graph(distribution, selfloops=False)
    graph_virtual_layer = nx.expected_degree_graph(distribution, selfloops=False)

    nodes_real = graph_real_layer.nodes()
    nodes_real_np = np.asarray(nodes_real)
    nodes_virtual = graph_virtual_layer.nodes()
    nodes_virtual_np = np.asarray(nodes_virtual)

    adjacency_matrix_real_layer = nx.adjacency_matrix(graph_real_layer)
    adjacency_matrix_real_layer = adjacency_matrix_real_layer.toarray()
    adjacency_matrix_virtual_layer = nx.adjacency_matrix(graph_virtual_layer)
    adjacency_matrix_virtual_layer = adjacency_matrix_virtual_layer.toarray()

    graph_with_initial_conditions = graph_real_layer
    nodes_all = graph_with_initial_conditions.nodes()

    for i in range(amount_nodes):
        nodes_all[i]['probability_dict'] = {'p_us': 0.79, 'p_ai': 0.195, 'p_as': 0.01, 'p_ui': 0.005}

    for timestamp in range(time):
        for nodes_i in range(amount_nodes):
            r_i = 1
            q_a = 1
            q_u = 1

            p_ai = nodes_all[nodes_i]['probability_dict']['p_ai']
            p_as = nodes_all[nodes_i]['probability_dict']['p_as']
            p_us = nodes_all[nodes_i]['probability_dict']['p_us']

            for j in range(amount_nodes):
                if nodes_i != j:
                    r_i = r_i * (1 - (adjacency_matrix_real_layer[nodes_i][j]*(p_ai + p_as)*lambda_letter))
                    q_a = q_a * (1 - (adjacency_matrix_virtual_layer[nodes_i][j]*p_ai*gamma*beta))
                    q_u = q_u * (1 - (adjacency_matrix_virtual_layer[nodes_i][j]*p_ai*beta))
                else:
                    r_i = r_i
                    q_a = q_a
                    q_u = q_u

            prob_us = p_ai * delta * mu + p_us * r_i * q_u + p_as * delta * q_u
            prob_as = p_ai * (1 - delta) * mu + p_us * (1 - r_i) * q_a + p_as * (1 - delta) * q_a
            prob_ai = p_ai * (1 - mu) + p_us * ((1 - r_i) * (1 - q_a) + r_i * (1 - q_u)) + p_as * (delta * (1 - q_u) + (1 - delta) * (1 - q_a))

            nodes_all[nodes_i]['probability_dict']['p_ai'] = prob_ai
            nodes_all[nodes_i]['probability_dict']['p_as'] = prob_as
            nodes_all[nodes_i]['probability_dict']['p_us'] = prob_us

    aware_array = []

    for i in range(amount_nodes):
        p_ai_new = nodes_all[i]['probability_dict']['p_ai']
        p_as_new = nodes_all[i]['probability_dict']['p_as']
        aware_array.append(p_ai_new + p_as_new)

    mean_value = statistics.mean(aware_array)
    return mean_value

mean_values_array = []

for ratio in beta_array:
    probability_in_aware = markov_chain_approach(time, ratio)
    mean_values_array.append(probability_in_aware)

print(mean_values_array)

plt.plot(beta_array, mean_values_array, color = 'red', linestyle = 'dotted')
plt.grid(True)
plt.show()





































