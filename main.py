from graph import Graph

if __name__ == "__main__":
    with open("input.txt", "rt") as f:
        q = int(f.readline())
        for i in range(q):
            n, m = [int(value) for value in f.readline().rstrip().split()]
            graph = Graph(n)
            for i in range(m):
                x, y = [int(x) for x in f.readline().rstrip().split()]
                graph.connect(x - 1, y - 1)
            s = int(f.readline())
            graph.find_all_distances(s - 1)
