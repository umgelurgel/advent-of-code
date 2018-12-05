from collections import deque


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        line = file.read().replace('\n', '')

    # line = 'dabAcCaCBAcCcaDA'
    poly = deque()

    def opposite_polarity(left, right):
        return left.lower() == right.lower() and (
            (left.islower() and right.isupper())
            or (left.isupper() and right.islower())
        )

    for char in line:
        if len(poly) and opposite_polarity(poly[-1], char):
            poly.pop()
            while len(poly) > 1 and opposite_polarity(poly[-1], poly[-2]):
                poly.pop()
                poly.pop()
        else:
            poly.append(char)

    print(f'The final polymer is {"".join(poly)}')

    with open('output.txt', 'w') as f:
        f.write("".join(poly))
