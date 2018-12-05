
if __name__ == '__main__':
    total = 0
    with open("input.txt","r") as file:
        lines = file.read().split('\n')

    int_lines = [int(x) for x in lines if x]

    found = False
    total = 0
    freqs = set([0])
    
    while not found:
        for x in int_lines:
            total += x
            if total in freqs:
                print(f'Freq is {total}')
                found = True
                break
            else:
                freqs.add(total)
                
