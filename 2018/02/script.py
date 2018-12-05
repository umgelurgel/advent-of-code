from collections import Counter

if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    two_count = 0
    three_count = 0

    for line in lines:
        letter_count = Counter(line)
        sums = Counter(letter_count).values()

        if 2 in sums:
            two_count += 1

        if 3 in sums:
            three_count += 1

    print(f'Checksum is {two_count * three_count}')
