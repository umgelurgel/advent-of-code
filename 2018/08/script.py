
if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    entries = [int(x) for x in lines[0].split(' ')]
    # entries = [int(x) for x in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split(' ')]
    metadata_sum = 0

    def get_nodes(index):
        global metadata_sum

        children = entries[index]
        metadata_count = entries[index + 1]
        index += 2

        for _ in range(children):
            index = get_nodes(index)

        metadata = entries[index:index + metadata_count]
        metadata_sum += sum(metadata)
        index += metadata_count
        return index

    get_nodes(index=0)

    print(f'The sum is: {metadata_sum}')

