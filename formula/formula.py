from numpy import array, ndenumerate
import operator

# 2 D


def get_cost(i, j, p):
    return (i + 1) * p[0] + (j + 1) * p[1]


def fastest(p_matrix, prices, max_p, max_cost):
    res = [-1, -1]
    aux_min = -1
    for i in range(0, len(p_matrix)):
        for j in range(0, len(p_matrix[i])):
            if (p_matrix[i][j] <= aux_min or aux_min == -1) and p_matrix[i][j] <= max_p and get_cost(i, j,
                                                                                                     prices) <= max_cost:
                if p_matrix[i][j] == aux_min:
                    if get_cost(i, j, prices) < get_cost(res[0], res[1], prices):
                        res = [i, j]
                        aux_min = p_matrix[i][j]
                else:
                    res = [i, j]
                    aux_min = p_matrix[i][j]

    if get_cost(res[0], res[1], prices) <= max_cost and p_matrix[res[0]][res[1]] <= max_p:
        return res
    else:
        return [-1, -1]


def cheapest(p_matrix, prices, max_p, max_cost):
    res = [-1]
    aux_min_cost = -1
    for i in range(0, len(p_matrix)):
        for j in range(0, len(p_matrix[i])):
            if (get_cost(i, j, prices) < aux_min_cost or aux_min_cost == -1) and p_matrix[i][j] <= max_p and get_cost(i,
                                                                                                                      j,
                                                                                                                      prices) <= max_cost:
                res = [i, j]
                aux_min_cost = get_cost(i, j, prices)
    if get_cost(res[0], res[1], prices) <= max_cost and p_matrix[res[0]][res[1]] <= max_p:
        return res
    else:
        return [-1, -1]


def rate_fastest(p_matrix, prices, max_p, max_cost, rate):
    res = []
    fastest1 = fastest(p_matrix, prices, max_p, max_cost)
    value_fastest = p_matrix[fastest1[0]][fastest1[1]]
    for i in range(0, len(p_matrix)):
        for j in range(0, len(p_matrix[i])):
            d = p_matrix[i][j] / value_fastest
            if d <= rate:
                if get_cost(i, j, prices) < max_cost:
                    a2 = (get_cost(i, j, prices), p_matrix[i][j], i, j)
                    res.append(a2)
    res = sorted(res, key=lambda a1: a1[0])
    return res


def rate_cheapest(p_matrix, prices, max_p, max_cost, rate):
    res = []
    cheapest1 = cheapest(p_matrix, prices, max_p, max_cost)
    value_cheapest = get_cost(cheapest1[0], cheapest1[1], prices)
    for i in range(0, len(p_matrix)):
        for j in range(0, len(p_matrix[i])):
            d = get_cost(i, j, prices) / value_cheapest
            if d <= rate:
                if p_matrix[i][j] < max_p:
                    a2 = (get_cost(i, j, prices), p_matrix[i][j], i, j)
                    res.append(a2)
    res = sorted(res, key=lambda a1: a1[1])
    return res


def formula(p_matrix, prices, max_p, max_cost, rate, policy):
    if policy == 'cheapest':
        return rate_cheapest(p_matrix, prices, max_p, max_cost, rate)
    elif policy == 'fastest':
        return rate_fastest(p_matrix, prices, max_p, max_cost, rate)
    else:
        return rate_fastest(p_matrix, prices, max_p, max_cost, rate)

# MD


def get_cost_md(index_matrix, p):
    cost = 0
    for i in range(0, len(index_matrix)):
        cost += ((index_matrix[i] + 1)*p[i])
    return cost


def fastest_md(p_matrix, prices, max_p, max_cost):
    res = (-1)
    aux_min = -1
    for index_matrix, value in ndenumerate(p_matrix):
        if (p_matrix[index_matrix] <= aux_min or aux_min == -1)\
                and p_matrix[index_matrix] <= max_p\
                and get_cost_md(index_matrix, prices) <= max_cost:
            aux_min = p_matrix[index_matrix]
            res = index_matrix
    if p_matrix[res] <= max_p \
            and get_cost_md(res, prices) <= max_cost:
        return res
    return res


def cheapest_md(p_matrix, prices, max_p, max_cost):
    res = (-1)
    aux_min_cost = -1
    for index_matrix, value in ndenumerate(p_matrix):
        if (get_cost_md(index_matrix, prices) < aux_min_cost or aux_min_cost == -1) \
                and p_matrix[index_matrix] <= max_p \
                and get_cost_md(index_matrix, prices) <= max_cost:
            aux_min_cost = get_cost_md(index_matrix, prices)
            res = index_matrix
    if p_matrix[res] <= max_p \
            and get_cost_md(res, prices) <= max_cost:
        return res
    return res


