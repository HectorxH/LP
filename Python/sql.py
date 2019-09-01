import re
from pprint import pprint as pp

class ColumnError(Exception):
    pass

class TableError(Exception):
    pass

select_regex = re.compile(
    r"^(SELECT) +((?:[^\s,='*\d][^\s,='*]*?(?: *, *[^\s,='*\d][^\s,='*]*?)*)|\*) +"
    r"(FROM) +([^\s,='*\d][^\s,='*]*?)"
    r"(?: +(INNER JOIN) +([^\s,='*\d][^\s,='*]*?))?"
    r"(?: +(WHERE) +([^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:[^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)?|-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:[^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)?|-?\d+(?:\.\d+)?|'[^']*'))*))?"
    r"(?: +(ORDER BY) +([^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)?) +(ASC|DESC))?;$")
insert_regex = re.compile(
    r"^(INSERT INTO) +([^\s,='*\d][^\s,='*]*?) +\( *([^\s,='*\d][^\s,='*]*?(?: *, *[^\s,='*\d][^\s,='*]*?)*) *\) +"
    r"(VALUES) +\( *((?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *(?:-?\d+(?:\.\d+)?|'[^']*'))*) *\);$")
update_regex = re.compile(
    r"^(UPDATE) +([^\s,='*\d][^\s,='*]*?) +"
    r"(SET) +([^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *[^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*) +"
    r"(WHERE) +([^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[^\s,='*\d][^\s,='*]*?(?:\.[^\s,='*\d][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*);$")

'''
commaSplit
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(lista) Output: Retorna una lista con los strings separados por comas ignorando espacios.
——————–
Extrae del string entregado los strings entre comas y espacios.
'''
def commaSplit(str):
    return re.split(r"'?(?: *),(?: *)'?", str.strip(" \n\'"))

'''
orSplit
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(lista) Output: Retorna una lista con los strings separados por OR ignorando espacios.
——————–
Extrae del string entregado los strings entre OR y espacios.
'''
def orSplit(str):
    return re.split(r"'?(?: +)OR(?: +)'?", str.strip(" \n\'"))

'''
andSplit
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(lista) Output: Retorna una lista con los strings separados por AND ignorando espacios.
——————–
Extrae del string entregado los strings entre AND y espacios.
'''
def andSplit(str):
    return re.split(r"'?(?: +)AND(?: +)'?", str.strip(" \n\'"))

'''
equalSplit
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(lista) Output: Retorna una lista con los strings separados por = ignorando espacios.
——————–
Extrae del string entregado los strings entre = y espacios.
'''
def equalSplit(str):
    return re.split(r"'?(?: *)=(?: *)'?", str.strip(" \n\'"))

'''
equalSplitVar
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(Tipo de dato) Output:
——————–
Descripción de la función.
'''
def equalSplitVar(str):
    return re.split(r"(?: *)=(?: *)", str.strip())

'''
hasTableName
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(bool) Output: Retorna TRUE si contiene . y FALSE si no.
——————–
Verifica si el string contiene un . para reconocer si para reconocer si es de la forma nombreTabla.nombreColumna
'''
def hasTableName(str):
    return '.' in str

'''
isColumn
——————–
Entradas:
(string) str: String entregado a la función
——————–
Salida:
(bool) Output: Retorna TRUE si es una columna y FALSE si no lo es.
——————–
Verifica si el string tiene el formato de una columna válida.
'''
def isColumn(str):
    return str[0].isalpha()

'''
isString
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(bool) Output: Retorna TRUE si es un string y FALSE si no lo es.
——————–
Verifica si el string contiene un ' para reconocer si hay un string.
'''
def isString(str):
    return '\'' in str

