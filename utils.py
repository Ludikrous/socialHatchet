import hatchet as ht
import pandas as pd

def readEdgelist(path):
    # graph will be an adjacency list, {int -> int[]}, where int is a vertex
    graph = {}
    nodes = set()

    with open(path) as file:
        for edgeText in file:
            start, end, weight = edgeText.split()
            graph.setdefault(int(start), []).append(int(end))
            nodes.add(int(start))
            nodes.add(int(end))
    
    return graph, nodes

def makeGraphFrame(path, roots=[]):
    g, n = readEdgelist(path)      # get basic adj list
    
    # make hatchet graph
    nodes = {}
    for node in range(1,129):
        nodes[node] = ht.node.Node(ht.frame.Frame(name=str(node), followers=len(g[node]) if node in g else 0, time=1, rank=0, thread=0))
    
    for node in g.keys():
        for child in g[node]:
            nodes[node].add_child(nodes[child])
    
    # allow user to specify one root
    if len(roots) == 0:
        htGraph = ht.graph.Graph(list(nodes.values()))
    else:
        htGraph = ht.graph.Graph([nodes[i] for i in roots])

    # dataframe
    htDataFrame = pd.DataFrame([[nodes[i], i, nodes[i].frame['followers'], 1, 0, 0] for i in g.keys()], columns=["node", "name", "followers", "time", "rank", "thread"])
    htDataFrame = htDataFrame.set_index("node")
    return ht.graphframe.GraphFrame(htGraph, htDataFrame)


# ============ MISC CLEANING ===================================================

def shorten():
    g, n = readEdgelist("./data/higgs-retweet_network.edgelist")

    new = set(list(n)[:128])

    with open("./data/higgs-social_network-short.edgelist", 'w') as out:
        for node in new:
            for neigh in g[node]:
                if neigh in new:
                    out.write(str(node) + " " + str(neigh) + "\n")
