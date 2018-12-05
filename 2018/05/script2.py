import string
from collections import deque


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        line = file.read().replace('\n', '')

    def opposite_polarity(left, right):
        return left.lower() == right.lower() and (
            (left.islower() and right.isupper())
            or (left.isupper() and right.islower())
        )

    poly_lengths = {}

    for alphabet_char in string.ascii_lowercase:
        poly = deque()
        new_line = line.replace(alphabet_char, '').replace(alphabet_char.upper(), '')

        for char in new_line:
            if len(poly) and opposite_polarity(poly[-1], char):
                poly.pop()
                while len(poly) > 1 and opposite_polarity(poly[-1], poly[-2]):
                    poly.pop()
                    poly.pop()
            else:
                poly.append(char)

        poly_lengths[alphabet_char] = len(poly)

    min_length = min(poly_lengths.values())

    print(f'The shorted polymer that can be produced is {min_length}')
