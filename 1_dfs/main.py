# class Graph:
#     def __init__(self, par):
#         if isinstance(par, dict):
#             self.graph = par
#         if isinstance(par, list):
#             dictionary = {}
#             for row in range(len(par)):
#                 numb = []
#                 for el in range(len(par)):
#                     if par[row][el] >=1:
#                         x = par[row][el]
#                         for i in range(x):
#                             numb.append((el+1))
#                         dictionary[row+1] = numb
#             self.graph = dictionary


def dfs_recursive(G, s):  # G-dany słownik reprezentujący graf; s-numer wierzchołka, od którego zaczynamy przeszukiwanie
    def dfs_recursive_nested(G, s, L):  # -||- ; L- lista odwiedzonych wierzchołków w odpowiedniej kolejności
        L.append(s)     # dodanie wierzchołka do listy
        for key in G[s]:    # iterowanie po wartościach jednego elementu słownika reprezentującego graf
            if key not in L:    # sprawdzenie, czy wartość, występuje już w liście odwiedzonych wierzchołków
                dfs_recursive_nested(G, key, L) # jeśli wartość nie występuje, następuje wywołanie funkcji zagnieżdżonej
    L = []  # tworzę pustą listę
    dfs_recursive_nested(G, s, L)   # wywołanie funkcju zagnieżdżonej
    # if len(L) < len(G.values()):                 # jeżeli liczba odwiedzonych wierzchołków jest mniejsza niż liczba
    #     print("Graf jest nispójny")     # elementów słownika przekazanego do funkcji to graf jest niespójny
    result = {}     # tworzę słownik do reprezentacji danych numer_odwiedzonego:odwiedzony
    for i in range(len(L)):     # numerowanie wierzchołków - kolejność; .key() - kolejność odwiedzenia
        result[i+1] = L[i]      # .value() - numer wierzchołka
    return L, result


def is_acycle(G, s):
    def is_acycle_nested(G, s, L, is_a = 0):
        L.append(s)
        for key in G[s]:
            if key not in L:
                is_acycle_nested(G, key, L, is_a)
            else:               # jeżeli jedan z wartośći(wierzchołków) danego elementu słownika reprezentacyjnego graf
                is_a = 1        # występuje już w liście odwiedzonych wierzchołków, oznacza to, że graf jest cykliczy
        return is_a             # (zmiana wartości zmiennej na jedynkę)
    L = []
    is_a = is_acycle_nested(G, s, L)
    if is_a == 0:   # sprawdzenie, czy zmienna jest równa '0', jeśli tak, to graf jest acykliczny
        return print("graf jest acykliczny")
    else:
        return print("graf jest cykliczny")


def is_consistent(G, s):
    def is_consistent_nested(G, s, L, is_a = 0):
        L.append(s)
        for key in G[s]:
            if key not in L:
                is_consistent_nested(G, key, L, is_a)
    L = []
    is_consistent_nested(G, s, L)
    if len(L) < len(G.keys()):   # sprawdzenie, czy długość listy jest mniejsza od kluczy listy sąsiedztwa
        return print("graf jest niespójny")
    else:
        return print("graf jest spójny")


consistant_acyclic_graph = {
    1: [2, 3],
    2: [4, 5, 6],
    3: [],
    4: [6, 7],
    5: [6],
    6: [7],
    7: []
}
con_cyclic_graph = {
    1: [2, 5],
    2: [1, 3],
    3: [2, 4, 5],
    4: [3, 8],
    5: [1, 3, 6, 8],
    6: [5, 7],
    7: [6],
    8: [4, 5, 9],
    9: [8],
}

not_con_cyclic_graph = {
    1: [2, 5],
    2: [1, 3],
    3: [2, 4, 5],
    4: [3, 8],
    5: [1, 3, 6, 8],
    6: [5, 7],
    7: [6],
    8: [4, 5, 9],
    9: [8],
    10: []
}


print(dfs_recursive(consistant_acyclic_graph, 1)[1])
is_acycle(consistant_acyclic_graph, 1)
is_consistent(consistant_acyclic_graph, 1)
print("")
print(dfs_recursive(con_cyclic_graph, 1)[1])
is_acycle(con_cyclic_graph, 1)
is_consistent(con_cyclic_graph, 1)
print("")
print(dfs_recursive(not_con_cyclic_graph, 1)[1])
is_acycle(not_con_cyclic_graph, 1)
is_consistent(not_con_cyclic_graph, 1)
