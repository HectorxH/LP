package estructuras;

import java.util.LinkedList;
import java.util.List;

public interface Grafo {
    public static final float INF = 1000000007.0F;

    public float edgeWeight(int v, int u);
    public List<Integer> shortestPath(int v, int u);
    public void addEdge(int v, int u, float w);
    public void addNode(int v);
}