def rate_cheapest_md(p_matrix, prices, max_p, max_cost, rate):
    res = []
    cheapest1 = cheapest_md(p_matrix, prices, max_p, max_cost)
    value_cheapest1 = p_matrix[cheapest1]
    for index, value in ndenumerate(p_matrix):
            d = get_cost_md(index, prices) / value_cheapest1
            if d <= rate:
                if p_matrix[index] < max_p:
                    a2 = (get_cost_md(index, prices), value, index)
                    res.append(a2)
    res = sorted(res, key=lambda a1: a1[1])
    return res


def rate_fastest_md(p_matrix, prices, max_p, max_cost, rate):
    res = []
    fastest1 = fastest_md(p_matrix, prices, max_p, max_cost)
    value_fastest = p_matrix[fastest1]
    for index, value in ndenumerate(p_matrix):
            d = p_matrix[index] / value_fastest
            if d <= rate:
                if get_cost_md(index, prices) < max_cost:
                    a2 = (get_cost_md(index, prices), value, index)
                    print a2
                    res.append(a2)
    res = sorted(res, key=lambda a1: a1[0])
    return res


def formula_md(p_matrix, prices, max_p, max_cost, rate, policy):
    if policy == 'cheapest':
        return rate_cheapest_md(p_matrix, prices, max_p, max_cost, rate)
    elif policy == 'fastest':
        return rate_fastest_md(p_matrix, prices, max_p, max_cost, rate)
    else:
        return rate_fastest_md(p_matrix, prices, max_p, max_cost, rate)


def print_example():
    price_stateless = 0.25
    price_stateful = 1.0 / 12
    max_performance = 45.0
    max_c = 0.8
    rate1 = 1.06
    rate2 = 1.2
    matrix_1 = array([
        [
            89.16724374,
            45.5318765193,
            43.7904612511,
            41.8832055032,
            42.0507290155,
            40.4489257663
        ],
        [
            71.6993230659,
            48.1122723985,
            40.0736481696,
            35.9154654562,
            36.0452770233,
            36.3544942796
        ]
    ])

    print "--------------"
    print "fastest"
    print fastest(matrix_1, [price_stateless, price_stateful], max_performance, max_c)

    print "--------------"
    print "cheapest"
    print cheapest(matrix_1, [price_stateless, price_stateful], max_performance, max_c)

    print "--------------"
    print "fastest with rate"
    res1 = rate_fastest(matrix_1, [price_stateless, price_stateful], max_performance, max_c, rate1)
    print "stateful | stateless | performance | price"
    for a in res1:
        print a

    print "--------------"
    print "cheapest with rate"
    res1 = rate_cheapest(matrix_1, [price_stateless, price_stateful], max_performance, max_c, rate2)
    print "stateful | stateless | performance | price"
    for a in res1:
        print a

    print "--------------"
    matrix_2 = array([
        [
            [
                89.16724374,
                45.5318765193,
                43.7904612511,
                41.8832055032,
                42.0507290155,
                40.4489257663
            ],
            [
                71.6993230659,
                48.1122723985,
                40.0736481696,
                35.9154654562,
                36.0452770233,
                36.3544942796
            ]
        ],
        [
            [
                189.16724374,
                145.5318765193,
                143.7904612511,
                141.8832055032,
                142.0507290155,
                140.4489257663
            ],
            [
                171.6993230659,
                148.1122723985,
                140.0736481696,
                135.9154654562,
                136.0452770233,
                136.3544942796
            ]
        ]
    ])
    matrix_1 = array([
        [
            89.16724374,
            45.5318765193,
            43.7904612511,
            41.8832055032,
            42.0507290155,
            40.4489257663
        ],
        [
            71.6993230659,
            48.1122723985,
            40.0736481696,
            35.9154654562,
            36.0452770233,
            36.3544942796
        ]
    ])
    prices1 = [1.1, 0.9, 1.0]
    print cheapest_md(matrix_2, prices1, 80, 8)
    print fastest_md(matrix_2, prices1, 80, 8)
    for a in rate_fastest_md(matrix_2, prices1, 80, 7, 1.2):
        print a
    for a in rate_cheapest_md(matrix_2, prices1, 43, 8, 1.2):
        print a


# TODO No tested
# ME
def solution_matrix(p_matrix, prices, max_p, max_cost):
    array_solutions = []
    for index_matrix, value in ndenumerate(p_matrix):
        array_solutions = []
        if value != -1:
            if value <= max_p:
                if get_cost_md(index_matrix, prices) <= max_cost:
                    array_solutions.append(index_matrix)
    return array_solutions


def me_cheapest_md(array_matrix, array_prices, array_performance, array_cost):
    solutions_index = []
    solutions_repetitions = []
    for i in range(0, len(array_matrix)):
        s = solution_matrix(array_matrix[i], array_prices, array_performance[i], array_cost[i])
        for j in s:
            if j in solutions_index:
                aux_i = solutions_index.index(j)
                solutions_repetitions[aux_i] += 1
            else:
                solutions_index.append(j)
                solutions_repetitions.append(1)
    index, value = max(enumerate(solutions_repetitions), key=operator.itemgetter(1))

    return solutions_index[index], value

