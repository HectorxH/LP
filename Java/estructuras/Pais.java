package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Pais implements Grafo {
    private int maxId = -1;

    private int nNodes;
    private int nEdges;

    private Empresa Empresa;
    private Ciudad[] Ciudades;

    private boolean floydBool;

    private int[][] adjMatrix;
    private int[][] dist;
    private int[][] path;
    private int[][] cost;

    public Pais(int nNodes, int nEdges, Empresa empresa) {
        this.nNodes = nNodes;
        this.nEdges = nEdges;
        this.Empresa = empresa;
        this.floydBool = false;

        this.Ciudades = new Ciudad[nNodes];

        this.adjMatrix = new int[nNodes][nNodes];
        this.dist = new int[nNodes][nNodes];
        this.path = new int[nNodes][nNodes];
        this.cost = new int[nNodes][nNodes];

        for(int i = 0; i < nNodes; i++) {
            for (int j = 0; j < nNodes; j++) {
                this.adjMatrix[i][j] = Grafo.INF;
                this.path[i][j] = -1;
                if (i == j) {
                    this.adjMatrix[i][j] = 0;
                    this.path[i][j] = 0;
                }
            }
        }
    }

    public int edgeWeight(int v, int u) {
        return this.adjMatrix[v][u];
    }

    private void init(){
        for(int i = 0; i < this.nNodes; i++){
            for(int j = 0; j < this.nNodes; j++){
                this.dist[i][j] = this.adjMatrix[i][j];
                if(this.dist[i][j] < Grafo.INF) this.path[i][j] = i;
            }
        }
    }

    private void setCosts(){
        for(int j = 0; j < this.nNodes; j++){
            Ciudad dest = this.Ciudades[j];
            for(int i = 0; i < this.nNodes; i++){
                int hayCasas = (dest.getnCasas() > 0)? 1 : 0;
                this.cost[i][j] = 2 * this.dist[i][j] * (hayCasas + dest.getnEdificios());
            }
        }
    }

    private void floyd(){
        this.init();
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
        this.setCosts();
        this.floydBool = true;
    }

    public List<Integer> shortestPath(int v, int u) {
        if(!this.floydBool) this.floyd();
        List<Integer> p;
        if(this.path[v][u] == v) p = new LinkedList<>();
        else p = this.shortestPath(v, this.path[v][u]);
        p.add(this.path[v][u]);
        return p;
    }

    public void addEdge(int v, int u, int w) {
        this.adjMatrix[v][u] = w;
        this.adjMatrix[u][v] = w;
    }

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
        return this.Empresa;
    }

    public void setEmpresa(Empresa empresa) {
        this.Empresa = empresa;
    }

    private void calcMax(){
        int maxVal = 0;
        for(int i = 0; i < this.nNodes; i++){
            int currVal = 0;
            for(int j = 0; j < this.nNodes; j++){
                currVal += this.cost[i][j];
            }
            if(currVal > maxVal){
                this.maxId = i;
                maxVal = currVal;
            }
        }
    }

    public int ciudadOptima() {
        if(this.maxId == -1) this.calcMax();
        return this.maxId;
    }

    public int getUtilidad(int id) {
        if(this.maxId == -1) this.calcMax();
        Ciudad ciudad = this.Ciudades[id];

        int precioBalon = this.Empresa.getPrecioBalon();
        int precioLitro = this.Empresa.getPrecioLitro();

        int consumoCasas = ciudad.consumoCasas();
        int consumoEdificios = ciudad.consumoEdificios();

        return precioBalon*consumoCasas + precioLitro*consumoEdificios- this.cost[this.maxId][id];
    }
}
