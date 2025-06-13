from modelAdmin import MagasinModel

class Dijkstra:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        self.cases_rayon = []
    
    def creer_graphe(rows, cols, rayon):
        """
        - rows, cols : dimensions de la grille
        - rayon : liste de coordonnées (i, j) représentant les rayons
        """
        graphe = {}

        for i in range(rows):
            for j in range(cols):
                if (i, j) in rayon:
                    continue  # Ignorer les rayon (rayons)

                voisins = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) not in rayon:
                        voisins.append((ni, nj))

                graphe[(i, j)] = voisins

        return graphe


    def printSolution(self, dist, parent, src):
        print("Sommet \t Distance depuis", src, "\t Chemin")
        for i in range(self.V):
            if i != src:
                print(f"{i} \t\t {dist[i]} \t\t {self.getPath(parent, i)}")

    def getPath(self, parent, j):
        path = []
        while j != -1:
            path.insert(0, j)
            j = parent[j]
        return path

    def minDistance(self, dist, sptSet):
        min_val = 1e7
        min_index = -1
        for v in range(self.V):
            if dist[v] < min_val and not sptSet[v]:
                min_val = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        parent = [-1] * self.V

        for _ in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                    not sptSet[v] and
                    dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        self.printSolution(dist, parent, src)


g = Dijkstra(9)
g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
           ]

g.dijkstra(0)