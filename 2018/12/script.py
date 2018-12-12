from datetime import datetime

if __name__ == '__main__':
    # with open("input.txt", "r") as file:
    with open("test_input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    initial_state = lines[0].replace('initial state: ', '')

    plant_states = set([line.split(' => ')[0] for line in lines[1:] if line.split(' => ')[1] == '#'])
    left_pad = max([x.find('#') for x in plant_states])
    right_pad = max([4 - x.rfind('#') for x in plant_states])
    state = '.' * left_pad + initial_state + '.' * right_pad  # add empty plants in the beginning
    pot_zero_ix = left_pad

    # generation_count = 50000000000
    generation_count = 20
    for gen_ix in range(generation_count):
        print(f'{str(gen_ix).zfill(2)}: {state}')
        # if gen_ix % 1_000 == 0:
        #     print(f'{datetime.now()}: {gen_ix}: {len(state)}')

        new_state = '..'
        for i in range(2, len(state) - 2):
            if state[i-2: i+3] in plant_states:
                i_state = '#'
            else:
                i_state = '.'

            new_state += i_state

        last_plant_ix = new_state.rfind('#')
        last_plant_till_end = len(new_state) - last_plant_ix
        if last_plant_till_end < right_pad:
            new_state += '.' * (right_pad - last_plant_till_end + 1)

        first_plant_ix = new_state.find('#')
        if first_plant_ix < left_pad:
            len_before = len(new_state)

            new_state = '.' * (left_pad - first_plant_ix) + new_state

            len_diff = len(new_state) - len_before
            pot_zero_ix += len_diff
        elif first_plant_ix > left_pad + 1:
            len_diff = first_plant_ix - left_pad
            new_state = new_state[len_diff:]
            pot_zero_ix -= len_diff

        state = new_state

    print(f'{str(gen_ix + 1).zfill(2)}: {state}')

    counter = 0
    for i in range(len(state)):
        if state[i] == '#':
            counter += i - pot_zero_ix

    print(f'Sum of plant pot ixs: {counter}')
