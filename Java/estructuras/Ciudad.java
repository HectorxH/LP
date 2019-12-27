package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Ciudad {

    //(int) (id) : Guarda el identificador de la Ciudad.
    private int id;

    //(int) (nEdificios) : Guarda el numero de Edificios de la Ciudad.
    private int nEdificios;

    //(int) (nCasas) : Guarda el numero de Casas de la Ciudad.
    private int nCasas;

    //(List<Edificacion>) (Casas) : Guarda las Casas de una Ciudad en una lista.
    private List<Edificacion> Casas;

    //(List<Edificacion>) (Edificios) : Guarda los Edificios de una Ciudad en una lista.
    private List<Edificacion> Edificios;

    public Ciudad(int id, int nCasas, int nEdificios){
        this.id = id;
        this.nEdificios = nEdificios;
        this.nCasas = nCasas;
        this.Casas = new LinkedList<>();
        this.Edificios = new LinkedList<>();
    }

    /** (getId)
    --------------------
    Obtiene el identificador de la Ciudad.
    --------------------
    */
    public int getId() {
        return this.id;
    }

    /** (setId)
    (int) (id)
    --------------------
    Establece el identificador de la Ciudad.
    --------------------
    */
    public void setId(int id) {
        this.id = id;
    }

    /** (getnEdificios)
    --------------------
    Obtiene el numero de edificios de la Ciudad.
    --------------------
    */
    public int getnEdificios() {
        return this.nEdificios;
    }

    /** (setnEdificios)
    (int) (nEdificios)
    --------------------
    Establece el numero de edificios de la Ciudad.
    --------------------
    */
    public void setnEdificios(int nEdificios) {
        this.nEdificios = nEdificios;
    }

    /** (getnCasas)
    --------------------
    Obtiene el numero de casas de la Ciudad.
    --------------------
    */
    public int getnCasas() {
        return this.nCasas;
    }

    /** (setnCasas)
    (int) (nCasas)
    --------------------
    Establece el numero de casas de la Ciudad.
    --------------------
    */
    public void setnCasas(int nCasas) {
        this.nCasas = nCasas;
    }

    /** (newCasa)
    (int) (consumo)
    --------------------
    Crea una Casa con su respectivo consumo.
    --------------------
    */
    public void newCasa(int consumo) {
        Edificacion casa = new Casa(consumo);
        this.Casas.add(casa);
    }

    /** (newEdificio)
    (int) (consumo)
    --------------------
    Crea un Edificio con su respectivo consumo.
    --------------------
    */
    public void newEdificio(int consumo) {
        Edificacion edificio = new Edificio(consumo);
        this.Edificios.add(edificio);
    }

    /** (consumoCasas)
    --------------------
    Obtiene el consumo total de las Casas de la Ciudad.
    --------------------
    */
    int consumoCasas() {
        int sum = 0;
        for(int i = 0; i < this.nCasas; i++){
            Edificacion casa = this.Casas.get(i);
            sum += casa.getConsumo();
        }
        return sum;
    }

    /** (consumoEdificios)
    --------------------
    Obtiene el consumo total de los Edificios de la Ciudad.
    --------------------
    */
    int consumoEdificios() {
        int sum = 0;
        for(int i = 0; i < this.nEdificios; i++){
            Edificacion edificio = this.Edificios.get(i);
            sum += edificio.getConsumo();
        }
        return sum;
    }
}
