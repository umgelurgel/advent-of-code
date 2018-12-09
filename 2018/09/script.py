import re
from collections import defaultdict
from datetime import datetime

from blist import blist


if __name__ == '__main__':
    # line = '9 players; last marble is worth 25 points'
    # line = '10 players; last marble is worth 1618 points'
    # line = '30 players; last marble is worth 5807 points'
    line = '404 players; last marble is worth 71852 points'

    regex_str = r'^(?P<player_count>\d+) players; last marble is worth (?P<last_marble>\d+) points'
    regex = re.compile(regex_str)
    group_dict = regex.match(line).groupdict()
    player_count = int(group_dict['player_count'])
    last_marble = int(group_dict['last_marble']) * 100

    marbles = blist([0])

    current_index = 0
    player_id = 0
    marble_id = 1
    player_totals = defaultdict(int)

    while marble_id <= last_marble:
        if marble_id % 10000 == 0:
            print(f'{datetime.utcnow()}: {marble_id}')
        if marble_id % 23 == 0:
            # Remove the marble 7 places left from current
            removed_ix = (current_index - 7) % len(marbles)
            removed_val = marbles[removed_ix]
            del marbles[removed_ix]

            # Add the current and removed marbles to player totals
            player_totals[player_id] += marble_id + removed_val

            # Update current_index
            current_index = removed_ix
        else:
            # Update current_index
            current_index = (current_index + 2) % len(marbles)

            # Place the marble in the correct position
            marbles.insert(current_index, marble_id)

        marble_id += 1
        player_id = (player_id + 1) % player_count

    print(f'High score is: {max(player_totals.values())}')