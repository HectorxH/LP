package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Ciudad {
    private int id;
    private int nEdificios;
    private int nCasas;

    private List<Edificacion> Casas;
    private List<Edificacion> Edificios;

    public Ciudad(int id, int nEdificios, int nCasas){
        this.id = id;
        this.nEdificios = nEdificios;
        this.nCasas = nCasas;
        this.Casas = new LinkedList<>();
        this.Edificios = new LinkedList<>();
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

    public void newCasa(int consumo) {
        Edificacion casa = new Casa(consumo);
        this.Casas.add(casa);
    }

    public void newEdificio(int consumo) {
        Edificacion edificio = new Edificio(consumo);
        this.Edificios.add(edificio);
    }

    int consumoCasas() {
        int sum = 0;
        for(int i = 0; i < this.nCasas; i++){
            Edificacion casa = this.Casas.get(i);
            sum += casa.getConsumo();
        }
        return sum;
    }

    int consumoEdificios() {
        int sum = 0;
        for(int i = 0; i < this.nEdificios; i++){
            Edificacion edificio = this.Edificios.get(i);
            sum += edificio.getConsumo();
        }
        return sum;
    }
}
