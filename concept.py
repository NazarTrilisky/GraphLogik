from copy import deepcopy


MAX_WEIGHT = 5
MAX_ACTIVATION = 5


class Node:
    def __init__(self, value:str, edges:list):
        self.value = value
        self.edges = edges
        self.activation = 0

    def set_edges(self, edges):
        self.edges = deepcopy(edges)

    def set_activation(self, level:int):
       assert level in list(range(MAX_ACTIVATION + 1))
       self.level = level


class Edge:
    def __init__(self, start:object, end:object, weight:int):
        self.start  = start
        self.end  = end
        assert abs(weight) in list(range(MAX_WEIGHT + 1))
        self.weight = weight


class Graph:
    def __init__(self, root):
        self.root = root

    def next_likely_nodes(self, node):
        res = []
        sorted_edges = sorted(node.edges, key=lambda x: x.weight, reverse=True)
        for edge in sorted_edges:
            new_node = edge.start if edge.end.value == node.value else edge.end
            res.append(new_node)
        return res


n1 = Node("Toothpaste", [])
n2 = Node("Mouthwash", [])
n3 = Node("Cavities", [])
n4 = Node("Fresh breath", [])

e12 = Edge(n1, n2, 4)
e13 = Edge(n1, n3, -4)
e14 = Edge(n1, n4, 4)
e23 = Edge(n2, n3, -4)
e24 = Edge(n2, n4, 5)
e34 = Edge(n3, n4, -5)

n1.set_edges([e12, e13, e14])
n2.set_edges([e12, e23, e24])
n3.set_edges([e13, e23, e34])
n4.set_edges([e14, e24, e34])

graph = Graph(n1)


print("If I use mouthwash the likely outcome is: ")
n2.set_activation(5)
print(graph.next_likely_nodes(n2)[0].value)

print("\nIf I use toothpaste the unlikely outcome is: ")
n2.set_activation(1)
n1.set_activation(5)
print(graph.next_likely_nodes(n1)[-1].value)
