package estructuras;

public class Ciudad {
    private int id;
    private int nEdificios;
    private int nCasas;

    private Edificacion[] edificaciones;

    public Ciudad(int id, int nEdificios, int nCasas){
        this.id = id;
        this.nEdificios = nEdificios;
        this.nCasas = nCasas;
        this.edificaciones = new Edificacion[nEdificios+nCasas];
    }

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getnEdificios() {
        return this.nEdificios;
    }

    public void setnEdificios(int nEdificios) {
        this.nEdificios = nEdificios;
    }

    public int getnCasas() {
        return this.nCasas;
    }

    public void setnCasas(int nCasas) {
        this.nCasas = nCasas;
    }
}
