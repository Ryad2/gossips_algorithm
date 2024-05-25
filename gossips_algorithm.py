class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.enemy = [-1] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

    def add_friendship(self, a, b):
        visited = set()
        self._add_friendship(a, b, visited)

    def _add_friendship(self, a, b, visited):
        if (a, b) in visited or (b, a) in visited:
            return
        visited.add((a, b))


        root_a = self.find(a)
        root_b = self.find(b)
        self.union(a, b)
        root_a_enemy = self.enemy[root_a]
        root_b_enemy = self.enemy[root_b]
        if root_a_enemy != -1 and root_b_enemy != -1:
            self.union(root_a_enemy, root_b_enemy)
        if root_a_enemy != -1:
            self._add_enmity(root_a_enemy, root_a, visited)
        if root_b_enemy != -1:
            self._add_enmity(root_b_enemy, root_b, visited)

    def add_enmity(self, a, b):
        visited = set()
        self._add_enmity(a, b, visited)

    def _add_enmity(self, a, b, visited):
        if (a, b) in visited or (b, a) in visited:
            return
        visited.add((a, b))

        root_a = self.find(a)
        root_b = self.find(b)
        root_a_enemy = self.enemy[root_a]
        root_b_enemy = self.enemy[root_b]
        if root_a_enemy != -1:
            self._add_friendship(root_a_enemy, b, visited)
        if root_b_enemy != -1:
            self._add_friendship(root_b_enemy, a, visited)
        self.enemy[root_a] = self.find(b)
        self.enemy[root_b] = self.find(a)

    def are_friends(self, a, b):
        return self.find(a) == self.find(b)

    def are_enemies(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        root_a_enemy = self.enemy[root_a]
        root_b_enemy = self.enemy[root_b]
        return (root_a_enemy != -1 and self.find(root_a_enemy) == self.find(b)) or \
            (root_b_enemy != -1 and self.find(root_b_enemy) == self.find(a))

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()

    n = int(data[0])
    q = int(data[1])
    gossips = data[2:]

    uf = UnionFind(n)
    index = 0
    results = []

    for _ in range(q):
        s = int(gossips[index])
        a = int(gossips[index + 1])
        b = int(gossips[index + 2])
        index += 3

        if s == 0:
            if uf.are_enemies(a, b):
                results.append("NO")
            else:
                uf.add_friendship(a, b)
                results.append("YES")
        else:
            if uf.are_friends(a, b):
                results.append("NO")
            else:
                uf.add_enmity(a, b)
                results.append("YES")

    # Output the results for each gossip
    for result in results:
        print(result)

    group_size = [0] * n
    max_size = 0

    for i in range(n):
        root_i = uf.find(i)
        group_size[root_i] += 1

    table = [(index, size, -1 if uf.enemy[index] == -1 else uf.find(uf.enemy[index])) for index, size in enumerate(group_size) if size > 0]

    for el in table:
        index, size, enemy = el
        if enemy == -1:
            max_size += size
        elif size == group_size[enemy]:
            max_size += size / 2

        elif min(size, group_size[enemy]) == size:
            continue
        else:
            max_size += size

    print(int(max_size))

# Example input redirection for testing (you can remove this in the final version)
if __name__ == "__main__":
    from io import StringIO
    import sys

    input_str = """9 16
1 0 1
1 2 3
1 4 5
1 1 6
1 3 7
1 5 8
1 3 0
1 3 4
1 0 4
1 4 8
1 6 8
1 6 0
0 0 4
0 4 8
0 6 8
0 6 0"""
    sys.stdin = StringIO(input_str)
    main()
