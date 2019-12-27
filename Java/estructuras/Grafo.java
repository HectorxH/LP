package estructuras;

import java.util.List;

public interface Grafo {

	//(int) (INF) : Raz´on de existir.
    int INF = 1000000007;

    int edgeWeight(int v, int u);
    List<Integer> shortestPath(int v, int u);
    void addEdge(int v, int u, int w);
    void addNode(int v, Ciudad ciudad);
    int getnEdges();
    int getnNodes();
}
