def insert(tabla, fila_dat):	
	f1 = open(tabla+".csv", "r")
	linea = f1.readline()
	l1 = linea.strip().split(",")
	f1.close()

	string = ""
	f2 = open(tabla+".csv", "a")
	for rotulo in l1:
		if rotulo in fila_dat:
			string = string+fila_dat[rotulo] + ", "
	string = string[:-2]+"\n"

	f2.write(string)
	f2.close()

dicc = {"Nombre":"Sofia Polet", "Rut":"20183612-3", "Rol":"201873570-1", "Teléfono":"983642795"}
insert("Estudiantes", dicc)