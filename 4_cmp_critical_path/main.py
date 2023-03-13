import numpy as np
from math import inf


class Event:    # klasa odwzorowywyjąca zdarzenie
    def __init__(self, index, t_omega=None, t_p=None):
        self.index = index      # nowy indek
        self.T_omega = t_omega      # najwcześniejszy możliwy termin wystąpienia zdarzenia
        self.T_p = t_p      # najpóźniejszy możliwy termin wystąpienia zdarzenia


class CPM:
    def __init__(self, graph):
        self.graph = graph      # graf wejściowy
        self.bin_mat = []       # macierz binarna grafu
        self.list_idx = []      # lista potrzebna do wyznaczenia nowych indeksów zdarzeń
        self.omega_0 = {}       # słownik posiadający składnię: {origin_idx : (new_idx, T_omega, T_p)},
        # gdzie origin_idx to indeks zdarzenia w oryginalnym grafie, a new_idx to nowy indeks zdarzenia
        self.crit_path = []     # lista zawierająca krawędzie ścieżki krytycznej
        self.total_cost = 0     # całkowity maksymalny koszt ścieżki kryrtcznej

    def binary_matrix(self):    # Utworzenie macierzy binarnej dla macierzy sąsiedztwa "graph" reprezentującej graf
        self.print_graph(self.graph)
        self.list_idx = []
        for i, el in enumerate(self.graph):
            self.bin_mat.append([])
            self.list_idx.append(i)
            for j in el:
                if j == 0:
                    self.bin_mat[i].append(0)
                else:
                    self.bin_mat[i].append(1)
        self.print_graph(self.bin_mat)

    def index_events(self):     # Indeksowanie w odpowiedniej kolejności zdarzeń (rosnąco od początku grafu)
        trans_bin_matrix = [[self.bin_mat[j][i] for j in range(len(self.bin_mat))] for i in range(len(self.bin_mat[0]))]
        # utworzenie transpozycji, aby łatwiej odnosić się do jej elemantów
        count = 0   # zmienna odpowiedzialna za kolejne indeksy zdarzeń
        while len(self.list_idx) > 0:
            for i, el in enumerate(trans_bin_matrix):
                if any(el) != 0:
                    continue
                else:
                    self.omega_0[self.list_idx.pop(i)] = Event(count)
                    trans_bin_matrix.pop(i)
                    for j in range(len(self.list_idx)):
                        trans_bin_matrix[j].pop(i)
                    count += 1
                    break
        self.print_omega()

    def term_index(self):   # funkcja odpowiedzialna za wyznaczenie najwcześniejszego możliwego terminu i
        # najpóźniejszego możliwego terminu wystąpienia zdarzenia
        for origin_idx, elem in self.omega_0.items():   # iterowanie po kelejnych elemantach zbioru "T_omega"
            if elem.index == 0:
                elem.T_omega = 0
            else:
                maxi = 0
                for i in range(len(self.graph)):
                    if self.graph[i][origin_idx] != 0:
                        if self.graph[i][origin_idx] + self.omega_0[i].T_omega > maxi:
                            maxi = self.graph[i][origin_idx] + self.omega_0[i].T_omega
                elem.T_omega = maxi
        self.print_omega_1()

        reversed_omega = dict(reversed(list(self.omega_0.items())))    # zmienna z odwrotną kolejnośćie względem omega_0
        for origin_idx, elem in reversed_omega.items():     # iterowanie po kelejnych elemantach zbioru "T_omega",
            # w odwrotnej kolejności - w celu wyznaczenia zbioru "T_p"
            if elem.index == len(self.omega_0) - 1:
                elem.T_p = elem.T_omega
            else:
                pass
                mini = inf
                for i in range(len(self.graph)):
                    if self.graph[origin_idx][i] != 0:
                        if reversed_omega[i].T_p - self.graph[origin_idx][i] < mini:
                            mini = reversed_omega[i].T_p - self.graph[origin_idx][i]
                elem.T_p = mini
        self.omega_0 = dict(reversed(list(reversed_omega.items())))
        self.print_omega_1()

    def critical_path(self):    # wyznacznie ścieżki kryrtycznej i maksymalnego kosztu
        for origin_idx, elem in self.omega_0.items():
            for i in range(len(self.graph)):
                if self.graph[origin_idx][i] != 0:
                    if self.omega_0[i].T_p - self.graph[origin_idx][i] == self.omega_0[origin_idx].T_omega:
                        self.crit_path.append((origin_idx, i))
            if elem.T_omega > self.total_cost:
                self.total_cost = elem.T_omega
        print(self.crit_path)
        print(self.total_cost)

    def print_graph(self, graph):
        for i in graph:
            print(i)
        print(" ")

    def print_omega(self):
        print("{", end="")
        for key, val in self.omega_0.items():
            print("{0}:{1}".format(key, val.index), end=", ")
        print("}\n")

    def print_omega_1(self):
        print("{", end="")
        for key, val in self.omega_0.items():
            print("{0}:({1}, {2}, {3})".format(key, val.index, val.T_omega, val.T_p), end=", ")
        print("}\n")

    def print_rev_omega_1(self):
        print("{", end="")
        for key, val in self.omega_0.items():
            print("{0}:({1}, {2}, {3})".format(key, val.index, val.T_omega, val.T_p), end=", ")
        print("}\n")


def main():
    graf_1 = [
        [0, 0, 0, 3, 0, 0],
        [2, 0, 4, 0, 6, 0],
        [4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0],
        [0, 4, 2, 0, 0, 0]
    ]
    graf_2 = [
        [0, 5, 9, 12, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 1, 2, 0],
        [0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    graf_3 = [
        [0, 8, 4, 2, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0],
        [0, 0, 0, 0, 0, 13, 0],
        [0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    graf = [
    #    0  1  2  3  4  5  6  7  8  9  10
        [0, 7, 0, 0, 0, 0, 3, 0, 4, 9, 0], # 0
        [0, 0, 0, 7, 8, 0, 0, 0, 0, 3, 0], # 1
        [0, 5, 0, 0, 2, 0, 0, 0, 0, 0, 0], # 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6], # 3
        [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0], # 4
        [0, 3, 1, 0, 0, 0, 0, 6, 0, 0, 0], # 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], # 6
        [5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7], # 8
        [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4], # 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 10
    ]
    A = CPM(graf)
    A.binary_matrix()
    A.index_events()
    A.term_index()
    A.critical_path()


if __name__ == "__main__":
    main()