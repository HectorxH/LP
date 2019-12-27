package estructuras;

abstract class Edificacion {

    //(int) (consumo) : Guarda el valor del consumo de una Edificacion.
    private int consumo;

    Edificacion(int consumo) {
        this.consumo = consumo;
    }

    /** (getConsumo)
    --------------------
    Obtiene el valor de consumo de una Edificacion.
    --------------------
    */
    public int getConsumo() {
        return this.consumo;
    }

    /** (setConsumo)
    (int) (consumo)
    --------------------
    Establece el valor de consumo de una Edificacion.
    --------------------
    */
    public void setConsumo(int consumo) {
        this.consumo = consumo;
    }
}
