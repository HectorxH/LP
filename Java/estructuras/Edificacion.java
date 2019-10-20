package estructuras;

abstract class Edificacion {
    private int consumo;

    Edificacion(int consumo) {
        this.consumo = consumo;
    }

    public int getConsumo() {
        return this.consumo;
    }

    public void setConsumo(int consumo) {
        this.consumo = consumo;
    }
}
