import constants
import networkx as nx
import numpy as np
import torch
from torch_geometric.utils.convert import from_networkx
import matplotlib.pyplot as plt
from data_parsing import get_frame_data


def construct_feature_vector(x, y, class_id, is_ball):
    x = (x - constants.PITCH_X_HALF) / constants.PITCH_X
    y = (y - constants.PITCH_Y_HALF) / constants.PITCH_Y
    team_a = 0
    team_b = 0
    ball = 0
    if class_id == 0 or class_id == 3:
        team_a = 1
    if class_id == 1 or class_id == 4:
        team_b = 1
    if is_ball:
        ball = 1
        team_a = 0

    return np.array([x, y, team_a, team_b, ball])


data_frames = get_frame_data(constants.FILE_NAME_REL)
frame = data_frames[25]  # nur ein frame bis es funktioniert
players_df = frame['players']
closest_players = []
if 'x' in frame and 'y' in frame:
    for player in players_df:
        if player['class_id'] != '5':  # Ignorieren Sie den Ball selbst
            player['distance_to_ball'] = np.sqrt(
                (player['x'] - frame['x']) ** 2 + (player['y'] - frame['y']) ** 2)

    non_ball_players = [player for player in players_df if player['class_id'] != '5']
    sorted_players = sorted(non_ball_players, key=lambda x: x['distance_to_ball'])

    closest_players = sorted_players[:5]

    ball_data = {
        'class_id': '5',
        'player_id': '000',
        'player_game_id': '000',
        'x': frame['x'],
        'y': frame['y'],
    }
    players_df.append(ball_data)


# Make the networkx graph
G = nx.Graph()

for row in players_df:
    state = construct_feature_vector(row['x'], row['y'], row['class_id'], row['class_id'] == 5)
    G.add_node(row['player_id'], pos=(row['x'], row['y']), class_id=row['class_id'], internal_state=state)

for _, player in enumerate(closest_players):
    G.add_edge('000', player['player_id'])

threshold_distance = 15  # Schwellenwert 25 wie im Paper
for i, pi in enumerate(players_df):
    for j, pj in enumerate(players_df):
        if i != j:
            distance = np.sqrt((pi['x'] - pj['x']) ** 2 +
                               (pi['y'] - pj['y']) ** 2)
            if distance <= threshold_distance:
                G.add_edge(pi['player_id'], pj['player_id'])

colors = []
for node in G.nodes(data=True):
    colors.append(constants.class_colors[node[1]['class_id']])


pos = {node: data.get('pos', (0, 0)) for node, data in G.nodes(data=True)}

nx.draw(G, pos, with_labels=True, node_color=colors)
plt.show()
exit()

# Convert the graph into PyTorch geometric
pyg_graph = from_networkx(G)

print(pyg_graph)
# Data(edge_index=[2, 12], x=[5], y=[5])
print(pyg_graph.x)
# tensor([0.5000, 0.2000, 0.3000, 0.1000, 0.2000])
print(pyg_graph.y)
# tensor([1, 2, 3, 4, 5])
print(pyg_graph.edge_index)
# tensor([[0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4],
#         [1, 3, 4, 0, 2, 3, 1, 4, 0, 1, 0, 2]])


# Split the data
train_ratio = 0.2
num_nodes = pyg_graph.x.shape[0]
num_train = int(num_nodes * train_ratio)
idx = [i for i in range(num_nodes)]

np.random.shuffle(idx)
train_mask = torch.full_like(pyg_graph.y, False, dtype=bool)
train_mask[idx[:num_train]] = True
test_mask = torch.full_like(pyg_graph.y, False, dtype=bool)
test_mask[idx[num_train:]] = True

print(train_mask)
# tensor([ True, False, False, False, False])
print(test_mask)
# tensor([False,  True,  True,  True,  True])
