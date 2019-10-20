package estructuras;

abstract class Vehiculo {
    private int consumo;

    Vehiculo(int consumo){
        this.consumo = consumo;
    }

    public int getConsumo() {
        return this.consumo;
    }

    public void setConsumo(int consumo) {
        this.consumo = consumo;
    }
}