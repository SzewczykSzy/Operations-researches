import numpy as np


def dynamics(count, weight, limit, q):
    matrix = np.zeros((limit+1, len(count)*2))  # stworzenie macierzy potrzebnej na  x_i  i  f_i(y_i)
    for i in range(limit + 1):
        for j in range(1, len(count)*2, 2):
            matrix[i][j] = np.inf   # w miejscach f_i(y_i) wpisuję nieskończoność (aby później podczas szukania minimum
            # nadpisywać tą wartość
    for j in range(len(count)):     # iteracja po wszystkich elemenrach w macierzy
        for i in range(limit + 1):
            act_index = len(weight) - j - 1     # inicjalizacja indeksu, aby odnosić sie od końca 'weight' i 'count'

            max_num_of_items = int(i / weight[act_index])      # maksymalna ilość przedmiotów
            if max_num_of_items > count[act_index]:
                max_num_of_items = count[act_index]
            if j == 0:      # warunek na wpisanie pierwszej i drugiel kolumny (pierwszy etap)
                matrix[i][j*2] = max_num_of_items
                matrix[i][(j*2)+1] = q[max_num_of_items][act_index]
            else:           # po pierwszych dwóch kolumnach
                for poss_max_num in range(max_num_of_items + 1):  # iteracja po wszystkich możliwych ilościach
                    # przedmiotów
                    cost = q[poss_max_num][act_index] + matrix[i-weight[act_index]*poss_max_num][(j*2)-1]   # obliczenie
                    # kosztu
                    if cost < matrix[i][(j*2) + 1]:  # wrunek sprawdzający, czy nowy koszt jest mniejszy od poprzedniego
                        matrix[i][j*2] = poss_max_num
                        matrix[i][(j*2)+1] = cost
    return matrix


def get_path(matrix, weight, limit, q):
    path = []
    free_space = limit
    for j in range(len(weight)-1, -1, -1):
        act_index = len(weight) - j - 1
        path.append("{0}:x{1}".format(int(matrix[free_space][j*2]), act_index))
        free_space = int(free_space - weight[act_index]*matrix[free_space][j*2])
    return path


def main():
    count = [6, 3, 2]
    weight = [1, 2, 3]
    limit = 7
    q = [[20, 9, 6],
         [18, 6, 2],
         [14, 3, 0],
         [11, 0, 0],
         [7, 0, 0],
         [2, 0, 0],
         [0, 0, 0]]
    matrix = dynamics(count, weight, limit, q)
    print(dynamics(count, weight, limit, q))
    print(get_path(matrix, weight, limit, q))

    # count = [1, 7, 3, 8, 9, 8, 3, 3, 5, 6]
    # weight = [7, 8, 9, 5, 7, 3, 5, 7, 8, 11]
    # limit = 45
    # q = [[54, 50, 49, 47, 45, 34, 13, 8, 5, 4],
    #      [34, 27, 35, 40, 33, 20,  4, 7, 2, 3],
    #      [20, 16, 27, 35, 29, 12,  2, 6, 1, 0],
    #      [17, 11, 22, 33, 17,  1,  0, 5, 0, 0],
    #      [13,  9, 11, 30,  9,  0,  0, 4, 0, 0],
    #      [10,  3,  1, 27,  1,  0,  0, 2, 0, 0],
    #      [8,   2,  0, 15,  0,  0,  0, 1, 0, 0],
    #      [4,   0,  0, 11,  0,  0,  0, 0, 0, 0],
    #      [3,   0,  0,  6,  0,  0,  0, 0, 0, 0],
    #      [0,   0,  0,  0,  0,  0,  0, 0, 0, 0]]
    # matrix = dynamics(count, weight, limit, q)
    # print(dynamics(count, weight, limit, q))
    # print(get_path(matrix, weight, limit, q))


if __name__ == '__main__':
    main()
