def get_input():
    with open("01_a_input.txt","r") as file:
        lines = file.read().split('\n')

    elems = [int(x) for x in lines if x]

    return elems

def part_a():
    elems = get_input()

    elem_set = set(elems)

    for elem in elems:
        rest = 2020 - elem
        if rest in elem_set:
            print(rest * elem)


def part_b():
    elems = get_input()

    elem_set = set(elems)

    for i in range(len(elems)):
        first = elems[i]
        for j in range(i+1, len(elems)):
            second = elems[j]
            third = 2020 - first - second
            if third in elem_set:
                print(first * second * third)

if __name__ == "__main__":
    part_a()
    part_b()
