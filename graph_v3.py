import networkx as nx
import time
import matplotlib.pyplot as plt

# Fonctions de gestion du graphe (créer, ajouter/supprimer des nœuds/arcs, etc.)
def create_graph():
    """Crée un graphe vide"""
    return nx.Graph()

def add_node(graph, node):
    """Ajoute un sommet au graphe"""
    graph.add_node(node)

def add_edge(graph, u, v):
    """Ajoute un arc entre deux sommets"""
    graph.add_edge(u, v)

def remove_node(graph, node):
    """Supprime un sommet du graphe"""
    graph.remove_node(node)

def remove_edge(graph, u, v):
    """Supprime un arc entre deux sommets"""
    graph.remove_edge(u, v)

def read_graph_from_file(file_path):
    """Lit un graphe depuis un fichier en format DIMACS (ou similaire)"""
    graph = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('e'):  # On ne traite que les lignes d'arêtes
                parts = line.split()
                if len(parts) == 3:  # Vérifie qu'il y a bien 3 éléments (le préfixe 'e' et 2 sommets)
                    u, v = map(int, parts[1:])
                    graph.add_edge(u, v)
    return graph

def write_graph_to_file(graph, file_path):
    """Écrit un graphe dans un fichier"""
    with open(file_path, 'w') as file:
        for u, v in graph.edges():
            file.write(f"{u} {v}\n")

def display_graph(graph):
    """Affiche les informations de base sur le graphe"""
    print(f"Nombre de sommets : {graph.number_of_nodes()}")
    print(f"Nombre d'arcs : {graph.number_of_edges()}")
    print("Liste des sommets :", list(graph.nodes))
    print("Liste des arcs :", list(graph.edges))

def welsh_powell(graph):
    """Implémente l'algorithme Welsh-Powell pour colorer un graphe"""
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree[x], reverse=True)
    color_map = {}
    current_color = 0

    for node in sorted_nodes:
        if node not in color_map:
            current_color += 1
            color_map[node] = current_color
            for neighbor in graph.nodes:
                if neighbor not in color_map and all(color_map.get(n) != current_color for n in graph.neighbors(neighbor)):
                    color_map[neighbor] = current_color
    return color_map

def greedy_coloring(graph):
    """Implémente l'algorithme de coloration greedy"""
    color_map = {}
    for node in graph.nodes:
        neighbor_colors = {color_map[neighbor] for neighbor in graph.neighbors(node) if neighbor in color_map}
        color = 1
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
    return color_map

def dsatur(graph):
    """Implémente l'algorithme DSATUR pour colorer un graphe"""
    color_map = {}
    saturation = {node: 0 for node in graph.nodes}
    degree = {node: graph.degree[node] for node in graph.nodes}

    while len(color_map) < graph.number_of_nodes():
        node = max((n for n in graph.nodes if n not in color_map), key=lambda x: (saturation[x], degree[x]))
        neighbor_colors = {color_map[neighbor] for neighbor in graph.neighbors(node) if neighbor in color_map}
        color = 1
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
        for neighbor in graph.neighbors(node):
            if neighbor not in color_map:
                saturation[neighbor] += 1
    return color_map

# Nouvelle fonction dédiée à la visualisation
def visualize_graph(graph, color_map, title):
    """Affiche la visualisation du graphe avec une coloration spécifique"""
    # Extraire les couleurs des nœuds en fonction de color_map
    colors = [color_map.get(node, 0) for node in graph.nodes()]
    nx.draw(graph, with_labels=True, node_color=colors, cmap=plt.cm.rainbow)
    plt.title(title)
    plt.show()

def test_with_random_graph():
    random_graph = nx.erdos_renyi_graph(50, 0.2)
    display_graph(random_graph)

    start = time.time()
    coloration_wp = welsh_powell(random_graph)
    end = time.time()
    print("Welsh-Powell (Graphe aléatoire) :", coloration_wp)
    print("Temps Welsh-Powell :", end - start, "secondes")

    start = time.time()
    coloration_greedy = greedy_coloring(random_graph)
    end = time.time()
    print("Greedy Search (Graphe aléatoire) :", coloration_greedy)
    print("Temps Greedy Search :", end - start, "secondes")

    start = time.time()
    coloration_dsatur = dsatur(random_graph)
    end = time.time()
    print("DSATUR (Graphe aléatoire) :", coloration_dsatur)
    print("Temps DSATUR :", end - start, "secondes")

    # Visualisation du graphe avec Welsh-Powell
    visualize_graph(random_graph, coloration_wp, "Welsh-Powell (Graphe Aléatoire)")

# Exemple de code pour lire et afficher un graphe à partir d'un fichier
file_path = "graph_2.txt"  # Assure-toi de mettre ici le bon chemin

# Lecture du graphe depuis le fichier
g_loaded = read_graph_from_file(file_path)
display_graph(g_loaded)

# Visualisation avec Welsh-Powell
coloration_wp = welsh_powell(g_loaded)
visualize_graph(g_loaded, coloration_wp, "Welsh-Powell Coloration")

# Visualisation avec Greedy Search
coloration_greedy = greedy_coloring(g_loaded)
visualize_graph(g_loaded, coloration_greedy, "Greedy Search Coloration")

# Tester avec un graphe aléatoire
test_with_random_graph()
