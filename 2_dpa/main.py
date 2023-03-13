import math
from copy import deepcopy


def DPA(graph: list, s: int = 0):       # graph - przekazany graf w postaci macierzy sąsiedztwa,
    # s - przekazana zmienna, mówiąca o tym, od jakiego wierzchołka rozpoczynamy poszukiwania
    V = []
    for el in range(len(graph)):
        for i in range(len(graph)):
            if i not in V:
                V.append(i)     # dodanie wszystkich wierzchołków grafu do pustel listy V
    d = []      # koszt osiągnięcia wierzchołka - od początkowego do aktualnego
    p = []      # poprzednik wierzchołka aktualnego
    for i in V:
        d.append(math.inf)      # przypisanie nieskończoności do utworzonej tablicy
        p.append(0)     # przypisanie 0 do utworzonej tablicy
    Q = deepcopy(V)     # głęboka kopia listy z wszystkimi wierzchołkami grafu
    Q.remove(s)
    d[s] = 0
    last_vertex = s     # przypisanie wierzchołka rozpoczynającego jako ostatni wierzchołek
    while Q:    # pętla do momentu usunięcia wszystkich wierzchołków z listy
        for act_vertex in Q:     # iterowanie po każdym wierzchołku w aktualnej liście wierzchołków, które nie zostały
            # jeszcze odwiedzone
            neighbours = [i for i in range(len(graph)) if (graph[last_vertex][i] != 0)]     # utworzenie listy
            # wierzchołków sąsiadujących z ostatnio odwiedzonym wierzchołkiem
            if act_vertex in neighbours and (d[last_vertex] + graph[last_vertex][act_vertex] < d[act_vertex]):
                # jeżeli aktualnie odwiedzony wierzchołek znajduje się w liście sąsiadów wcześniejszego wierzchołka
                # i koszt osiągnięcia poprzedniego wierzchołka powiększony o wagę krawędzi jest mniejszy od kosztu
                # osiągnięcia aktualnego wierzchołka
                d[act_vertex] = d[last_vertex] + graph[last_vertex][act_vertex]     # zapisanie kosztu przejścia do
                # aktualnego wierzchołka
                p[act_vertex] = last_vertex     # przypisane do listy poprzednichy wierzchołków,
                # aktualnie poprzedniego wierzchołka
        mini = math.inf     # stworzenie dodatkowej zmiennej reprezetującej nieskończoność
        for act_vertex in Q:     # iterowanie po wszystkich wierzchołach w liście Q
            if d[act_vertex] < mini:    # spełnienie warunku, czy koszt dotarcia do aktualnego wierzchołka jest
                # mniejsza od 'inf'
                mini = d[act_vertex]    # zmiana wartości zmiennej, na aktualny koszt
                last_vertex = act_vertex    # zmiana aktualnie odwiedzonego wierzchołka na ostatnio odwiedzony, aby
                # kolejne iteracje odnosiły się do ostatniego wierzchołka
        Q.remove(last_vertex)   # usunięcie z listy wierzchołków odwiedzonego wierzchołka
    new_d = {}      # stworzenie pustego słownika
    for i in V:
        new_d[i] = d[i]     # iterowanie po wszystkich wierzchołkach grafu, i dodanie do słownika,
        # klucz - wierzchołek do którego podróżujemy; wartość - minimalny koszt dotarcia do danego wierzchołka
    return new_d


con_cyclic_graph = [
    [0, 2, 0, 0, 5, 0, 0, 0, 0, 5],
    [2, 0, 1, 0, 4, 0, 0, 0, 0, 0],
    [0, 1, 0, 5, 2, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 6, 8, 0],
    [5, 4, 2, 0, 0, -6, 0, 3, 0, 0],
    [0, 0, 0, 0, -6, 0, 9, 1, 0, 0],
    [0, 0, 0, 0, 0, 9, 0, 0, 3, 2],
    [0, 0, 0, 6, 3, 1, 0, 0, 2, 0],
    [0, 0, 0, 8, 0, 0, 3, 2, 0, 0],
    [5, 0, 0, 0, 0, 0, 2, 0, 0, 0]
]

print(DPA(con_cyclic_graph))

con_cyclic_graph_2 = [
    [0, 2, 0, 0, 5, 0, 0, 0, 0, 0],
    [2, 0, 1, 0, 4, 0, 0, 0, 0, 0],
    [0, 1, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 6, 8, 0],
    [5, 4, 0, 0, 0, 5, 0, 3, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 6, 3, 1, 0, 0, 2, 0],
    [0, 0, 0, 8, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0]
]
# print(DPA(con_cyclic_graph_2))