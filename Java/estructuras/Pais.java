package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Pais implements Grafo {
    private int nNodes;
    private int nEdges;

    private Empresa Empresa;
    private Ciudad[] Ciudades;

    private boolean apsp = false;

    private int[][] adjMatrix;
    private int[][] dist;
    private int[][] path;
    private int[][] cost;

    public Pais(int nNodes, int nEdges, Empresa empresa) {
        this.nNodes = nNodes;
        this.nEdges = nEdges;
        this.Ciudades = new Ciudad[nNodes];
        this.adjMatrix = new int[nNodes][nNodes];
        this.dist = new int[nNodes][nNodes];
        this.path = new int[nNodes][nNodes];
        this.cost = new int[nNodes][nNodes];
        for(int i = 0; i < nNodes; i++){
            for(int j = 0; j < nNodes; j++){
                this.adjMatrix[i][j] = Grafo.INF;
                this.path[i][j] = -1;
                if(i == j) {
                    this.adjMatrix[i][j] = 0;
                    this.path[i][j] = 0;
                }
            }
        }
        this.Empresa = empresa;
    }

    @Override
    public int edgeWeight(int v, int u) {
        return this.adjMatrix[v][u];
    }

    private void floyd(){
        for(int i = 0; i < this.nNodes; i++){
            for(int j = 0; j < this.nNodes; j++){
                this.dist[i][j] = this.adjMatrix[i][j];
                if(this.dist[i][j] < Grafo.INF) this.path[i][j] = i;
            }
        }
        for(int k = 0; k < this.nNodes; k++) {
            for (int i = 0; i < this.nNodes; i++) {
                for (int j = 0; j < this.nNodes; j++) {
                    if(this.dist[i][k] + this.dist[k][j] < this.dist[i][j]){
                        this.dist[i][j] = this.dist[i][k] + this.dist[k][j];
                        this.path[i][j] = this.path[k][j];
                    }
                }
            }
        }
        for(int j = 0; j < this.nNodes; j++){
            Ciudad dest = this.Ciudades[j];
            for(int i = 0; i < this.nNodes; i++){
                this.cost[i][j] = this.dist[i][j] * (dest.getnCasas() + dest.getnEdificios());
            }
        }
        this.apsp = true;
    }

    @Override
    public List<Integer> shortestPath(int v, int u) {
        if(!this.apsp) this.floyd();
        List<Integer> p;
        if(this.path[v][u] == v) p = new LinkedList<>();
        else p = this.shortestPath(v, this.path[v][u]);
        p.add(this.path[v][u]);
        return p;
    }

    @Override
    public void addEdge(int v, int u, int w) {
        this.adjMatrix[v][u] = w;
        this.adjMatrix[u][v] = w;
    }

    @Override
    public void addNode(int v, Ciudad ciudad) {
        this.Ciudades[v] = ciudad;
    }

    public int getnNodes() {
        return this.nNodes;
    }

    public int getnEdges() {
        return this.nEdges;
    }

    public Empresa getEmpresa() {
        return Empresa;
    }

    public void setEmpresa(Empresa empresa) {
        Empresa = empresa;
    }
}
