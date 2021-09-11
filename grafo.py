import numpy as np
import sys
import random as rd

from numpy.core.numeric import count_nonzero
#sys.path.append('.')


class Graph:
    def __init__(self, vertices, graph_type='directed', weighted = False):
        '''
        Initialises Adjacent Matrix with Zeros and other class variables.
        Parameters:
        vertices -- number of vertices
        graph_type -- 'directed' or 'undirected'
        weighted -- True or False
        '''
        self._vertices = vertices
        self._type = graph_type
        self._weighted = weighted
        self._adjMAT = np.ones(shape=(vertices, vertices), dtype=np.int8)*-1

        self._visited = [False] * self._vertices
        self._padre = [-1] * self._vertices

    def insert_edge(self, u, v, weight=1):
        '''
        Adds an edge between the passed vertices (u,v) by allocating the weight at that index position.
        If the graph is 'undirected', then same weights are also copied to (v,u).
        '''
        self._adjMAT[u][v] = weight
        if self._type == 'undirected':
            self._adjMAT[v][u] = weight

    def remove_edge(self, u, v):
        '''
        Removes an edge between the passed vertices (u,v) by making that index position as 0.
        If the graph is 'undirected', then 0 is also copied to (v,u).
        '''
        self._adjMAT[u][v] = 0
        if self._type == 'undirected':
            self._adjMAT[v][u] = 0

    def exist_edge(self, u, v):
        '''
        Returns True if edge exists between vertices (u,v), else False.
        '''
        return self._adjMAT[u][v] != 0

    def vertex_count(self):
        '''
        Returns number of vertices present in the Graph.
        '''
        return self._vertices

    def edge_count(self):
        '''
        Returns number of edges present in the Graph.
        '''
        count = 0
        for i in range(self._vertices):
            for j in range(self._vertices):
                if self._adjMAT[i][j] != -1:
                    count += 1
        return count


    def vertices(self):
        '''
        Prints all the vertices.
        '''
        for i in range(self._vertices):
            print(i, end=' ')
        print()

    def edges(self):
        '''
        Prints all the edges with weights if the graph is undirected.
        '''
        for i in range(self._vertices):
            for j in range(self._vertices):
                if self._adjMAT[i][j] != -1 and self._weighted == True:
                    print(f'{i} -- {j} = {self._adjMAT[i][j]}')
                elif self._adjMAT[i][j] != -1:
                    print(f'{i} -- {j}')

    def get_FreeEdges(self, vertice):
        lista=[]
        for i in vertice:
            for j in range(self._vertices):
                if self._adjMAT[i][j] != -1 and self._weighted == True:
                    lista.append((i,j,self._adjMAT[i][j]))
                elif self._adjMAT[i][j] != -1:
                    print(f'{i} -- {j}')
        return lista

    def outdegree(self, v):
        '''
        Returns the outdegree of the passed vertex v.
        '''
        count = 0
        for j in range(self._vertices):
            if self._adjMAT[v][j] != 0:
                count += 1
        return count

    def indegree(self, v):
        '''
        Returns the indegree of the passed vertex v.
        '''
        count = 0
        for i in range(self._vertices):
            if self._adjMAT[i][v] != 0:
                count += 1
        return count


    def display(self):
        '''
        Displays Adjacency Matrix.
        '''
        n_edges = self.edge_count()
        if self._type == 'undirected':
            n_edges = int(n_edges / 2)

        print(self._adjMAT)
        print("Vertices: ", self.vertex_count())
        print("Edges: ", n_edges)

    def flush_visited(self):
        '''
            Reset explored matrix
        '''
        self._visited = [False] * self._vertices
    def is_all_visited(self):
        '''
            return if all vertex are explored 
        '''
        for w in self._visited:
            if not(w):
                return True
        return False
    def get_Nconexo(self):
        '''
            return Number of convex components 

        '''
        Edge = self.get_FreeEdges([x for x in range(self._vertices)])
        dic={}
        freeEdge=[]
        for w in Edge:
            a=w[0]
            b=w[1]

            if a > b:
                a, b = b, a
            if not((a,b)) in dic:
                dic[(a,b)]= w[2]
                freeEdge.append(w)
        vertices = [x for x in range(self._vertices)]
        parent = {}

        for v in vertices:
            parent[v] = v
        ds = DisjointSet(vertices, parent)
        for w in freeEdge:
            if ds._components == 1:
                break
            ds.union(w[0], w[1])
        return ds._components
    
    def is_conexo(self):
        if self.get_Nconexo() == 1:
            return True
        else:
            return False
    def is_tree(self):
        '''
            Returns if Graph is a tree
        '''
        Edge = self.get_FreeEdges([x for x in range(self._vertices)])
        dic={}
        freeEdge=[]
        for w in Edge:
            a=w[0]
            b=w[1]

            if a > b:
                a, b = b, a
            if not((a,b)) in dic:
                dic[(a,b)]= w[2]
                freeEdge.append(w)
        vertices = [x for x in range(self._vertices)]
        parent = {}

        for v in vertices:
            parent[v] = v
        ds = DisjointSet(vertices, parent)
        for w in freeEdge:
            if ds.is_parent(w[0],w[1]):
                return False
            ds.union(w[0],w[1])
        return True
    def get_hijos(self,nodo):
        return [(x,nodo) for x in range(self._vertices) if self._adjMAT[nodo][x] != -1 and self._padre[x] == -1 ]
    def set_padres(self):
        self._padre[0]=0
        padre=0
        sons=[(x,padre) for x in range(self._vertices) if self._adjMAT[0][x] != -1]
        while len(sons) != 0:
            self._padre[sons[0][0]]=sons[0][1]
            for w in self.get_hijos(sons[0][0]):
                sons.append(w)
            sons.pop(0)
    def get_padres(self):
        return self._padre
    
    def traceback(self,nodo):
        camino =[self._padre[nodo]]
        while self._padre[nodo] != nodo:
            nodo= self._padre[nodo]
            camino.append(self._padre[nodo])
        return camino


    def LCA(self,a,b):
        self.set_padres()
        lisA= self.traceback(a)
        lisB= self.traceback(b)
        for y in range(len(lisB)):
            for x in range(len(lisA)):
                if lisA[x] == lisB[y]:
                    return lisB[y]
        
        
        
        







