package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Ciudad {

    //(int) (id) : Raz´on de existir.
    private int id;

    //(int) (nEdificios) : Raz´on de existir.
    private int nEdificios;

    //(int) (nCasas) : Raz´on de existir.
    private int nCasas;

    //(List<Edificacion>) (Casas) : Raz´on de existir.
    private List<Edificacion> Casas;

    //(List<Edificacion>) (Edificios) : Raz´on de existir.
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
    Descripci´on breve
    --------------------
    */
    public int getId() {
        return this.id;
    }

    /** (setId)
    (int) (id)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void setId(int id) {
        this.id = id;
    }

    /** (getnEdificios)
    --------------------
    Descripci´on breve
    --------------------
    */
    public int getnEdificios() {
        return this.nEdificios;
    }

    /** (setnEdificios)
    (int) (nEdificios)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void setnEdificios(int nEdificios) {
        this.nEdificios = nEdificios;
    }

    /** (getnCasas)
    --------------------
    Descripci´on breve
    --------------------
    */
    public int getnCasas() {
        return this.nCasas;
    }

    /** (setnCasas)
    (int) (nCasas)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void setnCasas(int nCasas) {
        this.nCasas = nCasas;
    }

    /** (newCasa)
    (int) (consumo)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void newCasa(int consumo) {
        Edificacion casa = new Casa(consumo);
        this.Casas.add(casa);
    }

    /** (newEdificio)
    (int) (consumo)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void newEdificio(int consumo) {
        Edificacion edificio = new Edificio(consumo);
        this.Edificios.add(edificio);
    }

    /** (consumoCasas)
    --------------------
    Descripci´on breve
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
    Descripci´on breve
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
