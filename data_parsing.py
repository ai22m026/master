def remove_section(string, start_seq, end_seq):
    start_idx = string.find(start_seq)
    if start_idx == -1:
        return string  # Startsequenz nicht gefunden, gebe den originalen String zurück

    end_idx = string.find(end_seq, start_idx + len(start_seq))
    if end_idx == -1:
        return string  # Endsequenz nicht gefunden, gebe den originalen String zurück

    # Entferne den spezifizierten Abschnitt aus dem String
    return string[:start_idx] + string[end_idx + len(end_seq):], string[(start_idx + len(start_seq)):end_idx]


def parse_line(line):
    """Parses a single line of the data file."""

    outer, player_string = remove_section(line, "0:", ":")

    outer_data = parse_outer_data(outer)
    players = parse_players_data(player_string)

    parsed_data = {
        'timestamp': outer_data['timestamp'],
        'time_passed': outer_data['time_passed'],
        'half': outer_data['half'],
        'players': players  # 'players' ist bereits eine vorbereitete Liste von Spielerdaten
    }

    # Überprüfen, ob 'x', 'y' und 'class' in outer_data existieren und sie zum parsed_data hinzufügen
    if 'x' in outer_data:
        parsed_data['x'] = outer_data['x']
    if 'y' in outer_data:
        parsed_data['y'] = outer_data['y']
    if 'class' in outer_data:
        parsed_data['class'] = outer_data['class']
    return parsed_data


def parse_outer_data(line):
    parts = line.strip().split(';')
    timestamp = parts[0]
    other_data = parts[1].split(',')

    parsed_data = {
        'timestamp': int(timestamp),
        'time_passed': int(other_data[0]),
        'half': int(other_data[1])
    }

    # Überprüfen, ob x, y und class vorhanden sind
    if len(other_data) > 2:
        parsed_data['x'] = float(other_data[2])
    if len(other_data) > 3:
        parsed_data['y'] = float(other_data[3])
    if len(other_data) > 4:
        parsed_data['class'] = other_data[4]

    return parsed_data


def parse_players_data(player):
    """Parses a single player's data."""
    players = player.split(';')
    player_to_return = []
    for pl in players:
        if pl:
            class_id, player_id, player_game_id, x, y = pl.split(',')

            # clean class_id
            if class_id == '3':
                class_id = '0'
            if class_id == '4':
                class_id = '1'

            p = {'class_id': class_id, 'player_id': player_id,
                 'player_game_id': player_game_id, 'x': float(x), 'y': float(y)}
            player_to_return.append(p)
    return player_to_return


def get_frame_data(file_name):
    data_frames = []
    with open(file_name, 'r') as file:
        for _ in range(500):  # Read only the first 10 lines
            line = file.readline()
            if not line:
                break
            data_frames.append(parse_line(line))
    return data_frames
