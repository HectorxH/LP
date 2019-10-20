package estructuras;

import java.util.LinkedList;
import java.util.List;

public class Empresa{
    private int PrecioBalon;
    private int PrecioLitro;

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

    public int getPrecioBalon() {
        return this.PrecioBalon;
    }

    public void setPrecioBalon(int precioBalon) {
        this.PrecioBalon = precioBalon;
    }

    public int getPrecioLitro() {
        return this.PrecioLitro;
    }

    public void setPrecioLitro(int precioLitro) {
        this.PrecioLitro = precioLitro;
    }

    public int getConsumo(){
        Vehiculo vehiculo = this.Vehiculos.get(0);
        return vehiculo.getConsumo();
    }
}
