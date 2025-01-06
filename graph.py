import networkx as nx
import time
import matplotlib.pyplot as plt

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
    """Lit un graphe depuis un fichier"""
    graph = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Enlever les espaces avant et après
            if not line:  # Ignorer les lignes vides
                continue
            
            if line.startswith("c"):
                print(line[1:])  # Afficher les commentaires (lignes commençant par 'c')
                continue
            
            if line.startswith("p"):
                # Traitement spécifique pour les lignes de type 'p' si nécessaire
                print("Détails du graphe :", line[1:])
                continue
            
            if line.startswith("e"):
                # Pour les arêtes, on lit les deux entiers u et v
                try:
                    u, v = map(int, line[1:].split())  # Supposer que 'e' est suivi de deux entiers
                    graph.add_edge(u, v)
                except ValueError:
                    print(f"Format incorrect dans la ligne : {line}")
                    continue  # Ignorer les lignes mal formatées
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
    # Trier les sommets par degré décroissant
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree[x], reverse=True)
    color_map = {}  # Dictionnaire pour stocker la couleur de chaque sommet
    current_color = 0

    for node in sorted_nodes:
        if node not in color_map:
            current_color += 1
            color_map[node] = current_color
            # Colorer les sommets non adjacents
            for neighbor in graph.nodes:
                if neighbor not in color_map and all(color_map.get(n) != current_color for n in graph.neighbors(neighbor)):
                    color_map[neighbor] = current_color
    return color_map

def greedy_coloring(graph):
    """Implémente l'algorithme de coloration greedy"""
    color_map = {}  # Stocker les couleurs attribuées
    for node in graph.nodes:
        # Trouver les couleurs utilisées par les voisins
        neighbor_colors = {color_map[neighbor] for neighbor in graph.neighbors(node) if neighbor in color_map}
        # Attribuer la première couleur disponible
        color = 1
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
    return color_map

def dsatur(graph):
    """Implémente l'algorithme DSATUR pour colorer un graphe"""
    color_map = {}
    saturation = {node: 0 for node in graph.nodes}  # Saturation de chaque sommet
    degree = {node: graph.degree[node] for node in graph.nodes}  # Degré de chaque sommet

    while len(color_map) < graph.number_of_nodes():
        # Trouver le sommet avec la saturation maximale (et degré maximal en cas d'égalité)
        node = max((n for n in graph.nodes if n not in color_map), key=lambda x: (saturation[x], degree[x]))
        # Trouver la première couleur disponible
        neighbor_colors = {color_map[neighbor] for neighbor in graph.neighbors(node) if neighbor in color_map}
        color = 1
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
        # Mettre à jour la saturation des voisins non colorés
        for neighbor in graph.neighbors(node):
            if neighbor not in color_map:
                saturation[neighbor] += 1
    return color_map

def test_with_random_graph():
    """Teste les algorithmes sur un graphe aléatoire"""
    random_graph = nx.erdos_renyi_graph(50, 0.2)  # 50 sommets, densité de 0.2
    display_graph(random_graph)

    # Appliquer Welsh-Powell
    start = time.time()
    coloration_wp = welsh_powell(random_graph)
    end = time.time()
    print("Welsh-Powell (Graphe aléatoire) :", coloration_wp)
    print("Nombre de couleurs (Welsh-Powell) :", max(coloration_wp.values()))
    print("Temps Welsh-Powell :", end - start, "secondes")

    # Appliquer Greedy Search
    start = time.time()
    coloration_greedy = greedy_coloring(random_graph)
    end = time.time()
    print("Greedy Search (Graphe aléatoire) :", coloration_greedy)
    print("Nombre de couleurs (Greedy Search) :", max(coloration_greedy.values()))
    print("Temps Greedy Search :", end - start, "secondes")

    # Appliquer DSATUR
    start = time.time()
    coloration_dsatur = dsatur(random_graph)
    end = time.time()
    print("DSATUR (Graphe aléatoire) :", coloration_dsatur)
    print("Nombre de couleurs (DSATUR) :", max(coloration_dsatur.values()))
    print("Temps DSATUR :", end - start, "secondes")

    # # Visualisation des graphes
    # colors_wp = [coloration_wp.get(node, 0) for node in random_graph.nodes()]
    # nx.draw(random_graph, with_labels=True, node_color=colors_wp, cmap=plt.cm.rainbow)
    # plt.title("Welsh-Powell (Graphe Aléatoire)")
    # plt.show()

    # colors_greedy = [coloration_greedy.get(node, 0) for node in random_graph.nodes()]
    # nx.draw(random_graph, with_labels=True, node_color=colors_greedy, cmap=plt.cm.rainbow)
    # plt.title("Greedy Search (Graphe Aléatoire)")
    # plt.show()

    # colors_dsatur = [coloration_dsatur.get(node, 0) for node in random_graph.nodes()]
    # nx.draw(random_graph, with_labels=True, node_color=colors_dsatur, cmap=plt.cm.rainbow)
    # plt.title("DSATUR (Graphe Aléatoire)")
    # plt.show()

# Exemple d'utilisation
g = create_graph()
add_node(g, 1)
add_node(g, 2)
add_node(g, 3)
add_node(g, 4)
add_edge(g, 1, 2)
add_edge(g, 2, 3)
add_edge(g, 3, 4)
add_edge(g, 4, 1)
display_graph(g)

# Appliquer Welsh-Powell
start = time.time()
coloration_wp = welsh_powell(g)
end = time.time()
print("Welsh-Powell Coloration :", coloration_wp)
# Les fonctions existantes (create_graph, add_node, add_edge, remove_node, etc.) restent inchangées.

