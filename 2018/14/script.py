from datetime import datetime

if __name__ == '__main__':
    puzzle_input = 824501

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

    while len(recipes) < puzzle_input + 10:
        new_recipe = recipes[first_ix] + recipes[second_ix]

        if new_recipe // 10 != 0:
            recipes.append(new_recipe // 10)
        recipes.append(new_recipe % 10)

        first_ix = (first_ix + 1 + recipes[first_ix]) % len(recipes)
        second_ix = (second_ix + 1 + recipes[second_ix]) % len(recipes)

    start_ix = puzzle_input
    result = ''.join([str(x) for x in recipes[start_ix:start_ix+10]])
    print(result)
