import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import estructuras.Pais;
import estructuras.Empresa;
import estructuras.Ciudad;

class Main {
    public static void main(String[] args) throws FileNotFoundException{
        Empresa emp = empresa();
        Pais p = mapa(emp);
        edificaciones(p);

        int ciudadOptima = p.ciudadOptima();
        String format = String.format("La ciudad %d es la ubicación optima.", ciudadOptima);
        System.out.println(format);

        int nNodes = p.getnNodes();
        for(int i=0; i < nNodes; i++){
            format = String.format("ciudad %d:", i);
            System.out.println(format);
            format = String.format("- Utilidad: %d", p.getUtilidad(i));
            System.out.println(format);
            int nCamiones = p.getnCamiones(i);
            int nCamionetas = p.getnCamionetas(i);
            format = String.format("- Se utilizaron %d camiones cisterna y %d camionetas", nCamiones, nCamionetas);
            System.out.println(format); // NO SE CUANTOS CAMIONES Y CAMIONETAS AAAAAAAAAAAAAAAAAAA
        }
    }

    private static Pais mapa(Empresa emp) throws FileNotFoundException{
        File file = new File("mapa.txt");
        Scanner sc = new Scanner(file);

        int nCiudades = sc.nextInt();
        int nCaminos = sc.nextInt();
        Pais p = new Pais(nCiudades, nCaminos, emp);

        for(int i = 0; i < nCaminos; i++){
            int origen = sc.nextInt();
            int destino = sc.nextInt();
            int peso = sc.nextInt();

            p.addEdge(origen, destino, peso);
        }
        sc.close();
        return p;
    }

    private static Empresa empresa() throws FileNotFoundException{
        File file = new File("empresa.txt");
        Scanner sc = new Scanner(file);

        int balonGas = sc.nextInt();
        int litroGas = sc.nextInt();
        int kilometros = sc.nextInt();

        return new Empresa(balonGas, litroGas, kilometros);
    }

    private static void edificaciones(Pais p) throws FileNotFoundException{
        File file = new File("edificaciones.txt");
        Scanner sc = new Scanner(file);

        int cantCiudad = p.getnNodes();

        for(int i=0; i < cantCiudad; i++){
            int id = sc.nextInt();
            int nCasas = sc.nextInt();
            int nEdificios = sc.nextInt();

            Ciudad ciudad = new Ciudad(id, nCasas, nEdificios);

            for(int j = 0; j < nCasas; j++){
                int consumo = sc.nextInt();
                ciudad.newCasa(consumo);
            }
            for(int j=0; j < nEdificios; j++){
                int consumo = sc.nextInt();
                ciudad.newEdificio(consumo);
            }
            p.addNode(id, ciudad);
        }
        sc.close();
    }
}