class DisjointSet:
    def __init__(self, vertices, parent):
        self._vertices = vertices
        self._parent = parent
        self._components =  len(vertices)

    def find(self, item):
        if self._parent[item] == item:
            return item
        else:
            return self.find(self._parent[item])
    
    def is_parent(self,set1,set2):
        if self.find(set1) == self.find(set2):
            return True
        else:
             False

    

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self._components = self._components -1
        self._parent[root1] = root2


def generador_minimo(graph, method="prim", noise =False):
    '''
        
    
    
    '''
    if method == "prim":

        arbol=Graph(graph._vertices,graph_type="undirected",weighted=True)
        node=rd.randint(0,graph._vertices-1)
        graph._visited[node]=True
        
        
        freeEdge=graph.get_FreeEdges( [x for x in range(graph._vertices) if graph._visited[x] ] )        
        freeEdge.sort(key=lambda x: x[2])
        
        while graph.is_all_visited():
            for w in freeEdge:
                if not( graph._visited[ w[1] ] ):
                    if noise:
                        print("agregando: ", w)
                    graph._visited[w[1]]= True
                    arbol.insert_edge(w[0],w[1],weight=w[2])
                    break
                    
            freeEdge=graph.get_FreeEdges( [x for x in range(graph._vertices) if graph._visited[x] ] )
            freeEdge.sort(key=lambda x: x[2])
            if noise:
                print(freeEdge)
        graph.flush_visited()

            

        return arbol
    elif method == "kruskal":
        Edge = graph.get_FreeEdges([x for x in range(graph._vertices)])
        dic={}
        freeEdge=[]
        for w in Edge:
            a=w[0]
            b=w[1]

            if a > b:
                a, b = b, a
            if not((a,b)) in dic:
                dic[(a,b)]= w[2]
                freeEdge.append(w)
        freeEdge.sort(key=lambda x: x[2])

        vertices = [x for x in range(graph._vertices)]
        parent = {}

        for v in vertices:
            parent[v] = v
        ds = DisjointSet(vertices, parent)
        arbol=Graph(graph._vertices,graph_type="undirected",weighted=True)
        for w in freeEdge:
            if noise:
                print("considerando: ", w)
            if ds._components == 1:
                break
            if not(ds.is_parent(w[0],w[1])):
                ds.union(w[0], w[1])
                if noise:
                        print("agregando: ", w)
                arbol.insert_edge(w[0],w[1],weight=w[2])
        
        return arbol


def grafo_Aleatorio(n,p,max_value=999):
    '''
        Returns graph using Edos-Renyi
    '''
    grafo=Graph(n,graph_type="undirected",weighted=True)
    for w in range(n):
        for k in range(w):
            if rd.random() < p:
                grafo.insert_edge(k,w,weight=rd.randint(0,max_value))
    return grafo
def grafo_AleatorioA(n,p,m,max_value=999):
    '''
        Returns graph using Edos-Renyi with m-vertices
    '''
    grafo=Graph(n,graph_type="undirected",weighted=True)
    E = [(u,v) for v in range(n) for u in range(v)]
    for w in rd.sample(E,m):
        grafo.insert_edge(w[0],w[1],weight=rd.randint(0,max_value))
    return grafo
def grafoConexo_Aleatorio(n,p,max_value=999):
    grafo=Graph(n,graph_type="undirected",weighted=True)

    vertices = [x for x in range(grafo._vertices)]
    parent = {}
    for v in vertices:
        parent[v] = v
    ds = DisjointSet(vertices, parent)
    candidatos=[(u,v) for v in range(n) for u in range(v)]
    rd.shuffle(candidatos)
    count=0
    while ds._components != 1:
        if count == len(candidatos):
            count = 0
        if rd.random() < p:
            value=rd.randint(0,max_value)
            print(candidatos[count][0],candidatos[count][1],value)
            grafo.insert_edge(candidatos[count][0],candidatos[count][1],weight=value)
            ds.union(candidatos[count][0],candidatos[count][1])
        count+=1
    return grafo



                
        



