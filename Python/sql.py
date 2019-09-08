import re
from pprint import pprint as pp

class ColumnError(Exception):
    pass

class TableError(Exception):
    pass

select_regex = re.compile(
    r"^(SELECT) +((?:[a-zA-Z][^\s,='*;.]*?(?: *, *[a-zA-Z][^\s,='*;.]*?)*)|\*) +"
    r"(FROM) +([a-zA-Z][^\s,='*;.]*?)"
    r"(?: +(INNER JOIN) +([a-zA-Z][^\s,='*;.]*?))?"
    r"(?: +(WHERE) +([a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:[a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)?|-?\d+(?:\.\d+)?|'[^']*') *(?: +(?:AND|OR) +[a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:[a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)?|-?\d+(?:\.\d+)?|'[^']*'))*))?"
    r"(?: +(ORDER BY) +([a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)?) +(ASC|DESC))?;$")
insert_regex = re.compile(
    r"^(INSERT INTO) +([a-zA-Z][^\s,='*;.]*?) +\( *([a-zA-Z][^\s,='*;.]*?(?: *, *[a-zA-Z][^\s,='*;.]*?)*) *\) +"
    r"(VALUES) +\( *((?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *(?:-?\d+(?:\.\d+)?|'[^']*'))*) *\);$")
update_regex = re.compile(
    r"^(UPDATE) +([a-zA-Z][^\s,='*;.]*?) +"
    r"(SET) +([a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *[a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*) +"
    r"(WHERE) +([a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*') *?(?: +(?:AND|OR) +[a-zA-Z][^\s,='*;.]*?(?:\.[a-zA-Z][^\s,='*;.]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*);$")
colcol = re.compile(
    r"[a-zA-Z][^\s,='*;.]*(?:\.[a-zA-Z][^\s,='*;.]*)? *= *[a-zA-Z][^\s,='*;.]*(?:\.[a-zA-Z][^\s,='*;.]*)? *(?:AND|OR|ORDER BY)?"
)

'''
splitter
——————–
Entradas:
(string) str: String al cual se le quiere hacer split.
(string) split_str: String por el cual se realizará el split.
——————–
Salida:
(lista[string]) Output: Retorna una lista con los strings separados por split_str ignorando espacios.
——————–
Extrae del string entregado los strings entre split_str y espacios.
'''
def splitter(str, split_str):
    return re.split(r" *"+split_str+" *", str.strip(" \n"))

'''
hasTableName
——————–
Entradas:
(string) str: String entregado a la función.
——————–
Salida:
(bool) Output: Retorna TRUE si contiene . y FALSE si no.
——————–
Verifica si el string contiene un . para reconocer si es de la forma nombreTabla.nombreColumna
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
getIndex
——————–
Entradas:
(string) col: String de la forma nombreColumna o nombreTabla.nombreColumna
(string) cols1: Rótulos de la tabla correspondiente a table1.
(string) cols2: Rótulos de la tabla correspondiente a table2.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(tupla(string, int)) Output: Retorna una tupla con el nombre de la tabla en la que se encuentra y la posición
en la que se encuentra.
——————–
Busca en cuál tabla se encuentra la columna col y su número de columna, retornándolo como una tupla.
'''
def getIndex(col, cols1, cols2 = [], table1 = "", table2 = ""):
    (table, col) = col.split('.') if hasTableName(col) else ("", col)
    if table is "" or table1 is "":
        try:
            return (table1, cols1.index(col))
        except:
            try:
                return (table2, cols2.index(col))
            except:
                raise ColumnError
    elif table == table1:
        try:
            return (table, cols1.index(col))
        except:
            raise ColumnError
    elif table == table2:
        try:
            return (table, cols2.index(col))
        except:
            raise ColumnError
    else:
        raise TableError


'''
check
——————–
Entradas:
(string) subexpr: Condición de la forma columna = valor o columna = columna.
(lista[strings]) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista[strings]) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si se cumple la condición de subexpr y en FALSE si no la cumple.
——————–
Recibe una condición de la forma columna = valor o columna = columna y retorna una función que se evalúa en
TRUE o FALSE si sus parametros cumplen esta condición o no.
'''

def check(subexpr, cols1, table1 = "", cols2 = [], table2 = ""):
    (A, B) = splitter(subexpr, '=')
    if not cols2:
        B = B.strip('\'')
        (*_, pos) = getIndex(A, cols1)
        return lambda row: row[pos] == B;
    else:
        (tableA, posA) = getIndex(A, cols1, cols2, table1, table2)
        if isColumn(B):
            (tableB, posB) = getIndex(B, cols1, cols2, table1, table2)
        else:
            tableB = ""
            B = B.strip('\'')
        if tableB == table1:
            if tableA == table1:
                return lambda row1, row2: row1[posA] == row1[posB]
            else:
                return lambda row1, row2: row2[posA] == row1[posB]
        elif tableB == table2:
            if tableA == table1:
                return lambda row1, row2: row1[posA] == row2[posB]
            else:
                return lambda row1, row2: row2[posA] == row2[posB]
        else:
            if tableA == table1:
                return lambda row1, row2: row1[posA] == B
            else:
                return lambda row1, row2: row2[posA] == B

