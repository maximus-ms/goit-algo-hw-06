import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

import pandas as pd

class UkraineRoads:
    CITIES = [
        "Київ",
        "Луцьк",
        "Рівне",
        "Житомир",
        "Чернігів",
        "Суми",
        "Львів",
        "Тернопіль",
        "Хмельницький",
        "Вінниця",
        "Івано-Франківськ",
        "Ужгород",
        "Чернівці",
        "Черкаси",
        "Полтава",
        "Харків",
        "Кропивницький",
        "Дніпро",
        "Запоріжжя",
        "Донецьк",
        "Луганськ",
        "Одеса",
        "Миколаїв",
        "Херсон",
        "Сімферополь",
        "Севастополь",
    ]

    POSITIONS = {
        "Київ": (6.5, 7.5),
        "Луцьк": (2, 8),
        "Рівне": (3, 8),
        "Житомир": (5, 7.5),
        "Чернігів": (7.5, 9),
        "Суми": (10, 8),
        "Львів": (1.5, 7),
        "Тернопіль": (2.5, 6),
        "Хмельницький": (3.5, 6.5),
        "Вінниця": (5, 6),
        "Івано-Франківськ": (2, 5.5),
        "Ужгород": (0, 5),
        "Чернівці": (3, 4.5),
        "Черкаси": (8, 6.5),
        "Полтава": (10, 6.5),
        "Харків": (11.5, 7),
        "Кропивницький": (8, 5),
        "Дніпро": (10.5, 5),
        "Запоріжжя": (10.5, 4.5),
        "Донецьк": (12.5, 4.5),
        "Луганськ": (14, 5),
        "Одеса": (7, 2.5),
        "Миколаїв": (8, 3.5),
        "Херсон": (8.5, 3),
        "Сімферополь": (9.5, 1),
        "Севастополь": (9, 0.5),
    }

    NEIGHBORS = {
        "Київ": [
            "Житомир",
            "Одеса",
            "Чернігів",
            "Суми",
            "Черкаси",
            "Полтава",
            "Кропивницький",
            "Миколаїв",
        ],
        "Луцьк": ["Рівне", "Львів", "Тернопіль"],
        "Рівне": ["Луцьк", "Львів", "Тернопіль", "Хмельницький", "Житомир"],
        "Житомир": ["Рівне", "Хмельницький", "Вінниця", "Київ"],
        "Чернігів": ["Київ"],
        "Суми": ["Київ", "Полтава", "Харків"],
        "Львів": [
            "Луцьк",
            "Ужгород",
            "Івано-Франківськ",
            "Тернопіль",
            "Рівне",
        ],
        "Тернопіль": [
            "Львів",
            "Івано-Франківськ",
            "Ужгород",
            "Чернівці",
            "Хмельницький",
            "Рівне",
            "Луцьк",
        ],
        "Хмельницький": [
            "Рівне",
            "Житомир",
            "Тернопіль",
            "Чернівці",
            "Вінниця",
        ],
        "Вінниця": ["Житомир", "Хмельницький", "Кропивницький", "Одеса"],
        "Івано-Франківськ": ["Ужгород", "Львів", "Чернівці", "Тернопіль"],
        "Ужгород": ["Львів", "Івано-Франківськ", "Тернопіль"],
        "Чернівці": ["Івано-Франківськ", "Хмельницький", "Тернопіль"],
        "Черкаси": ["Київ", "Кропивницький", "Полтава"],
        "Полтава": ["Київ", "Харків", "Дніпро", "Кропивницький"],
        "Харків": ["Полтава", "Дніпро", "Донецьк", "Луганськ"],
        "Кропивницький": [
            "Київ",
            "Вінниця",
            "Одеса",
            "Миколаїв",
            "Полтава",
            "Дніпро",
        ],
        "Дніпро": [
            "Полтава",
            "Харків",
            "Донецьк",
            "Запоріжжя",
            "Миколаїв",
            "Кропивницький",
        ],
        "Запоріжжя": ["Дніпро", "Херсон", "Сімферополь"],
        "Донецьк": ["Дніпро", "Харків", "Луганськ", "Сімферополь"],
        "Луганськ": ["Донецьк", "Харків"],
        "Одеса": ["Київ", "Вінниця", "Кропивницький", "Миколаїв"],
        "Миколаїв": ["Одеса", "Кропивницький", "Дніпро", "Херсон"],
        "Херсон": ["Миколаїв", "Запоріжжя", "Сімферополь"],
        "Сімферополь": ["Херсон", "Запоріжжя", "Донецьк", "Севастополь"],
        "Севастополь": ["Сімферополь"],
    }

    def __init__(self, print_info=False, show=False):
        self.g = nx.Graph()
        self.g.add_nodes_from(UkraineRoads.CITIES)
        nx.set_node_attributes(self.g, UkraineRoads.POSITIONS, "pos")
        for city, neighbors in UkraineRoads.NEIGHBORS.items():
            for neighbor in neighbors:
                distance = self.get_distance(city, neighbor)
                self.g.add_edge(city, neighbor, weight=distance)
            # roads = [(city, n, {"weight":self.get_distance(city, n)}) for n in neighbors]
        if print_info:
            self.print_info()
        if show:
            self.show()

    def get_distance(self, a, b):
        a_pos = UkraineRoads.POSITIONS[a]
        b_pos = UkraineRoads.POSITIONS[b]
        return int(np.sqrt((a_pos[0]-b_pos[0])**2 + (a_pos[1]-b_pos[1])**2)*100)

    def show(self):
        plt.figure(figsize=(12, 6))
        pos = nx.get_node_attributes(self.g, "pos")
        nx.draw(
            self.g,
            pos,
            with_labels=True,
            node_size=400,
            node_color="lightblue",
            font_size=8,
        )
        labels = nx.get_edge_attributes(self.g, 'weight')
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels=labels, font_size=7)
        plt.title("Ukraine")
        plt.show()

    def print_info(self):
        print(f"Number of cities: {self.g.number_of_nodes()}")
        print(f"Number of roads: {self.g.number_of_edges()}")
        dc = nx.degree_centrality(self.g)
        print("Centrality:")
        for c, v in dc.items():
            print(f"  {c:<16} {v}")

    def dfs(self, start):
        visited = set()
        visit_order = []
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visit_order.append(vertex)
                visited.add(vertex)
                stack.extend(list(self.g[vertex]))
        return visit_order

    def bfs(self, start):
        visited = set()
        visit_order = []
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visit_order.append(vertex)
                visited.add(vertex)
                queue.extend(set(self.g[vertex]) - visited)
        return visit_order

    def dijkstra(self, start):
        distances = {vertex: float('infinity') for vertex in self.g}
        distances[start] = 0
        unvisited = list(self.g)

        while unvisited:
            current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
            if distances[current_vertex] == float('infinity'):
                break
            for neighbor, attr in self.g[current_vertex].items():
                distance = distances[current_vertex] + attr["weight"]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
            unvisited.remove(current_vertex)
        return distances

    def get_distance_map(self):
        return pd.DataFrame( { c:self.dijkstra(c) for c in self.g } )

if __name__ == "__main__":
    U = UkraineRoads()
    U.print_info()
    print(f"DFS visit order: {", ".join(U.dfs("Київ"))}")
    print(f"BFS visit order: {", ".join(U.bfs("Київ"))}")
    print(U.get_distance_map())
    U.show()
