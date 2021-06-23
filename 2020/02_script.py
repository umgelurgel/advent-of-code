import re
from collections import Counter

def get_input():
    with open("02_a_input.txt","r") as file:
        lines = [x for x in file.read().split('\n') if x]

    regex = re.compile(r"(\d+)-(\d+) (\w): (\w+)")
    elems = []

    for line in lines:
        result = regex.match(line)
        if not result:
            import pdb; pdb.set_trace()
            exit(1)

        groups = result.groups()
        elems.append([int(groups[0]), int(groups[1]), groups[2], groups[3]])

    return elems

def validate(min, max, letter, password):
    count = Counter(password)
    return min <= count[letter] <= max

def part_a():
    elems = get_input()

    counter = 0

    for elem in elems:
        if validate(*elem):
            counter += 1

    print(counter)

def part_b():
    elems = get_input()

    counter = 0
    for elem in elems:
        left, right, value, pwd = elem
        if (pwd[left-1] == value and pwd[right-1] != value) or (pwd[right-1] == value and pwd[left-1] != value):
            counter += 1

    print(counter)


if __name__ == "__main__":
    part_a()
    part_b()
