import math
import numpy as np

def greed(graph):
    edges_list = []
    cost_list = []
    V = []
    res = {}
    for i in range(len(graph)):     # utworzenie wektorów krawędzi, i odpowiadających im kosztów, oraz wierzchołków
        for j in range(len(graph)):
            if graph[i][j] != 0:
                edges_list.append((i, j))
                cost_list.append(graph[i][j])
                if i not in V:
                    V.append(i)
    n = len(cost_list)
    for i in range(n - 1):      # posortowanie (bąbelkowe) krawędzi - od najmniejszego ich kosztu, do największego
        for j in range(0, n - i - 1):
            if cost_list[j] > cost_list[j + 1]:
                cost_list[j], cost_list[j + 1] = cost_list[j + 1], cost_list[j]
                edges_list[j], edges_list[j + 1] = edges_list[j + 1], edges_list[j]

    total_cost = 0      # całkowity koszt cyklu hamiltona
    for idx, el in enumerate(edges_list):       # iterowanie po posortowanych krawędziach względem kosztów
        if el[0] in res.keys() or el[1] in res.values():        # sprawdzenie warunku, czy el[0] jest już początkiem
            # krawędzi a el[1] jest już końcem krawędzi, jeśli tak, to przechodzimy do kolejnej krawędzi
            continue

        if (el[1] in res.keys() and el[0] in res.values()) and (len(res.keys()) < (len(V) - 1)):        # sprawdzenie
            # warunku, czy el[1] jest już początkiem krawędzi a el[0] jest końcem i, czy dodanie krawędzi nie zakończy
            # poszukiwania kolejnych krawędzi
            if sub_cycle_exist(res, el[0], el[1]):
                continue

        res[el[0]] = el[1]      # dodanie do rozwiązania krawędzi, która spełnia powyższe warunki
        total_cost += cost_list[idx]        # dodanie do całkowitego kosztu aktualnego kosztu krawędzi
    print(res)
    if len(res) < len(V):       # warunek na graf, dla którego nie można utworzyć cyklu Hamiltona, np grafu z
        # wierzchołkiem rozspajającym
        raise Exception("Brak rozwiązania")

    return res, total_cost


def sub_cycle_exist(res, x, y):
    act = y
    for i in range(len(res.keys())):
        if act not in res.keys():
            return False
        act = res[act]
        if act == x:
            return True

def print_tsp(V, suma):
    string = f"{list(V.keys())[0]}"
    act = list(V.keys())[0]
    for i in range(len(V.keys())):
        string += f" - {V[act]}"
        act = V[act]
    print(f"{string}  :  {suma}")


example_1 = np.array([
 [0, 2, 3, 5, 5, 3, 6, 11, 9, 5],
 [2, 0, 1, 4, 4, 7, 5, 2, 8, 10],
 [3, 1, 0, 5, 2, 11, 9, 2, 3, 7],
 [5, 4, 5, 0, 3, 9, 12, 6, 8, 1],
 [5, 4, 2, 3, 0, 5, 7, 3, 10, 4],
 [3, 7, 11, 9, 5, 0, 9, 1, 5, 3],
 [6, 5, 9, 12, 7, 9, 0, 6, 3, 2],
 [11, 2, 2, 6, 3, 1, 6, 0, 2, 3],
 [9, 8, 3, 8, 10, 5, 3, 2, 0, 9],
 [5, 10, 7, 1, 4, 3, 2, 3, 9, 0]
])

# example_2 = np.array([
#  [0, 2, 1, 4, 3, 6, 10],
#  [2, 0, 2, 3, 3, 3, 5],
#  [1, 2, 0, 7, 1, 2, 4],
#  [4, 3, 7, 0, 6, 4, 4],
#  [3, 3, 1, 6, 0, 3, 8],
#  [6, 3, 2, 4, 3, 0, 3],
#  [10, 5, 4, 4, 8, 3, 0]
# ])
example_2 = np.array([
 [0, 0, 0, 1, 0, 1, 2, 0, 0, 0],
 [0, 0, 2, 4, 3, 0, 0, 0, 0, 0],
 [0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 4, 0, 0, 1, 0, 4, 5, 3, 0],
 [0, 3, 0, 1, 0, 0, 0, 0, 0, 2],
 [1, 0, 0, 0, 0, 0, 2, 0, 4, 0],
 [2, 0, 0, 4, 0, 2, 0, 4, 5, 0],
 [0, 0, 0, 5, 0, 0, 4, 0, 2, 0],
 [0, 0, 0, 3, 0, 4, 5, 2, 0, 0],
 [0, 0, 1, 0, 2, 0, 0, 0, 0, 0],
])
# print(greed(example_1)[0])
# print_tsp(greed(example_1)[0], greed(example_1)[1])
# print(" ")
print(greed(example_2)[0])
print_tsp(greed(example_1)[0], greed(example_1)[1])

# example_3 = np.array([
#  [0, 2, 1, 4, 3, 0, 0],
#  [2, 0, 0, 3, 0, 0, 5],
#  [1, 0, 0, 7, 1, 2, 0],
#  [4, 3, 7, 0, 0, 4, 4],
#  [3, 0, 1, 0, 0, 3, 0],
#  [0, 0, 2, 4, 3, 0, 3],
#  [0, 5, 0, 4, 0, 3, 0]])
# print(greed(example_3)[0])
#
# example_4 = np.array([
#     [0, 2, 0, 0, 5, 0, 0, 0, 0, 5],
#     [2, 0, 1, 0, 4, 0, 0, 0, 0, 0],
#     [0, 1, 0, 5, 2, 0, 0, 0, 0, 0],
#     [0, 0, 5, 0, 0, 0, 0, 6, 8, 0],
#     [5, 4, 2, 0, 0, 6, 0, 3, 0, 4],
#     [0, 0, 0, 0, 6, 0, 9, 1, 0, 0],
#     [0, 0, 0, 0, 0, 9, 0, 0, 3, 2],
#     [0, 0, 0, 6, 3, 1, 0, 0, 2, 0],
#     [0, 0, 0, 8, 0, 0, 3, 2, 0, 0],
#     [5, 0, 0, 0, 4, 0, 2, 0, 0, 0]
# ])
# print(greed(example_4)[0])
