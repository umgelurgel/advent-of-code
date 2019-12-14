from collections import deque
from math import ceil

if __name__ == '__main__':
    with open("14_input.txt","r") as file:
        lines = [line for line in file.read().split('\n') if line]

    reactions = {}

    for line in lines:
        inputs, output = line.split(' => ')

        chemicals = []
        for value in inputs.split(','):
            quantity, chemical = value.strip().split(' ')
            chemicals.append((int(quantity), chemical))

        quantity, chemical = output.strip().split(' ')

        reactions[chemical] = {
            'inputs': chemicals,
            'quantity': int(quantity),
        }

    def consolidate(resources):
        new_resources = deque()

        # reduce resources
        quantities_required = {}
        for quantity, resource in resources:
            if resource not in quantities_required:
                quantities_required[resource] = quantity
            else:
                quantities_required[resource] += quantity

        for key,value in quantities_required.items():
            new_resources.append((value, key))

        return new_resources

    resources = deque([tuple([1, 'FUEL'])])
    # resources = deque([tuple([7, 'A'])])
    resource_cache = {}
    ore_required = 0
    basic_resources = []
    totals = {}

    while resources:
        print(f'Resources: {resources}')
        print(f'Cache: {resource_cache}')
        print(f'Ore so far: {ore_required}')
        print('')
        required_quantity, resource = resources.popleft()
        entry = reactions[resource]

        # check if we have any of the resource in the cache
        if resource in resource_cache:
            reduce_by = min(resource_cache[resource], required_quantity)
            required_quantity -= reduce_by
            resource_cache[resource] -= reduce_by

        reaction_quantity = entry['quantity']
        reaction_count = ceil(required_quantity / reaction_quantity)

        produced_quantity = reaction_count * reaction_quantity
        if produced_quantity > required_quantity:
            resource_cache[resource] = resource_cache.get(resource, 0) + produced_quantity - required_quantity

        for input in entry['inputs']:
            in_quantity, in_chemical = input

            if in_chemical == 'ORE':
                ore_required += in_quantity * reaction_count
            else:
                in_quantity_required = in_quantity * reaction_count

                if in_chemical in resource_cache:
                    reduce_by = min(resource_cache[in_chemical], in_quantity_required)
                    in_quantity_required -= reduce_by
                    resource_cache[in_chemical] -= reduce_by

                if in_quantity_required:
                    resources.append((in_quantity_required, in_chemical))
                    resources = consolidate(resources)

    print(ore_required)