'''
check
——————–
Entradas:
(string) subexpr: Condición de la forma columna = valor o columna = columna.
(lista) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si se cumple la condición de subexpr y en FALSE si no la cumple.
——————–
Recibe una condición de la forma columna = valor o columna = columna y retorna una función que se evalúa en
TRUE o FALSE si cumple esta condición o no.
'''
def check(subexpr, cols1, table1 = "", cols2 = [], table2 = ""):
    if not cols2:
        (A, B) = equalSplit(subexpr)
        B.strip('\'')
        try:
            pos = cols1.index(A)
        except ValueError:
            print("Una columna solicitada no existe.")
            raise ColumnError
        return lambda row: row[pos] == B;
    else:
        (A, B) = equalSplitVar(subexpr)
        if hasTableName(A):
            (tableA, colA) = A.split('.')
            if isColumn(B):
                if hasTableName(B):
                    (tableB, colB) = B.split('.')
                    if tableA == table1 and tableB == table1:
                        try:
                            posA = cols1.index(colA)
                            posB = cols1.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        return lambda row1, row2: row1[posA] == row1[posB]
                    elif tableA == table1 and tableB == table2:
                        try:
                            posA = cols1.index(colA)
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        return lambda row1, row2: row1[posA] == row2[posB]
                    elif tableA == table2 and tableB == table1:
                        try:
                            posA = cols2.index(colA)
                            posB = cols1.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        return lambda row1, row2: row2[posA] == row1[posB]
                    elif tableA == table2 and tableB == table2:
                        try:
                            posA = cols2.index(colA)
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise tableError
                        return lambda row1, row2: row2[posA] == row2[posB]
                    else:
                        print("Una tabla indicada no existe.")
                        raise TableError
                else:
                    if tableA == table1:
                        try:
                            posA = cols1.index(colA)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        try:
                            posB = cols1.index(colB)
                            return lambda row1, row2: row1[posA] == row1[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row1[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada no existe.")
                                raise ColumnError
                    elif tableA == table2:
                        try:
                            posA = cols2.index(colA)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        try:
                            posB = cols1.index(colB)
                            return lambda row1, row2: row2[posA] == row1[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row2[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada no existe.")
                                raise ColumnError
                    else:
                        print("Una tabla indicada no existe.")
                        raise TableError
            else:
                B = B.strip('\'')
                if tableA == table1:
                    posA = cols1.index(colA)
                    return lambda row1, row2: row1[posA] == B
                else:
                    posA = cols2.index(colA)
                    return lambda row1, row2: row2[posA] == B
        else:
            colA = A
            if isColumn(B):
                if hasTableName(B):
                    if tableB == table1:
                        try:
                            posB = cols1.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        try:
                            posA = cols1.index(colA)
                            return lambda row1, row2: row1[posA] == row1[posB]
                        except ValueError:
                            try:
                                posA = cols2.index(colA)
                                return lambda row1, row2: row2[posA] == row1[posB]
                            except ValueError:
                                print("Una columna solicitada no existe.")
                                raise ColumnError
                    elif tableB == table2:
                        try:
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
                        try:
                            posA = cols1.index(colA)
                            return lambda row1, row2: row1[posA] == row2[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row2[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada no existe.")
                                raise ColumnError
                else:
                    try:
                        posA = cols1.index(colA)
                        try:
                            posB = cols1.index(colB)
                            return lambda row1, row2: row1[posA] == row1[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row1[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada no existe.")
                                raise ColumnError
                    except ValueError:
                        try:
                            posA = cols2.index(colA)
                            try:
                                posB = cols1.index(colB)
                                return lambda row1, row2: row2[posA] == row1[posB]
                            except ValueError:
                                try:
                                    posB = cols2.index(colB)
                                    return lambda row1, row2: row2[posA] == row2[posB]
                                except ValueError:
                                    print("Una columna solicitada no existe.")
                                    raise ColumnError
                        except ValueError:
                            print("Una columna solicitada no existe.")
                            raise ColumnError
            else:
                B = B.strip('\'')
                try:
                    posA = cols1.index(colA)
                    return lambda row1, row2: row1[posA] == B
                except ValueError:
                    try:
                        posA = cols2.index(colA)
                        return lambda row1, row2: row2[posA] == B
                    except ValueError:
                        print("Una columna solicitada no existe.")
                        raise ColumnError

'''
exprToBool
——————–
Entradas:
(string) expr: Condición que solo puede contener AND.
(lista) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si la(s) lista(s) cumplen con la condición ingresada y FALSE si no la cumple.
——————–
Recibe un string que lo separa por AND. Luego llama a la función check y le entrega cada uno de estos strings.
'''
def exprToBool(expr, cols1, table1 = "", cols2 = [], table2 = ""):
    expr = andSplit(expr)
    expr = [check(subexpr, cols1, table1, cols2, table2) for subexpr in expr]
    if not cols2:
        return lambda row: all([subexpr(row) for subexpr in expr])
    else:
        return lambda row1, row2: all([subexpr(row1, row2) for subexpr in expr])

'''
stmtToBool
——————–
Entradas:
(string) stmt: Condición ingresada para WHERE.
(lista) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si la(s) lista(s) cumplen con la condición ingresada y FALSE si no la cumple.
——————–
Recibe la condición para WHERE y retorna una función que se evalúa en TRUE o FALSE si cumple esta condición o no.
'''
def stmtToBool(stmt, cols1, table1 = "", cols2 = [], table2 = ""):
    stmt = orSplit(stmt)
    stmt = [exprToBool(expr, cols1, table1, cols2, table2) for expr in stmt]
    if not cols2:
        return lambda row: any([expr(row) for expr in stmt])
    else:
        return lambda row1, row2: any([expr(row1, row2) for expr in stmt])

'''
select
——————–
Entradas:
(lista) sel: Lista de columnas que se quieren mostrar, contiene solo '*' si se quieren mostrar todas las columnas.
(string) table: Tabla a la que se le quiere hacer SELECT.
(string) inner: Tabla a la que se le quiere hacer INNER JOIN.
(string) where: Condición para WHERE.
(string) order_by: Columna que se quiere ordenar.
(string) order_type: Ordenar de manera adcendente o descendente.
——————–
Salida:
(void) Output: No retorna.
——————–
Imprime los datos de la tabla que son especificados.
Puede juntar columnas de distintas tablas y ordenarlas de forma ascendente y descendente.
'''
def select(match):
    select = commaSplit(match[2])
    table = match[4]
    inner = match[6]
    where = match[8]
    order_by = match[10]
    order_type = match[11]

    out = []
    cols = []
    try:
        file = open(table+".csv", 'r', encoding="utf-8-sig");
    except FileNotFoundError:
        print("La tabla solicitada no existe.")
        return
    if not inner:
        with file:
            cols = file.readline().strip().split(",")
            try:
                stmt = stmtToBool(where, cols) if where else lambda *_: True
            except (ColumnError, TableError):
                return
            for line in file:
                row = line.strip().split(",")
                if stmt(row):
                    out.append(row)
    else:
        try:
            join_file = open(inner+".csv", 'r', encoding="utf-8-sig")
        except FileNotFoundError:
            print("La tabla solicitada en INNER JOIN no existe.")
        with file, join_file:
            cols1 = file.readline().strip().split(",")
            cols2 = join_file.readline().strip().split(",")
            cols = cols1+cols2
            join_lines = join_file.read().splitlines()
            try:
                stmt = stmtToBool(where, cols1, table, cols2, inner)
            except (ColumnError, TableError):
                return
            for line in file:
                row1 = line.strip().split(",")
                for join_line in join_lines:
                    row2 = join_line.strip().split(",")
                    if stmt(row1, row2):
                        out.append(row1+row2)

    select = range(len(cols)) if "*" in select else list(map(lambda col: cols.index(col), select))
    if order_by:
        i = cols.index(order_by)
        out = sorted(out, key=lambda l: l[i])
        if order_type == "DESC":
            out = reversed(out)

    for line in out:
        string = ""
        for col in select:
            string = string + line[col] + "   "
        string = string[:-1]
        print(string)
    if not out:
        print("La informacion solicitada no existe.")

'''
insert
——————–
Entradas:
(string) table: Nombre de la tabla a la que se le insertará datos.
(diccionario) row_dat: Diccionario que contiene los datos que se ingresarán.
——————–
Salida:
(void) Output: No retorna.
——————–
Añade una fila al final de la tabla entregada a la función con los datos que se han ingresado.
'''
def insert(table, row_dat):
    cols = ""
    contador = 0

    try:
        file = open(table+".csv", "r", encoding='utf-8-sig')
    except FileNotFoundError:
        print("La tabla solicitada no existe.")
        return
    else:
        with file:
            cols = file.readline().strip().split(",")
    string = ""

    with open(table+".csv", "a", encoding='utf-8-sig') as file:
        for col in cols:
            if col in row_dat:
                string = string + row_dat[col] + ","
                contador+=1
            else:
                string = string + "" + ","
        string = string[:-1] + "\n"

        if len(row_dat) > contador:
            print("No se pudo ingresar uno de los datos ya que no existe su columna respectiva.")
            return
        else:
            file.write(string)

    print("Se ha insertado 1 fila.")

'''
update
——————–
Entradas:
(string) table: Nombre de la tabla a la que se le actualizarán los datos.
(lista de strings) set: Lista con el nombre de la columna que se quiere cambiar junto con el valor al cual se quiere actualizar.
(string) stmt: Condición que se debe cumplir para cambiar el valor que corresponde a esa fila.
——————–
Salida:
(void) Output: No retorna.
——————–
Actualiza la tabla entregada a la función con los valores han sido ingresados.
'''
def update(table, set, stmt):
    count = 0

    try:
        file = open(table+".csv", "r", encoding='utf-8-sig')
    except FileNotFoundError:
        print("La tabla solicitada no existe.")
        return
    else:
        with file:
            lines = file.read().splitlines()

    with open(table+".csv", "w", encoding='utf-8-sig') as file:
        cols = lines[0].strip().split(",")
        try:
            set[0] = cols.index(set[0])
        except ValueError:
            print("Una columna indicada no existe.")
            for line in lines:
                file.write(','.join(line)+'\n')
            return
        try:
            stmt = stmtToBool(stmt, cols)
        except (ColumnError, TableError):
            stmt = lambda *_: False

        for line in lines:
            line = line.strip().split(",")
            if stmt(line):
                line[set[0]] = set[1]
                count += 1
            line = ','.join(line)+'\n'
            file.write(line)

    if count == 0:
        print("No se han actualizado filas.")
    elif count == 1:
        print("Se ha actualizado 1 fila.")
    else:
        print("Se han actualizado {} filas.".format(count))

running = True
print("Para salir ingrese el comando EXIT;")
while running:
    query = str(input("Ingrese su query: "))

    select_match = re.fullmatch(select_regex, query)
    insert_match = re.fullmatch(insert_regex, query)
    update_match = re.fullmatch(update_regex, query)

    if select_match:
        if select_match[5] and not select_match[7]: #INNER JOIN sin un WHERE
            print("Error de Sintaxis!")
        else:
            select(select_match)
    elif insert_match:
        table = insert_match[2]
        keys = commaSplit(insert_match[3])
        values = commaSplit(insert_match[5])

        if len(keys) != len(values):
            print("Error de Sintaxis!")
        else:
            row_dat = dict(zip(keys,values))
            insert(table, row_dat)

    elif update_match:
        table = update_match[2]
        set = equalSplit(update_match[4])
        stmt = update_match[6]
        update(table, set, stmt)

    elif query == "EXIT;":
        running = False
    else:
        print("Error de Sintaxis!")
