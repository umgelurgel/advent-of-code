import re
from collections import Counter, defaultdict

if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    # #1 @ 12,548: 19x10
    regex_str = r'^#(?P<claim_id>\d+) @ (?P<x_min>\d+),(?P<y_min>\d+): (?P<x_size>\d+)x(?P<y_size>\d+)'
    regex = re.compile(regex_str)

    inches = defaultdict(int)

    for line in lines:
        parsed = regex.match(line).groupdict()
        claim_id = int(parsed['claim_id'])
        x_min = int(parsed['x_min'])
        y_min = int(parsed['y_min'])
        x_size = int(parsed['x_size'])
        y_size = int(parsed['y_size'])

        single_overlap_sum = 0

        for x_offset in range(x_size):
            for y_offset in range(y_size):
                x_current = x_min + x_offset
                y_current = y_min + y_offset

                single_overlap_sum += inches[f'{x_current},{y_current}'] 
                inches[f'{x_current},{y_current}'] += 1

        if single_overlap_sum == 0:
            printf(f'The claim that does not overlap')

    overlap_sum = 0
    for key, value in Counter(inches.values()).items():
        if key != 1:
            overlap_sum += value

    print(f'There are {overlap_sum} inches that overlap.')
