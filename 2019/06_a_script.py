from collections import deque

class Orbit(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1

if __name__ == '__main__':
    with open("06_a_input.txt", "r") as file:
        lines = [line for line in file.read().split('\n') if line]

    orbits = {
        'COM': Orbit(name='COM', parent=None)
    }

    queue = deque(lines)

    while queue:
        item = queue.popleft()
        print(f'processing: {item}')
        inner, outer = item.split(')')

        if inner not in orbits:
            queue.append(item)
        else:
            orbits[outer] = Orbit(name=outer, parent=orbits[inner])

    total = sum([x.depth for x in orbits.values()])
    print(f'total is {total}')