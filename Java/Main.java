import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Arrays;

class Main {
    public static void main(String[] args) throws FileNotFoundException{
        Pais p = mapa();
        Empresa emp = empresa(p);
        edificaciones(p);

        int ciudadOptima = p.ciudadOptima();
        system.out.println("La ciudad "+ciudadOptima+" es la ubicación optima.");

        for(int i=0; i < p.getnNodes(); i++){
            System.out.println("ciudad "+i+":");
            System.out.println("- Utilidad: "+p.getUtilidad(i));
            int[] nVehiculos;
            System.out.println("- Se utilizaron "); // NO SE CUANTOS CAMIONES Y CAMIONETAS AAAAAAAAAAAAAAAAAAA
        }
    }

    public static Pais mapa() throws FileNotFoundException{
        File file = new File("mapa.txt");
        Scanner sc = new Scanner(file);

        int nCiudades = sc.nextInt();
        int nCaminos = sc.nextInt();
        Pais p = new Pais(nCiudades, nCaminos);

        for(int i=0; i < nCaminos; i++){
            int origen = sc.nextInt();
            int destino = sc.nextInt();
            int peso = sc.nextInt();

            p.addEdge(origen, destino, peso);
        }

        return p;
    }

    public static Empresa empresa() throws FileNotFoundException{
        File file = new File("empresa.txt");
        Scanner sc = new Scanner(file);

        int balon_gas = sc.nextInt();
        int litro_gas = sc.nextInt();
        int kilometros = sc.nextInt();

        return new Empresa(balon_gas, litro_gas, kilometros);
    }

    public static void edificaciones(Pais p) throws FileNotFoundException{
        File file = new File("edificaciones.txt");
        Scanner sc = new Scanner(file);

        int cantCiudad = p.getnNodes();

        for(int i=0; i < cantCiudad; i++){
            int id = sc.nextInt();
            int nCasas = sc.nextInt();
            int nEdificios = sc.nextInt();

            Ciudad c = new Ciudad(id, nCasas, nEdificios);

            for(int i=0; i < nCasas; i++){
                int consumo = sc.nextInt();
                c.newCasa(consumo);
            }
            for(int i=0; i < nEdificios; i++){
                int consumo = sc.nextInt();
                c.newEdificio(consumo);
            }
            p.addNode(id, c);
        }
    }
}
