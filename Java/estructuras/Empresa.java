package estructuras;

import java.util.List;

public class Empresa{
    private int PrecioBalon;
    private int PrecioLitro;

    private List<Vehiculo> Vehiculos;

    public int getPrecioBalon() {
        return PrecioBalon;
    }

    public void setPrecioBalon(int precioBalon) {
        PrecioBalon = precioBalon;
    }

    public int getPrecioLitro() {
        return PrecioLitro;
    }

    public void setPrecioLitro(int precioLitro) {
        PrecioLitro = precioLitro;
    }
}
