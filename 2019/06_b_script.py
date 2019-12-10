from collections import deque

class Orbit(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.depth = 0 if parent == None else parent.depth + 1
        self.san_depth = None

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

    san_parent = orbits['SAN'].parent
    orbits[san_parent.name].san_depth = 0


    queue = deque([san_parent.name])
    processed = set()

    while queue:
        item = queue.popleft()
        print(f'processing: {item}')

        current = orbits[item]
        # find children
        children = [x.name for x in orbits.values() if x.parent and x.parent.name == item]
        for child in children:
            if child not in processed:
                processed.add(child)
                queue.append(child)
                orbits[child].san_depth = current.san_depth + 1
        # find parent
        if current.parent and current.parent.name not in processed:
            processed.add(current.parent.name)
            queue.append(current.parent.name)
            orbits[current.parent.name].san_depth = current.san_depth + 1

    you_parent = orbits[orbits['YOU'].parent.name]
    print(f'Jumps required: {you_parent.san_depth}')
