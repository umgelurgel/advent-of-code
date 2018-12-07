import re
from collections import defaultdict


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    regex_str = r'^Step (?P<prior>\w) must be finished before step (?P<posterior>\w) can begin\.'
    regex = re.compile(regex_str)

    dependencies = defaultdict(set)
    for line in lines:
        match_group = regex.match(line).groupdict()
        prior = match_group['prior']
        posterior = match_group['posterior']

        dependencies[prior].add(posterior)
        dependencies[posterior]

    steps = []
    while dependencies:
        # Find all steps whose dependencies are completed
        possible_steps = [step for step, dependency_set in dependencies.items() if len(dependency_set) == 0]
        # Select the lowest step alphabetically
        next_step = sorted(possible_steps)[0]
        steps.append(next_step)

        # Remove the step from the dict and update all remaining dependencies
        del dependencies[next_step]
        for step, dependency_set in dependencies.items():
            dependencies[step] = dependency_set.difference({next_step})

    print(f'The step list is: {"".join(steps)}')
