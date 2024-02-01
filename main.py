import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import constants
from data_parsing import get_frame_data





data_frames = get_frame_data(constants.FILE_NAME_REL)

fig, ax = plt.subplots()
rect = patches.Rectangle((0, 0), 100, 50, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)


def animate(i):
    ax.clear()
    ax.add_patch(patches.Rectangle((0, 0), constants.PITCH_X, constants.PITCH_Y, linewidth=1, edgecolor='r', facecolor='none'))
    data = data_frames[i]
    x_coords = [player['x'] for player in data['players']]
    y_coords = [player['y'] for player in data['players']]
    colors = [constants.class_colors[player['class_id']] for player in data['players']]

    # Überprüfen und Zeichnen der optionalen Balldaten
    if 'x' in data and 'y' in data and 'class' in data:
        ax.scatter(data['x'], data['y'], color=constants.class_colors[data['class']], marker='*', s=100)

    ax.scatter(x_coords, y_coords, c=colors)
    ax.set_title('Frame: {}'.format(i))
    ax.set_xlim(-5, constants.PITCH_X + 5)
    ax.set_ylim(-5, constants.PITCH_Y + 5)


# Erstellen der Animation
ani = FuncAnimation(fig, animate, frames=len(data_frames), interval=100)

plt.show()


