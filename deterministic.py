from matplotlib import pyplot as plt, patches
from matplotlib.animation import FuncAnimation

from data_parsing import get_frame_data
import constants
import pandas as pd
import numpy as np

data_frames = get_frame_data(constants.FILE_NAME_REL)
frames = []
for frame in data_frames:
    players_df = pd.DataFrame(frame['players'])
    if 'x' in frame and 'y' in frame and 'class' in frame:
        # ball was tracked
        ball_x = float(frame['x'])
        ball_y = float(frame['y'])

        players_df['distance_to_ball'] = np.sqrt((players_df['x'] - ball_x) ** 2 + (players_df['y'] - ball_y) ** 2)

        players_in_possession_zone = players_df[players_df['distance_to_ball'] <= constants.POSESSION_RADIUS]
        players_df['possession'] = np.where(players_df['distance_to_ball'] <= constants.POSESSION_RADIUS, True, False)
        players_df['s'] = np.where(players_df['possession'], 200, 100)

        ball_data = {
            'class_id' : '5',
            'player_id': '000',
            'player_game_id': '000',
            'x': ball_x,
            'y': ball_y,
            'distance_to_ball': 0,
            'possession': False,  # Der Ball kann nicht im Besitz des Balls sein
            's': 100
        }
        players_df = pd.concat([players_df, pd.DataFrame([ball_data])], ignore_index=True)

    frames.append(players_df)

fig, ax = plt.subplots()
rect = patches.Rectangle((0, 0), constants.PITCH_X, constants.PITCH_Y, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)


def animate(i):
    ax.clear()
    ax.add_patch(
        patches.Rectangle((0, 0), constants.PITCH_X, constants.PITCH_Y, linewidth=1, edgecolor='r', facecolor='none'))
    frame_data = frames[i]
    colors = [constants.class_colors[class_id] for class_id in players_df['class_id']]
    ax.scatter(frame_data['x'], frame_data['y'], color=colors,  s=frame_data['s'])

    ax.set_title('Frame: {}'.format(i))
    ax.set_xlim(-5, constants.PITCH_X + 5)
    ax.set_ylim(-5, constants.PITCH_Y + 5)


# Erstellen der Animation
ani = FuncAnimation(fig, animate, frames=len(data_frames), interval=100)

plt.show()