def test_with_file_graph(file_path):
    """Teste les algorithmes sur un graphe provenant d'un fichier"""
    # Lire le graphe depuis le fichier
    graph_from_file = read_graph_from_file(file_path)
    display_graph(graph_from_file)

    # Appliquer Welsh-Powell
    start = time.time()
    coloration_wp = welsh_powell(graph_from_file)
    end = time.time()
    print(f"Welsh-Powell (Graphe depuis {file_path}) :", coloration_wp)
    print("Nombre de couleurs (Welsh-Powell) :", max(coloration_wp.values()))
    print("Temps Welsh-Powell :", end - start, "secondes")

    # Appliquer Greedy Search
    start = time.time()
    coloration_greedy = greedy_coloring(graph_from_file)
    end = time.time()
    print(f"Greedy Search (Graphe depuis {file_path}) :", coloration_greedy)
    print("Nombre de couleurs (Greedy Search) :", max(coloration_greedy.values()))
    print("Temps Greedy Search :", end - start, "secondes")

    # Appliquer DSATUR
    start = time.time()
    coloration_dsatur = dsatur(graph_from_file)
    end = time.time()
    print(f"DSATUR (Graphe depuis {file_path}) :", coloration_dsatur)
    print("Nombre de couleurs (DSATUR) :", max(coloration_dsatur.values()))
    print("Temps DSATUR :", end - start, "secondes")

    # # Visualisation des graphes
    # colors_wp = [coloration_wp.get(node, 0) for node in graph_from_file.nodes()]
    # nx.draw(graph_from_file, with_labels=True, node_color=colors_wp, cmap=plt.cm.rainbow)
    # plt.title(f"Welsh-Powell (Graphe depuis {file_path})")
    # plt.show()

    # colors_greedy = [coloration_greedy.get(node, 0) for node in graph_from_file.nodes()]
    # nx.draw(graph_from_file, with_labels=True, node_color=colors_greedy, cmap=plt.cm.rainbow)
    # plt.title(f"Greedy Search (Graphe depuis {file_path})")
    # plt.show()

    # colors_dsatur = [coloration_dsatur.get(node, 0) for node in graph_from_file.nodes()]
    # nx.draw(graph_from_file, with_labels=True, node_color=colors_dsatur, cmap=plt.cm.rainbow)
    # plt.title(f"DSATUR (Graphe depuis {file_path})")
    # plt.show()

# Exemple d'utilisation (avec un fichier "anna.col.txt" qui contient un graphe)
g = create_graph()
add_node(g, 1)
add_node(g, 2)
add_node(g, 3)
add_node(g, 4)
add_edge(g, 1, 2)
add_edge(g, 2, 3)
add_edge(g, 3, 4)
add_edge(g, 4, 1)
display_graph(g)

# Appliquer Welsh-Powell
start = time.time()
coloration_wp = welsh_powell(g)
end = time.time()
print("Welsh-Powell Coloration :", coloration_wp)
print("Nombre de couleurs (Welsh-Powell) :", max(coloration_wp.values()))
print("Temps Welsh-Powell :", end - start, "secondes")

# Appliquer Greedy Search
start = time.time()
coloration_greedy = greedy_coloring(g)
end = time.time()
print("Greedy Search Coloration :", coloration_greedy)
print("Nombre de couleurs (Greedy Search) :", max(coloration_greedy.values()))
print("Temps Greedy Search :", end - start, "secondes")

# Sauvegarde dans un fichier
write_graph_to_file(g, "graph.txt")
print("Graphe sauvegardé dans graph.txt")

# Lecture depuis un fichier
g_loaded = read_graph_from_file("graph.txt")
display_graph(g_loaded)

# # Visualisation du graphe
# colors_wp = [coloration_wp.get(node, 0) for node in g_loaded.nodes()]
# nx.draw(g_loaded, with_labels=True, node_color=colors_wp, cmap=plt.cm.rainbow)
# plt.title("Welsh-Powell Coloration")
# plt.show()

# colors_greedy = [coloration_greedy.get(node, 0) for node in g_loaded.nodes()]
# nx.draw(g_loaded, with_labels=True, node_color=colors_greedy, cmap=plt.cm.rainbow)
# plt.title("Greedy Search Coloration")
# plt.show()

# Tester avec un graphe aléatoire
# test_with_random_graph()

# Tester avec un graphe provenant d'un fichier ("anna.col.txt")
test_with_file_graph("anna.col.txt")

print("Nombre de couleurs (Welsh-Powell) :", max(coloration_wp.values()))
print("Temps Welsh-Powell :", end - start, "secondes")

# Appliquer Greedy Search
start = time.time()
coloration_greedy = greedy_coloring(g)
end = time.time()
print("Greedy Search Coloration :", coloration_greedy)
print("Nombre de couleurs (Greedy Search) :", max(coloration_greedy.values()))
print("Temps Greedy Search :", end - start, "secondes")

# Sauvegarde dans un fichier
write_graph_to_file(g, "graph.txt")
print("Graphe sauvegardé dans graph.txt")

# Lecture depuis un fichier
g_loaded = read_graph_from_file("graph.txt")
display_graph(g_loaded)

# # Visualisation du graphe
# colors_wp = [coloration_wp.get(node, 0) for node in g_loaded.nodes()]
# nx.draw(g_loaded, with_labels=True, node_color=colors_wp, cmap=plt.cm.rainbow)
# plt.title("Welsh-Powell Coloration")
# plt.show()

# colors_greedy = [coloration_greedy.get(node, 0) for node in g_loaded.nodes()]
# nx.draw(g_loaded, with_labels=True, node_color=colors_greedy, cmap=plt.cm.rainbow)
# plt.title("Greedy Search Coloration")
# plt.show()

# Tester avec un graphe aléatoire
test_with_random_graph()

# okay okay 


# ------ Mise en place de anna.col.txt ------ # 


