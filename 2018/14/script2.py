from datetime import datetime


if __name__ == '__main__':
    puzzle_input = '824501'

    recipes = [3, 7]
    first_ix = 0
    second_ix = 1

    def print_recipes():
        current = []
        for j in range(len(recipes)):
            if j == first_ix:
                current.append(f'({recipes[j]})')
            elif j == second_ix:
                current.append(f'[{recipes[j]}]')
            else:
                current.append(str(recipes[j]))

        print(' '.join(current))

    last_ix = 0
    while True:
        new_recipe = recipes[first_ix] + recipes[second_ix]

        if new_recipe // 10 != 0:
            recipes.append(new_recipe // 10)
        recipes.append(new_recipe % 10)

        recipes_str = ''.join([str(x) for x in recipes[last_ix:]])
        target_ix = recipes_str.find(puzzle_input)
        if target_ix != -1:
            print(target_ix + last_ix)
            break

        last_ix = max(len(recipes) - len(puzzle_input), 0)
        first_ix = (first_ix + 1 + recipes[first_ix]) % len(recipes)
        second_ix = (second_ix + 1 + recipes[second_ix]) % len(recipes)

