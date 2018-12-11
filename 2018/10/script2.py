
if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    entries = [int(x) for x in lines[0].split(' ')]

    def get_nodes(index):
        children = entries[index]
        metadata_count = entries[index + 1]
        index += 2

        child_values = []
        for _ in range(children):
            index, child_value = get_nodes(index)
            child_values.append(child_value)

        metadata = entries[index:index + metadata_count]
        if not child_values:
            node_value = sum(metadata)
        else:
            node_value = 0
            child_indexes = [x for x in metadata if x < len(child_values) + 1]
            for child_index in child_indexes:
                node_value += child_values[child_index - 1]


        index += metadata_count
        return index, node_value

    index, total_value = get_nodes(0)

    print(f'The sum is: {total_value}')
