import random

if __name__ == '__main__':
    with open("16_input.txt","r") as file:
        lines = file.read().split('\n')[0]

    def get_digit_pattern(init_pattern, digit, length):
        # Repeat each number in the patter n times, skip the first entry
        list_of_lists = [[x] * (digit + 1) for x in init_pattern]
        flat_list = [x for sublist in list_of_lists for x in sublist]
        result_list = list(flat_list)
        while len(result_list) < length + 1:
            result_list.extend(flat_list)
        return result_list[1:length+1]

    base_pattern = [0, 1, 0, -1]



    numbers = [int(x) for x in list(lines)]
    phase = 0

    digit_patterns = {
        i: get_digit_pattern(init_pattern=base_pattern, digit=i, length=len(numbers)) for i in range(len(numbers))
    }

    while phase < 100:
        new_numbers = []

        for i in range(len(numbers)):
            number = 0
            for j in range(len(numbers)):
                # print(f'{i}, {j}: {numbers[j]} * {digit_patterns[i][j]}')
                number += numbers[j] * digit_patterns[i][j]

            # print(f'sum {i}, {j}: {abs(number) % 10}')
            new_numbers.append(abs(number) % 10)

        numbers = new_numbers
        phase += 1
        print(f'{phase}: {"".join([str(x) for x in numbers[:8]])}')
