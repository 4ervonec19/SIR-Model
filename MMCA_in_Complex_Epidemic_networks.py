import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import statistics



lambda_letter = 0.15
delta = 0.6
mu = 0.4
beta_array = np.linspace(0, 1, 20)

gamma = 0.0
from_beta_mean_target = []
from_beta_mean_target_s = []


distribution = nx.utils.powerlaw_sequence(100, exponent=2.5, seed=None)
graph_real_layer = nx.expected_degree_graph(distribution, selfloops=False)
graph_virtual_layer = nx.expected_degree_graph(distribution, selfloops=False)

nodes_real = graph_real_layer.nodes()
nodes_real_np = np.asarray(nodes_real)
nodes_virtual = graph_virtual_layer.nodes()
nodes_virtual_np = np.asarray(nodes_virtual)

np.random.shuffle(nodes_real_np)
np.random.shuffle(nodes_virtual_np)

initial_fraction_infected = 0.2
initial_fraction_suspected = 0.8

for i in range(len(nodes_real)):
    nodes_real[nodes_real_np[i]]['Compartment'] = 'S'

break_point = initial_fraction_infected * len(nodes_real)
count = 0
for i in range(len(nodes_real_np)):
    nodes_real[nodes_real_np[i]]['Compartment'] = 'I'
    count += 1
    if count == break_point:
        break

for i in range(len(nodes_virtual)):
    nodes_virtual[nodes_virtual_np[i]]['Compartment'] = 'U'

break_point = initial_fraction_infected * len(nodes_virtual)
count = 0
for i in range(len(nodes_virtual)):
    nodes_virtual[nodes_virtual_np[i]]['Compartment'] = 'A'
    count += 1
    if count == break_point:
        break

for i in range(len(nodes_real)):
    if nodes_real[i]['Compartment'] == 'I' and nodes_virtual[i]['Compartment'] == 'A':
        nodes_real[i]['AI_prob'] = 0.2 ** 2
    else:
        nodes_real[i]['AI_prob'] = 1 - 0.2 ** 2

    if nodes_virtual[i]['Compartment'] == 'A':
        nodes_real[i]['A_prob'] = 0.2
    else:
        nodes_real[i]['A_prob'] = 0.8

    if nodes_real[i]['Compartment'] == 'S' and nodes_virtual[i]['Compartment'] == 'A':
        nodes_real[i]['AS_prob'] = 0.2 * 0.8
    else:
        nodes_real[i]['AS_prob'] = 1 - 0.2 * 0.8

    if nodes_real[i]['Compartment'] == 'S' and nodes_virtual[i]['Compartment'] == 'U':
        nodes_real[i]['US_prob'] = 0.2 * 0.8
    else:
        nodes_real[i]['US_prob'] = 1 - 0.2 * 0.8

# for i in range(len(nodes_real)):
#     print(nodes_real[i]['AI_prob'], nodes_real[i]['A_prob'], sep='\t')

adjacency_matrix = nx.adjacency_matrix(graph_real_layer, nodelist=nodes_real)
adjacency_matrix = adjacency_matrix.toarray()


for betas in range(len(beta_array)):



    for i in range(len(nodes_real)):
        factor = [1, 1, 1]
        for j in range(100):
            factor[0] = (1 - adjacency_matrix[i][j]*nodes_real[i]['A_prob']*lambda_letter)*factor[0]
            factor[1] = (1 - adjacency_matrix[i][j]*nodes_real[i]['AI_prob']*0.0)*factor[1]
            factor[2] = (1 - adjacency_matrix[i][j]*nodes_real[i]['AI_prob']*beta_array[betas])*factor[2]
            if j == 999:
                nodes_real[i]['r_rate'] = factor[0]
                nodes_real[i]['qa_rate'] = factor[1]
                nodes_real[i]['qu_rate'] = factor[2]

    # for i in range(len(nodes_real)):
    #     print("{0:.2f}".format(nodes_real[i]['AI_prob']), "{0:.2f}".format(nodes_real[i]['A_prob']), "{0:.2f}".format(nodes_real[i]['AS_prob']),
    #           "{0:.2f}".format(nodes_real[i]['US_prob']),
    #           "{0:.2f}".format(nodes_real[i]['r_rate']),
    #           "{0:.2f}".format(nodes_real[i]['qa_rate']),
    #           "{0:.2f}".format(nodes_real[i]['qu_rate'],
    #             sep='\t'))


    time_laps =[]
    mean_target = []
    mean_target_s = []

    for i in range(len(nodes_real)):
        p_ai = []
        p_as = []
        p_us = []
        p_ai.append(nodes_real[i]['AI_prob'])
        p_as.append(nodes_real[i]['AS_prob'])
        p_us.append(nodes_real[i]['US_prob'])
        for time in range(1000):
            factor = [1, 1, 1]
            for j in range(100):
                factor[0] = (1 - adjacency_matrix[i][j] * nodes_real[i]['A_prob'] * lambda_letter) * factor[0]
                factor[1] = (1 - adjacency_matrix[i][j] * nodes_real[i]['AI_prob'] * 0.0) * factor[1]
                factor[2] = (1 - adjacency_matrix[i][j] * nodes_real[i]['AI_prob'] * beta_array[betas]) * factor[2]

            p_ai.append(p_ai[-1]*(1-mu) + p_us[-1] * ((1 - factor[0]) * (1 - factor[1]) + factor[0]* (1 - factor[2])) + p_as[-1] * (delta * (1 - factor[2]) + (1 - delta)*(1 - factor[1]) ))
            p_as.append(p_ai[-1] * (1 - delta) * mu + p_us[-1] * (1 - factor[0])* factor[1] + p_as[-1] * (1 - delta) * factor[1])
            p_us.append(p_ai[-1] * delta * mu + p_us[-1] * factor[0] * factor[2] + p_as[-1] * delta * factor[2])

        mean_target.append(statistics.mean(p_ai))
        # mean_target_s.append(statistics.mean(p_as))


    from_beta_mean_target.append(statistics.mean(mean_target))




print(from_beta_mean_target)

plt.plot(beta_array, from_beta_mean_target)
plt.xlabel('beta')
plt.ylabel('Probability in Aware')

plt.grid()
plt.show()



















