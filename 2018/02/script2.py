from collections import Counter

if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    for i, source_line in enumerate(lines):
        for target_line in lines[i:]:
            diff_positions = []
            for j in range(len(source_line)):
                if source_line[j] != target_line[j]:
                    diff_positions.append(j)

            if len(diff_positions) == 1:
                diff_index = diff_positions[0]
                print(source_line[:diff_index] + source_line[diff_index + 1:])
                exit()
