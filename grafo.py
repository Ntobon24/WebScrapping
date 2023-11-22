class Grafo:
    def __init__(self):
        self.adj_list = {}

    def nuevo_nodo(self, valor):
        if valor not in self.adj_list:
            self.adj_list[valor] = []
        else:
            return False

    def nueva_arista(self, v1, v2, bid=False, tipo=None):
        if v1 not in self.adj_list:
            self.nuevo_nodo(v1)
        if v2 not in self.adj_list:
            self.nuevo_nodo(v2)

        self.adj_list[v1].append([v2, tipo])

        if bid:
            self.adj_list[v2].append([v1, tipo])

