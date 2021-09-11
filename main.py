
from grafo import  Graph as gf
import grafo

nodo2 = gf(6,graph_type="undirected",weighted=True)

nodo2.insert_edge(0,1,weight=8)
nodo2.insert_edge(0,3,weight=1)
nodo2.insert_edge(1,2,weight=5)
nodo2.insert_edge(1,4,weight=7)
nodo2.insert_edge(2,5,weight=3)
nodo2.insert_edge(3,4,weight=12)
nodo2.insert_edge(4,5,weight=2)


nodo1 = gf(5,graph_type="undirected",weighted=True)

nodo1.insert_edge(0,2,weight=8)
nodo1.insert_edge(0,3,weight=2)
nodo1.insert_edge(1,2,weight=2)
nodo1.insert_edge(1,3,weight=6)
nodo1.insert_edge(1,4,weight=1)
nodo1.insert_edge(2,4,weight=4)

nodo1.display()


print("----------Usando arlbol generador de peso minimo---------")
#usando prim
grafo.generador_minimo(nodo1,method="kruskal",noise=False).display()

#usando kruskal
grafo.generador_minimo(nodo1,method="kruskal",noise=False).display()

print("------------------------------------------------------")
print("------------grafo aleatorios----------------------")

#usando renyi
grafo.grafo_Aleatorio(6,0.3,max_value=30).display()
#usando reny con m aristas
grafo.grafo_AleatorioA(8,0.8,5,max_value=10).display()
# grafo conexo aleatorio
grafo.grafoConexo_Aleatorio(10,0.8,max_value=10).display()
print("------------------------------------------------------")

print("------------Usando conexividad----------------------")
#es conexo?
print(grafo.grafo_Aleatorio(6,0.25,max_value=30).is_conexo())
#n componentes
print(grafo.grafo_Aleatorio(6,0.25,max_value=30).get_Nconexo())
#es arbol?
print(grafo.grafo_Aleatorio(8,0.45,max_value=30).is_tree())
print("------------------------------------------------------")

print("----------------------Usando LCA-----------------------")
nodo3 = gf(8,graph_type="undirected",weighted=True)

nodo3.insert_edge(0,1,weight=2)
nodo3.insert_edge(0,2,weight=2)
nodo3.insert_edge(0,3,weight=2)
nodo3.insert_edge(1,4,weight=2)
nodo3.insert_edge(1,5,weight=2)
nodo3.insert_edge(4,7,weight=2)
nodo3.insert_edge(2,6,weight=2)

#LCA ingenuo
print(nodo3.LCA(5,7))


print("------------------------------------------------------")



