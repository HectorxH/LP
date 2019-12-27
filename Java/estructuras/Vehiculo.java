package estructuras;

abstract class Vehiculo {

    //(int) (consumo) : Guarda el valor del consumo de un Vehiculo.
    private int consumo;

    Vehiculo(int consumo){
        this.consumo = consumo;
    }

    /** (getConsumo)
    --------------------
    Obtiene el valor de consumo de un Vehiculo.
    --------------------
    */
    public int getConsumo() {
        return this.consumo;
    }

    /** (setConsumo)
    (int) (consumo)
    --------------------
    Establece el valor de consumo de un Vehiculo.
    --------------------
    */
    public void setConsumo(int consumo) {
        this.consumo = consumo;
    }
}