import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;

import estructuras.Pais;
import estructuras.Empresa;
import estructuras.Ciudad;

class Main {
    public static void main(String[] args) throws FileNotFoundException{
        Empresa emp = empresa();
        Pais p = mapa(emp);
        edificaciones(p);

        String format;

        List<Integer> ciudadesOptimas = p.ciudadesOptimas();
        int nOptimas = ciudadesOptimas.size();
        if(nOptimas == 1)
            format = String.format("La ciudad %d es la ubicación optima.\n", ciudadesOptimas.get(0));
        else
            format = String.format("Las ciudades %s son la ubicación optima.\n", ciudadesOptimas.toString());
        System.out.println(format);

        int nNodes = p.getnNodes();
        for(int dest = 0; dest < nNodes; dest++){
            format = String.format("ciudad %d:", dest);
            System.out.println(format);

            for (int src : ciudadesOptimas) {
                int util = p.getUtilidad(src, dest);

                if(nOptimas == 1)
                    format = String.format("- Utilidad: %d", util);
                else
                    format = String.format("- Utilidad desde %d: %d", src, util);
                System.out.println(format);
            }

            int nCamiones = p.getnCamiones(dest);
            int nCamionetas = p.getnCamionetas(dest);

            format = String.format("- Se utilizaron %d camiones cisterna y %d camionetas", nCamiones, nCamionetas);
            System.out.println(format);
            System.out.println();
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

        sc.close();

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
