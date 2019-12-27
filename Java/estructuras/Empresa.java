package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Empresa{

    //(int) (PrecioBalon) : Raz´on de existir.
    private int PrecioBalon;

    //(int) (PrecioLitro) : Raz´on de existir.
    private int PrecioLitro;

    //(List<Vehiculo>) (Vehiculos) : Raz´on de existir.
    private List<Vehiculo> Vehiculos;

    public Empresa(int precioBalon, int precioLitro, int kilometros) {
        this.PrecioBalon = precioBalon;
        this.PrecioLitro = precioLitro;

        //No estoy seguro para que usar los vehiculos
        this.Vehiculos = new LinkedList<>();
        Vehiculo camionCisterna = new CamionCisterna(kilometros);
        this.Vehiculos.add(camionCisterna);
        Vehiculo camioneta = new Camioneta(kilometros);
        this.Vehiculos.add(camioneta);
    }

    /** (getPrecioBalon)
    --------------------
    Descripci´on breve
    --------------------
    */
    public int getPrecioBalon() {
        return this.PrecioBalon;
    }

    /** (setPrecioBalon)
    (int) (precioBalon)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void setPrecioBalon(int precioBalon) {
        this.PrecioBalon = precioBalon;
    }

    /** (getPrecioLitro)
    --------------------
    Descripci´on breve
    --------------------
    */
    public int getPrecioLitro() {
        return this.PrecioLitro;
    }

    /** (setPrecioLitro)
    (int) (precioLitro)
    --------------------
    Descripci´on breve
    --------------------
    */
    public void setPrecioLitro(int precioLitro) {
        this.PrecioLitro = precioLitro;
    }

    /** (getConsumo)
    --------------------
    Descripci´on breve
    --------------------
    */
    public int getConsumo(){
        Vehiculo vehiculo = this.Vehiculos.get(0);
        return vehiculo.getConsumo();
    }
}
