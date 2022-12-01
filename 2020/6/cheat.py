with open("input.txt") as inputs:
    groups = [line for line in inputs.read()[:-1].split("\n\n")]

solution = 0

for group in groups:
    yes = False

    for person in group.split("\n"):
        if yes is not False:
            yes = yes & set(person)
        else:
            yes = set(person)

    solution += len(yes)

print(solution)
