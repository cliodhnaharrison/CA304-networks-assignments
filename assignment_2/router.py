#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx
import pandas

class Router:
    def __init__(self, name, graph):
        """
        Initialises required attributes of router object.

        Args:
            name: string name of router
            graph: Graph object with all connections for this router and others
        """
        self.name = name
        self.graph = graph
        self.paths = {}


    def remove_router(self, router_name):
        """
        Removes router from self.graph.edges and self.graph.nodes

        Args:
            router_name: string name of router to be removed

        Prints:
            prints new routing table from self.print_routing_table()
        """
        self.graph.nodes.remove(router_name)
        del self.graph.edges[router_name]
        for node in self.graph.edges:
            if router_name in self.graph.edges[node]:
                del self.graph.edges[node][router_name]
        self.print_routing_table()


    def get_path(self, router_name):
        """
        Uses Dijkstra's algorithm to find shortest path between self and given
        router_name.

        Args:
            router_name: string name of router to find shortest path to.

        Returns:
            message: formated string of start, finish, cost and path

        Raises:
            Exception: if there is a node with no path to it
        """
        start = self.name
        finish = router_name

        # Populate unvisted dictionary with node: [None, None]
        # eg {"a": [None, None], "b": [None, None], ...}
        unvisited = {node: [None, None] for node in self.graph.nodes}
        visited = {}
        curr = start
        curr_distance = 0
        path  = self.name
        unvisited[curr] = [curr_distance, path]

        while True:
            # Loop through each neighbour of the current node
            # eg self.graph.edges["a"] = {"b": 7, "c", 10, "f": 14}
            for neighbour, distance in self.graph.edges[curr].items():
                if neighbour not in unvisited:
                    continue
                new_dist = curr_distance + distance
                new_path = path + neighbour

                # If no cost for this neighbour or bigger cost in unvisited
                if not unvisited[neighbour][0] or unvisited[neighbour][0] > new_dist:
                    unvisited[neighbour] = [new_dist]
                    unvisited[neighbour].append(new_path)
            visited[curr] = [curr_distance]
            visited[curr].append(unvisited[curr][1])
            del unvisited[curr]

            # if no more nodes to visit then exit the while loop
            if not unvisited:
                break

            # find next node to travel to
            candidates = [node for node in unvisited.items() if node[1][0]]
            if not candidates:
                raise Exception("There is a problem with your graph, missing connections")
            curr, dist_path = sorted(candidates, key = lambda x: x[1])[0]
            curr_distance, path = dist_path[0], dist_path[1]

        # Constructs message to print out
        message = ""
        message += f"Start: {start}\n"
        message += f"Finish: {finish}\n"
        print_path = "->".join(visited[finish][1])
        message += f"Path: {print_path}\n"
        message += f"Cost: {visited[finish][0]}\n"
        self.paths = visited

        return message


    def print_routing_table(self):
        """
        Prints out routing table of costs and shortest paths from self router to
        all others in self.graph.
        """
        # Call to self.get_path updates the class variable self.paths
        self.get_path(self.graph.nodes[0])
        routing_table = {}
        i = 0
        for k, v in self.paths.items():
            # Don't include self to self
            if k == self.name:
                continue
            routing_table[i] = [self.name, k, v[0], "->".join(v[1])]
            i += 1
        print(pandas.DataFrame.from_dict(routing_table, orient="index", columns=["From", "To", "Cost", "Path"]))


class Graph:
    def __init__(self):
        """
        Initialises all required attributes of a Graph object.
        """
        self.edges = {}
        self.nodes = []
        self.nx_edges = []
        self.nx_weights = {}


    def add_edge(self, node1, node2, weight):
        """
        Adds edges to graph. Assumes relations are bidirectional.

        Populates self.nodes as list of nodes in graph:
        eg ["a", "b", "c", ...]

        Populates self.edges as dictionary of relations:
        eg {"a": {"b": 7}, "b": {"a": 7}}
        """
        self.nx_edges.append((node1.upper(), node2.upper()))
        self.nx_weights[(node1.upper(), node2.upper())] = str(weight)
        if node1 not in self.edges:
            self.edges[node1] = {node2: weight}
            self.nodes.append(node1)
        else:
            self.edges[node1][node2] = weight
        if node2 not in self.edges:
            self.edges[node2] = {node1: weight}
            self.nodes.append(node2)
        else:
            self.edges[node2][node1] = weight

    def visualise(self):
        """
        Uses networkx and matplotlib to visualise Graph object.
        """
        G = nx.Graph()
        G.add_nodes_from([node.upper() for node in self.nodes])
        for x in self.nx_edges:
            G.add_edge(*x)
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw_networkx(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=self.nx_weights)
        plt.show()




def main():
    """
    Function for testing functionality of Router and Graph classes.

    Commented out all the printing lines.
    """
    g = Graph()
    g.add_edge("a", "b", 7)
    g.add_edge("a", "c", 9)
    g.add_edge("a", "f", 14)
    g.add_edge("b", "c", 10)
    g.add_edge("b", "d", 15)
    g.add_edge("c", "d", 11)
    g.add_edge("c", "f", 2)
    g.add_edge("d", "e", 6)
    g.add_edge("e", "f", 9)
    r = Router("a", g)
    r2 = Router("b", g)
    # g.visualise()
    # r.print_routing_table()
    # print ("-------------")
    # r2.print_routing_table()
    # print ("-------------")
    # r.remove_router("c")
    # print ("-------------")
    # r2.print_routing_table()



if __name__ == "__main__":
    main()
