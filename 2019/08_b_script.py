from collections import Counter

if __name__ == '__main__':
    with open("08_a_input.txt", "r") as file:
        lines = [line for line in file.read().split('\n') if line][0]

    width = 25
    height = 6
    size = width * height
    output = []

    # lines = '0222112222120000'
    # size = 4

    for i in range(0, size):
        for j in range(0, int(len(lines)/size)):
            if lines[i + j*size] != '2':
                # print(f'{i}, {j}')
                break

        output.append(lines[i + j*size])

    for i in range(0, height):
        print(''.join(output[i*width: (i+1)*width]).replace('0', ' '))


    # for i in range(0, int(len(lines)/size)):
    #     print(lines[i*size:(i+1) * size].replace('2', ' '))