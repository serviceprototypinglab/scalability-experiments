names_micro_services = ['stateless_search', 'stateless_crud', 'stateful_mongo']
# number_micro_services = [(0, 3), (0, 2), (1, 3)]
number_micro_services = [3, 2, 2]

index = [0, 0, 0]




s = 0
i = 0
while i < len(number_micro_services) - 1:
    while s < number_micro_services[i]:
        index[i] = s
        print index
        s += 1
    print "---"
    s = 0
    index[i] = 0
    if i < len(number_micro_services) - 1:
        if index[i + 1] < (number_micro_services[i + 1] - 1):
            index[i + 1] += 1
        else:
            index[i] = 0
            i += 1


