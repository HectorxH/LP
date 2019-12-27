package estructuras;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class Pais implements Grafo {

    //(List<Integer>) (minId) : Guarda los nodos optimos en una lista.
    private List<Integer> minId;

    //(int) (nNodes) : Guarda el numero de nodos del pais.
    private int nNodes;

    //(int) (nEdges) : Guarda el numero de aristas del pais.
    private int nEdges;

    //(Empresa) (Empresa) : Guarda una Empresa.
    private Empresa Empresa;

    //(Ciudad) (Ciudades) : Guarda Ciudades en un arreglo.
    private Ciudad[] Ciudades;

    //(boolean) (floydBool) : Es True si la distancia calculada es minima para el pais actual y False en caso contrario.
    private boolean floydBool;

    //(int) (adjMatrix) : Guarda la matriz de adjacencia del grafo.
    private int[][] adjMatrix;

    //(int) (dist) : Guarda la distancia entre par de nodos.
    private int[][] dist;

    //(int) (path) : Guarda la informacion necesaria para reconstruir el camino mas corto.
    private int[][] path;

    //(int) (cost) : Guarda el costo entre par de nodos.
    private int[][] cost;

    public Pais(int nNodes, int nEdges, Empresa empresa) {
        this.nNodes = nNodes;
        this.nEdges = nEdges;
        this.Empresa = empresa;
        this.floydBool = false;

        this.Ciudades = new Ciudad[nNodes];
        this.minId = new LinkedList<>();

        this.adjMatrix = new int[nNodes][nNodes];
        this.dist = new int[nNodes][nNodes];
        this.path = new int[nNodes][nNodes];
        this.cost = new int[nNodes][nNodes];

        for(int i = 0; i < nNodes; i++) {
            for (int j = 0; j < nNodes; j++) {
                this.adjMatrix[i][j] = Grafo.INF;
                this.path[i][j] = -1;
            }
            this.adjMatrix[i][i] = 0;
            this.path[i][i] = 0;
        }
    }

    /** (edgeWeight)
    (int) (v)
    (int) (u)
    --------------------
    Establece el peso de una arista.
    --------------------
    */
    public int edgeWeight(int v, int u) {
        System.out.println("Added edge");
        return this.adjMatrix[v][u];
    }

    /** (init)
    --------------------
    Crea un grafo.
    --------------------
    */
    private void init(){
        for(int i = 0; i < this.nNodes; i++){
            for(int j = 0; j < this.nNodes; j++){
                this.dist[i][j] = this.adjMatrix[i][j];
                if(this.dist[i][j] < Grafo.INF) this.path[i][j] = i;
            }
        }
    }

    /** (setCosts)
    --------------------
    Establece los costos de una Empresa.
    --------------------
    */
    private void setCosts(){
        int consumo = this.Empresa.getConsumo();
        for(int j = 0; j < this.nNodes; j++){
            Ciudad dest = this.Ciudades[j];
            for(int i = 0; i < this.nNodes; i++)
                this.cost[i][j] = 2 * this.dist[i][j] * (getnCamiones(j) + getnCamionetas(j)) * consumo;
        }
    }

    /** (floyd)
    --------------------
    Calcula la distancia minima entre todos los pares de nodos.
    --------------------
    */
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

    /** (shortestPath)
    (int) (v)
    (int) (u)
    --------------------
    Retorna el camino mas corto desde el nodo v hasta el nodo u.
    --------------------
    */
    public List<Integer> shortestPath(int v, int u) {
        if(!this.floydBool) this.floyd();
        List<Integer> p;
        if(this.path[v][u] == v) p = new LinkedList<>();
        else p = this.shortestPath(v, this.path[v][u]);
        p.add(this.path[v][u]);
        return p;
    }

    /** (addEdge)
    (int) (v)
    (int) (u)
    (int) (w)
    --------------------
    Agrega una arista de v a u con el peso w.
    --------------------
    */
    public void addEdge(int v, int u, int w) {
        this.adjMatrix[v][u] = w;
        this.adjMatrix[u][v] = w;
    }

    /** (addNode)
    (int) (v)
    (Ciudad) (ciudad)
    --------------------
    Agrega un nodo v a la ciudad.
    --------------------
    */
    public void addNode(int v, Ciudad ciudad) {
        this.Ciudades[v] = ciudad;
    }

    /** (getnNodes)
    --------------------
    Obtiene el numero de nodos del Pais.
    --------------------
    */
    public int getnNodes() {
        return this.nNodes;
    }

    /** (getnEdges)
    --------------------
    Obitene el numero de aristas del Pais.
    --------------------
    */
    public int getnEdges() {
        return this.nEdges;
    }

    /** (getEmpresa)
    --------------------
    Obtiene una Empresa.
    --------------------
    */
    public Empresa getEmpresa() {
        return this.Empresa;
    }

    /** (setEmpresa)
    (Empresa) (empresa)
    --------------------
    Establece una Empresa.
    --------------------
    */
    public void setEmpresa(Empresa empresa) {
        this.Empresa = empresa;
    }

    /** (calcMin)
    --------------------
    Calcula las ciudades optimas.
    --------------------
    */
    private void calcMin(){
        if(!this.floydBool) this.floyd();

        int minVal = Grafo.INF;
        for(int i = 0; i < this.nNodes; i++){
            int currVal = 0;
            for(int j = 0; j < this.nNodes; j++){
                currVal += this.cost[i][j];
            }
            if(currVal < minVal){
                this.minId = new LinkedList<>();
                minVal = currVal;
            }
            if(currVal <= minVal) this.minId.add(i);
        }
    }

    /** (ciudadesOptimas)
    --------------------
    Retorna una lista con las ciudades optimas.
    --------------------
    */
    public List<Integer> ciudadesOptimas() {
        if(this.minId.isEmpty()) this.calcMin();
        return this.minId;
    }

    /** (getUtilidad)
    (int) (src)
    (int) (dest)
    --------------------
    Obtiene la utilidad desde un nodo de origen src hasta el nodo destino dest.
    --------------------
    */
    public int getUtilidad(int src, int dest) {
        Ciudad ciudad = this.Ciudades[dest];

        int precioBalon = this.Empresa.getPrecioBalon();
        int precioLitro = this.Empresa.getPrecioLitro();

        int consumoCasas = ciudad.consumoCasas();
        int consumoEdificios = ciudad.consumoEdificios();

        return precioBalon*consumoCasas + precioLitro*consumoEdificios- this.cost[src][dest];
    }

    /** (getnCamiones)
    (int) (i)
    --------------------
    Obtiene el numero de camiones.
    --------------------
    */
    public int getnCamiones(int i){
        Ciudad ciudad = this.Ciudades[i];
        return ciudad.getnEdificios();
    }

    /** (getnCamionetas)
    (int) (i)
    --------------------
    Obtiene el numero de camionetas.
    --------------------
    */
    public int getnCamionetas(int i){
        Ciudad ciudad = this.Ciudades[i];
        return (ciudad.getnCasas() > 0)? 1 : 0;

    }
}
