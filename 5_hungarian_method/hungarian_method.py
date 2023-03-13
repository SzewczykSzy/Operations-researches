import numpy as np
from copy import deepcopy


class CostMatrix:
    def __init__(self, matrix: np.ndarray):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Zle wymiary")
        self.matrix = matrix
        self.base_cost_matrix = deepcopy(self.matrix)
        self.size = len(matrix)
        self.phi = 0
        self.list_index_independent = []
        self.list_index_dependent = []
        self.list_index_rows = []
        self.list_index_cols = []
        self.dict_of_rows = {}
        self.dict_of_cols = {}
        self.x_lines = []
        self.y_lines = []

    def reduce_matrix_rows(self):
        for id, el in enumerate(self.matrix):
            self.phi += min(el)
            self.matrix[id] -= min(el)

    def reduce_matrix_cols(self):
        self.matrix = self.matrix.T
        self.reduce_matrix_rows()
        self.matrix = self.matrix.T

    def find_zeros(self):
        rows = [x for x in range(self.size)]
        cols = deepcopy(rows)
        list_index_rows = []
        list_index_cols = []
        self.list_index_independent = []
        self.list_index_dependent = []
        # znalezienie wszytskcih zer
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    list_index_rows.append(i)
                    list_index_cols.append(j)
                    if (i, j) not in self.list_index_dependent:
                        self.list_index_dependent.append((i, j))
        # #utworzenie słownika wiersz / kolumna : ilość zer
        dict_of_rows = {}
        dict_of_cols = {}
        for i in range(self.size):
            dict_of_rows[i] = list_index_rows.count(i)
            dict_of_cols[i] = list_index_cols.count(i)
        # posortowanie wdg ilości zer rosnąco
        dict_of_rows = dict(sorted(dict_of_rows.items(), key=lambda x: x[1], reverse=False))
        dict_of_cols = dict(sorted(dict_of_cols.items(), key=lambda x: x[1], reverse=False))
        sorted_rows = list(dict_of_rows.keys())
        sorted_cols = list(dict_of_cols.keys())
        # według listy wszytstkich zer wyzanczenie zer niezależnych
        for i in sorted_rows:
            for j in sorted_cols:
                if (i, j) in self.list_index_dependent and i in rows and j in cols:
                    self.list_index_dependent.remove((i, j))
                    if (i, j) not in self.list_index_independent:
                        self.list_index_independent.append((i, j))
                    rows.remove(i)
                    cols.remove(j)

    def result(self):
        self.reduce_matrix_rows()
        self.reduce_matrix_cols()
        while True:
            print(self.matrix, " ")
            self.find_zeros()
            if len(self.list_index_independent) == self.size:
                print("Macierz początkowa")
                print(self.base_cost_matrix)
                print("Macierz zredukowana")
                print(self.matrix)
                print("Dolne ograniczenie kosztu")
                print(self.phi)
                print("Wspólrzędne zer niezależnych")
                print(self.list_index_independent)
                x = np.zeros((self.size, self.size))
                for i in range(self.size):
                    for j in range(self.size):
                        if (i, j) in self.list_index_independent:
                            x[i][j] = 1
                print("macierz rozwiązania")
                print(x)
                print("przydział zadań")
                re = x * self.base_cost_matrix
                print(re)
                print("Koszt rozwiązania")
                print(np.sum(re))
                break
            self.minimal_line()
            self.new_independent_zeros()

    def minimal_line(self):
        list_idx = [i for i in range(self.size)]    # lista z wszystkimi indeksami macierzy

        list_x_idx_und = []  # lista wierszy posiadających niezależne zera
        for idx, el in enumerate(self.list_index_independent):
            list_x_idx_und.append(el[0])

        for i, el in enumerate(list_idx):   # dodanie wierszy do zaznaczonych (oznaczenie)
            if el not in list_x_idx_und:
                self.x_lines.append(el)

        for i, el in enumerate(self.x_lines):   # dodanie kolumn do zaznaczonych (oznaczenie)
            list_y_idx_dep = []  # lista kolumn posiadających zależne zera, dla listy wierszy posiadających
            # niezależne zera
            for idx, elem in enumerate(self.list_index_dependent):
                if el == elem[0]:
                    list_y_idx_dep.append(elem[1])
            if el in list_y_idx_dep:
                self.y_lines.append(el)

        for i, el in enumerate(self.y_lines):
            list_x_idx = []  # lista wierszy mających w oznakowanych kolumnach niezależne zero
            for idx, elem in enumerate(self.list_index_independent):    # dodanie wierszy do niezależnych
                if el == elem[1]:
                    if elem[0] not in self.x_lines:
                        self.x_lines.append(elem[0])

    def new_independent_zeros(self):
        mini = np.inf
        for i, el in enumerate(self.x_lines):   # Wyznaczenie najmniejszej wartości w nieoznaczonych liniach
            for j in range(self.size):
                if j not in self.y_lines:
                    if self.matrix[el][j] < mini:
                        mini = self.matrix[el][j]
        for i, el in enumerate(self.x_lines):   # odjęcie od niezaznaczonych lini najmniejszej wyznaczonej wartosci
            for j in range(self.size):
                if j not in self.y_lines:
                    self.matrix[el][j] -= mini
        self.phi += mini    # zwiększenie wartości o krotność elementu minimalnego

        list_idx = [i for i in range(self.size)]
        x_cross = []
        for i in list_idx:      # wyznacznie punktów przecięcia lini (miejsce spotkania dwóch lini)
            if i not in self.x_lines:
                x_cross.append(i)

        for i in x_cross:   # dodanie do wyznaczonych punktów, minimalnej wartości
            for j in self.y_lines:
                self.matrix[i][j] += mini

    def __str__(self):
        result = ""
        for el in self.matrix:
            result += str(el) + "\n"
        return result


def main():
    matrix = np.array([[5, 2, 3, 2, 7, 6],
                         [6, 8, 4, 2, 5, 9],
                         [6, 4, 3, 7, 2, 5],
                         [6, 9, 0, 4, 0, 3],
                         [4, 1, 2, 4, 0, 6],
                         [3, 7, 9, 4, 1, 5]])
    A = CostMatrix(matrix)
    A.result()


if __name__ == "__main__":
    main()