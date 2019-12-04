
if __name__ == '__main__':
    range_start = 146810
    range_end = 612564

    def check_adjecent_numbers(number):
        number = str(number)
        for i in range(0, len(number) - 1):
            if number[i] == number[i + 1] and (
                    (i - 1 < 0 or number[i - 1] != number[i])
                    and (i + 2 >= len(number) or number[i + 2] != number[i])
            ):
                return True

        return False

    def check_incrementing_numbers(number):
        number = str(number)
        for i in range(0, len(number) - 1):
            if number[i + 1] < number[i]:
                return False

        return True

    # check_adjecent_numbers(567778)
    numbers = []
    for i in range(range_start, range_end + 1):
        if check_adjecent_numbers(i) and check_incrementing_numbers(i):
            numbers.append(i)

    print('\n'.join([str(number) for number in numbers]))
    print(f'Total numbers: {len(numbers)}')
