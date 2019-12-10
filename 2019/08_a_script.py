from collections import Counter

if __name__ == '__main__':
    with open("08_a_input.txt", "r") as file:
        lines = [line for line in file.read().split('\n') if line][0]

    width = 25
    height = 6
    size = width * height
    min_zeros = Counter('0' * size)

    for i in range(0, int(len(lines)/size)):
        layer = lines[i*size: (i+1) * size]
        count = Counter(layer)
        if count['0'] < min_zeros['0']:
            min_zeros = count

    print(f'result is: {min_zeros["2"] * min_zeros["1"]}')
