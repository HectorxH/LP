package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Empresa{

    //(int) (PrecioBalon) : Guarda el valor del precio del Balon de gas.
    private int PrecioBalon;

    //(int) (PrecioLitro) : Guarda el valor del precio del Litro de gas.
    private int PrecioLitro;

    //(List<Vehiculo>) (Vehiculos) : Guarda los Vehiculos de la Empresa en una lista.
    private List<Vehiculo> Vehiculos;

    public Empresa(int precioBalon, int precioLitro, int kilometros) {
        this.PrecioBalon = precioBalon;
        this.PrecioLitro = precioLitro;

        this.Vehiculos = new LinkedList<>();
        Vehiculo camionCisterna = new CamionCisterna(kilometros);
        this.Vehiculos.add(camionCisterna);
        Vehiculo camioneta = new Camioneta(kilometros);
        this.Vehiculos.add(camioneta);
    }

    /** (getPrecioBalon)
    --------------------
    Obtiene el precio del Balon de gas.
    --------------------
    */
    public int getPrecioBalon() {
        return this.PrecioBalon;
    }

    /** (setPrecioBalon)
    (int) (precioBalon)
    --------------------
    Establece el precio del Balon de gas.
    --------------------
    */
    public void setPrecioBalon(int precioBalon) {
        this.PrecioBalon = precioBalon;
    }

    /** (getPrecioLitro)
    --------------------
    Obtiene el precio del Litro de gas.
    --------------------
    */
    public int getPrecioLitro() {
        return this.PrecioLitro;
    }

    /** (setPrecioLitro)
    (int) (precioLitro)
    --------------------
    Establece el precio del Litro de gas.
    --------------------
    */
    public void setPrecioLitro(int precioLitro) {
        this.PrecioLitro = precioLitro;
    }

    /** (getConsumo)
    --------------------
    Obtiene el consumo de los Vehiculos de la Empresa.
    --------------------
    */
    public int getConsumo(){
        Vehiculo vehiculo = this.Vehiculos.get(0);
        return vehiculo.getConsumo();
    }
}
