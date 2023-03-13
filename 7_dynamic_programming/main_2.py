import numpy as np


def dynamics(production_cost, storage_cost, month_demand, min_storage, max_storage, storage_start, storage_end):
    # production_cost - koszt produkcji;  storage_cost - koszt magazynowania;  month_demand - miesięczne zapotrzebowanie
    # na dany produkt;  min_storage - minimalna wypełnienie magazynu;  max_storage - maksymalne wypełnienie magazynu;
    # storage_start - początkowe wypełnienie magazynu;  storage_end - końcowe wypełniene magazynu

    poss_count = np.array([i for i in range(min_storage, max_storage + 1)])  # lista możliwych ilości przedmiotów
    matrix = np.zeros((max_storage - min_storage + 1, len(month_demand)*2))  # macierz potrzebna na  x_i  i  f_i(y_i)

    for i in range(max_storage - min_storage + 1):
        for j in range(1, len(month_demand)*2, 2):  # iterowanie po f_i(y_i) (funkcji celu) 'macierzy matrix'
            matrix[i][j] = np.inf  # wpisuję nieskończoność (aby później podczas szukania minimum nadpisywać tą wartość)

    for j in range(int(len(matrix[0])/2)):     # iteracja po wszystkich elementach w macierzy, aby poruszać się najpierw
        # kolumanmi
        for i in range(len(matrix)):
            act_index = int(len(matrix[0])/2) - j - 1  # inicjalizacja aktualnego indeksu (odrotnie względem 'j')

            if j == 0:      # warunek dla pierwszej i drugiel kolumny, wyznaczenie minimalnej i maksymalnej
                # dopuszczalnej produkcji
                product_min = storage_end + month_demand[act_index] - poss_count[i]
                product_max = storage_end + month_demand[act_index] - poss_count[i]

            else:           # analogicznie dla poprzedniego warunku, lecz dla kolejnych kolumn (etapów)
                product_min = max(min_storage + month_demand[act_index] - poss_count[i], 0)
                product_max = min(max_storage + month_demand[act_index] - poss_count[i], len(production_cost) - 1)

            if product_min > product_max or product_max < 0 or product_min < 0 or product_max > len(production_cost)- 1:
                # dla niespełnionych warunków, nadpisanie wartości, aby się nie pomylić
                matrix[i][j*2] = None
                matrix[i][(j*2)+1] = np.inf
                continue

            for poss_product in range(product_min, product_max + 1):  # iteracja po wszystkich możliwych produktach
                if j == 0:   # wyliczenie kosztu pierwszej kolumny
                    cost = production_cost[poss_product]
                else:      # wyliczenie kosztu dla wszystkich kolumn za wyjątkiem pierwszej
                    cost = production_cost[poss_product] + storage_cost[poss_count[i] + poss_product -\
                           month_demand[act_index] - min_storage] + matrix[poss_count[i] + poss_product - \
                           month_demand[act_index] - min_storage][j*2 - 1]

                if cost < matrix[i][j*2 + 1]:   # aktualizacja kosztu na mniejszy
                    matrix[i][j*2] = poss_product
                    matrix[i][j*2 + 1] = cost
    suma = matrix[storage_start - min_storage][-1]
    return matrix, suma


def get_path(month_demand, min_storage, storage_start, matrix):
    state = storage_start
    path = ""
    for j in range(int(len(matrix[0])/2) - 1, -1, -1):
        decision = int(matrix[state - min_storage][j*2])
        act_index = int(len(matrix[0])/2) - j - 1
        path += "y{0} = {1},  x{2} = {3}\n".format(act_index, state, act_index, decision)
        state = int(state + decision - month_demand[act_index])
    return path


def main():
    production_cost = np.array([0, 15, 18, 19, 20, 24])
    storage_cost = np.array([i * 2 for i in range(6)])
    month_demand = np.array([3, 3, 3, 3, 3, 3])
    min_storage = 0
    max_storage = 4
    storage_start = 0
    storage_end = 0

    production_cost = np.array([4, 7, 15, 17, 18, 26, 29, 38])
    storage_cost = np.array([1, 2, 4, 6, 8, 10])
    month_demand = np.array([3, 7, 8, 2, 4, 5, 6, 7, 2, 4, 1, 9])
    min_storage = 3
    max_storage = 8
    storage_start = 5
    storage_end = 2
    m, s = dynamics(production_cost, storage_cost, month_demand, min_storage, max_storage, storage_start, storage_end)
    # print(m)
    for i in m:
        print('[', end='')
        for j in i:
            print(j, ", ", end='')
        print(']')
    print("całkowity koszt: {0}".format(s))
    print("")
    print("strategia:")
    print(get_path(month_demand, min_storage, storage_start, m))


if __name__ == '__main__':
    main()