'''
exprToBool
——————–
Entradas:
(string) expr: Condición que solo puede contener AND.
(lista[strings]) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista[strings]) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si la(s) lista(s) cumplen con la condición ingresada y FALSE si no la cumple.
——————–
Recibe un string que lo separa por AND. Luego llama a la función check y le entrega cada uno de estos strings.
'''
def exprToBool(expr, cols1, table1 = "", cols2 = [], table2 = ""):
    expr = splitter(expr, "AND")
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
(lista[strings]) cols1: Rótulos de la tabla correspondiente a table1.
(string) table1: Nombre de una tabla (se requiere cuando hay más de una tabla), por defecto es un string vacío.
(lista[strings]) cols2: Rótulos de la tabla correspondiente a table2.
(string) table2: Nombre de la segunda tabla.
——————–
Salida:
(función) Output: Se evalúa en TRUE si la(s) lista(s) cumplen con la condición ingresada y FALSE si no la cumple.
——————–
Recibe la condición para WHERE y retorna una función que se evalúa en TRUE o FALSE si sus parametros cumplen esta condición o no.
'''
def stmtToBool(stmt, cols1, table1 = "", cols2 = [], table2 = ""):
    stmt = splitter(stmt, "OR")
    stmt = [exprToBool(expr, cols1, table1, cols2, table2) for expr in stmt]
    if not cols2:
        return lambda row: any([expr(row) for expr in stmt])
    else:
        return lambda row1, row2: any([expr(row1, row2) for expr in stmt])

'''
select
——————–
Entradas:
(lista[string]) sel: Lista de columnas que se quieren mostrar, contiene solo '*' si se quieren mostrar todas las columnas.
(string) table: Tabla a la que se le quiere hacer SELECT.
(string) inner: Tabla a la que se le quiere hacer INNER JOIN.
(string) where: Condición para WHERE.
(string) order_by: Columna que se quiere ordenar.
(string) order_type: Especifica si se quiere ordenar de manera adcendente o descendente.
——————–
Salida:
(void) Output: No retorna.
——————–
Imprime los datos de la tabla que son seleccionados.
Puede juntar columnas de distintas tablas y ordenarlas de forma ascendente y descendente.
'''
def select(sel, table, inner, where, order_by, order_type):
    out = [] #Matriz con las filas que se deben mostrar.
    cols1 = [] #Lista con los rotulos de la primera tabla (FROM)
    cols2 = [] #Lista con los rotulos de la segunda tabla si es que esta existe (INNER JOIN)

    try:
        file = open(table+".csv", 'r', encoding="utf-8-sig")
    except FileNotFoundError:
        print("La tabla solicitada no existe.\n")
        return
    if not inner:
        conditions = re.findall(colcol, where) if where else []
        if conditions:
            print("Expresion de la forma Columna = Columna sin la presencia de un INNER JOIN\n")
            return
        with file:
            cols1 = file.readline().strip().split(",")
            try:
                stmt = stmtToBool(where, cols1) if where else lambda *_: True
            except ColumnError:
                print("Una o mas de las columnas solicitadas no existen.\n")
                return
            except TableError:
                print("Una o mas de las columnas de forma nombreTabla.nombreColumna no existen\n")
                return

            for line in file:
                row = line.strip().split(",")
                if stmt(row): #Si la fila cumple la condicion especificada en WHERE
                    out.append(row)
    else:
        conditions = re.findall(colcol, where)
        if not conditions:
            print("INNER JOIN requiere de una exprecion de la forma Columna = Columna en WHERE.\n")
            return
        try:
            join_file = open(inner+".csv", 'r', encoding="utf-8-sig")
        except FileNotFoundError:
            print("La tabla solicitada en INNER JOIN no existe.\n")
        with file, join_file:
            cols1 = file.readline().strip().split(",")
            cols2 = join_file.readline().strip().split(",")
            join_lines = join_file.read().splitlines()
            try:
                stmt = stmtToBool(where, cols1, table, cols2, inner)
            except ColumnError:
                print("Una o mas de las columnas solicitadas no existen.\n")
                return
            except TableError:
                print("Una o mas de las columnas de forma nombreTabla.nombreColumna no existen\n")
                return
            for line in file:
                row1 = line.strip().split(",")
                for join_line in join_lines:
                    row2 = join_line.strip().split(",")
                    if stmt(row1, row2): #Si la fila junto a una fila cualquiera de la segunda tabla cumplen la condicion especificada en where
                        out.append(row1+row2)

    if not out:
        print("La informacion solicitada no existe.\n")
        return

    cols = cols1+cols2
    for (i, col) in enumerate(sel):
        if col == '*': #Si la columna seleccionada es * entonces se deben mostar todas las columnas [0, 1, ..., Ncolumnas].
            sel = list(range(len(cols)))
            if inner:
                s = set()
                for condition in conditions:
                    col1, col2 = splitter(condition, '=')
                    if hasTableName(col1):
                        *_, col1 = col1.split('.')
                    if hasTableName(col2):
                        *_, col2 = col2.split('.')
                    if col1 == col2:
                        *_, pos1 = getIndex(col1,cols)
                        *_, pos2 = getIndex(col1, cols[pos1+1:])
                        pos2 += pos1+1
                    else:
                        *_, pos2 = getIndex(col2, cols)
                    if pos2 not in s:
                        s.add(pos2)
                        del sel[pos2]
            break
        else: #Si la columna no es * se remplaza en la lista por el indice que identifica a esta columna.
            try:
                (t, sel[i]) = getIndex(col, cols1, cols2, table, inner)
                if t == inner: #Si enuentra el indice en la segunda lista de columnas se debe empezar a contar desde donde termina la primera.
                    sel[i] += len(cols1)
            except ColumnError:
                print("Una o mas de las columnas solicitadas no existen.\n")
                return
            except TableError:
                print("Una o mas de las columnas de forma nombreTabla.nombreColumna no existen\n")
                return

    if order_by:
        try:
            (*_, i) = getIndex(order_by, cols) #Busca el indice de la columna que se quiere ordenar.
        except ColumnError:
            print("Una o mas de las columnas solicitadas no existen.\n")
            return
        except TableError:
            print("Una o mas de las columnas de forma nombreTabla.nombreColumna no existen\n")
            return
        out = sorted(out, key=lambda l: l[i])
        if order_type == "DESC":
            out = reversed(out)

    new_out = []
    max_lens = [0] * len(cols)
    for line in out:
        l = []
        for col in sel:
            l.append(line[col])
            max_lens[col] = max(max_lens[col], len(line[col])) #Almacena el tamaño de la string mas larga para cada columna seleccionada.
        new_out.append(l)

    row_format = ''.join("{:<"+str(max_lens[col]+2)+"}" for col in sel) #Crea un formato para que cada columna tenga de ancho 2 caracteres mas que la string mas larga que contiene.
    print('', *[row_format.format(*list) for list in new_out] , '', sep='\n')

'''
insert
——————–
Entradas:
(string) table: Nombre de la tabla a la que se le insertará datos.
(diccionario{string:string}) row_dat: Diccionario que contiene los datos que se ingresarán de la forma columna:valor.
——————–
Salida:
(void) Output: No retorna.
——————–
Añade una fila al final de la tabla entregada a la función con los datos que se han ingresado.
'''
def insert(table, row_dat):
    contador = 0

    try:
        file = open(table+".csv", "r", encoding='utf-8-sig')
    except FileNotFoundError:
        print("La tabla solicitada no existe.\n")
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

        if contador < len(row_dat): #Se actualizaron menos columnas que las indicadas.
            print("Una o mas de las columnas solicitadas no existen.\n")
            return
        else:
            file.write(string)

    print("\nSe ha insertado 1 fila.\n")

'''
update
——————–
Entradas:
(string) table: Nombre de la tabla a la que se le actualizarán los datos.
(lista[string]) set: Lista con el nombre de la columna que se quiere cambiar junto con el valor al cual se quiere actualizar.
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
        print("La tabla solicitada no existe.\n")
        return
    else:
        with file:
            lines = file.read().splitlines()

    with open(table+".csv", "w", encoding='utf-8-sig') as file:
        cols = lines[0].strip().split(",")
        try:
            set[0] = cols.index(set[0])
        except ValueError:
            print("Una columna indicada no existe.\n")
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
        print("\nNo se han actualizado filas.\n")
    elif count == 1:
        print("\nSe ha actualizado 1 fila.\n")
    else:
        print("\nSe han actualizado {} filas.\n".format(count))

running = True
print("Para salir ingrese el comando EXIT;")
while running:
    query = str(input("Ingrese su query: "))

    select_match = re.fullmatch(select_regex, query)
    insert_match = re.fullmatch(insert_regex, query)
    update_match = re.fullmatch(update_regex, query)

    if select_match:
        sel = splitter(select_match[2], ',')
        table = select_match[4]
        inner = select_match[6]
        where = select_match[8]
        order_by = select_match[10]
        order_type = select_match[11]
        if inner and not where:
            print("Error de Sintaxis!\n")
        else:
            select(sel, table, inner, where, order_by, order_type)
    elif insert_match:
        table = insert_match[2]
        keys = splitter(insert_match[3], ',')
        values = splitter(insert_match[5], ',')

        if len(keys) != len(values):
            print("Error de Sintaxis!\n")
        else:
            row_dat = dict(zip(keys,values))
            insert(table, row_dat)

    elif update_match:
        table = update_match[2]
        set = splitter(update_match[4], '=')
        stmt = update_match[6]
        update(table, set, stmt)

    elif query == "EXIT;":
        running = False
    else:
        print("Error de Sintaxis!\n")
