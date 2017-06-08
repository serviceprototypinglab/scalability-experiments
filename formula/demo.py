from array import array

from formula import rate_fastest_md

from formula import index_to_number_replicas


def demo():
    price_stateless = 0.25
    price_stateful = 1.0 / 12
    prices = [price_stateless, price_stateful]
    max_performance = 45.0
    max_c = 0.8
    rate1 = 1.06
    # rate2 = 1.2
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

    a = rate_fastest_md(matrix_1, prices, max_performance, max_c, rate1)
    res = index_to_number_replicas(a)
    print "cost               |  makespan         | (stateless, stateful)"
    print res


print "------------"
demo()
print "------------"
