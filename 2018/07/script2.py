import re
import string
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

        dependencies[posterior].add(prior)
        dependencies[prior]

    def task_time(task_id):
        return 60 + string.ascii_uppercase.index(task_id) + 1


    worker_steps = []
    worker_times = []
    steps = []
    timer = 0

    while dependencies:
        # Find all steps whose dependencies are completed
        possible_steps = [step for step, dependency_set in dependencies.items()
                          if len(dependency_set) == 0 and step not in set(worker_steps)]

        # Assign steps to work on as long as there's workers available.
        while len(worker_steps) <= 5 and len(possible_steps) > 0:
            next_worker = len(worker_steps)
            worker_step = possible_steps[0]
            del possible_steps[0]

            worker_steps.append(worker_step)
            worker_times.append(task_time(worker_step))

        # Run the timer until a step is complete.
        done_indexes = []
        while not done_indexes:
            timer += 1
            for i in range(len(worker_times)):
                worker_times[i] -= 1
                if worker_times[i] == 0:
                    done_indexes.append(i)

        done_steps = [worker_steps[step_id] for step_id in done_indexes]
        for i in done_indexes:
            del worker_steps[i]
            del worker_times[i]

        # Update dependencies.
        for done_step in done_steps:
            del dependencies[done_step]
            for step, dependency_set in dependencies.items():
                dependencies[step] = dependency_set.difference({done_step})

    print(f'The total assembly time is: {timer}')
