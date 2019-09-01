import re
from pprint import pprint as pp

class ColumnError(Exception):
    pass

class TableError(Exception):
    pass

select_regex = re.compile(
    r"^(SELECT) +((?:[a-zA-Z][^\s,='*]*?(?: *, *[a-zA-Z][^\s,='*]*?)*)|\*) +"
    r"(FROM) +([a-zA-Z][^\s,='*]*?)"
    r"(?: +(INNER JOIN) +([a-zA-Z][^\s,='*]*?))?"
    r"(?: +(WHERE) +([a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:[a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)?|-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:[a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)?|-?\d+(?:\.\d+)?|'[^']*'))*))?"
    r"(?: +(ORDER BY) +([a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)?) +(ASC|DESC))?;$")
insert_regex = re.compile(
    r"^(INSERT INTO) +([a-zA-Z][^\s,='*]*?) +\( *([a-zA-Z][^\s,='*]*?(?: *, *[a-zA-Z][^\s,='*]*?)*) *\) +"
    r"(VALUES) +\( *((?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *(?:-?\d+(?:\.\d+)?|'[^']*'))*) *\);$")
update_regex = re.compile(
    r"^(UPDATE) +([a-zA-Z][^\s,='*]*?) +"
    r"(SET) +([a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *[a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*) +"
    r"(WHERE) +([a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[a-zA-Z][^\s,='*]*?(?:\.[a-zA-Z][^\s,='*]*?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*);$")

def comaSplit(str):
    return re.split(r"(?: *),(?: *)", str.strip(" \n"))

def orSplit(str):
    return re.split(r"(?: +)OR(?: +)", str.strip(" \n"))

def andSplit(str):
    return re.split(r"(?: +)AND(?: +)", str.strip(" \n"))

def equalSplit(str):
    return re.split(r"(?: *)=(?: *)", str.strip(" \n"))

def equalSplitVar(str):
    return re.split(r"(?: *)=(?: *)", str.strip(" \n"))

def hasTableName(str):
    return '.' in str

def isColumn(str):
    return str[0].isalpha()

def getIndex(str, cols1, cols2 = [], table1 = "", table2 = ""):
    (table, col) = str.split('.') if hasTableName(str) else ("", str)
    if table is "" or table1 is "":
        try:
            return (table1, cols1.index(col))
        except:
            try:
                return (table2, cols2.index(col))
            except:
                print("Una o mas de las columnas solicitadas no existen.")
                raise ColumnError
    elif table == table1:
        try:
            return (table, cols1.index(col))
        except:
            print("Una o mas de las columnas solicitadas no existen.")
            raise ColumnError
    elif table == table2:
        try:
            return (table, cols2.index(col))
        except:
            print("Una o mas de las columnas solicitadas no existen.")
            raise ColumnError
    else:
        print("Una o mas de las columnas de forma nombreTabla.nombreColumna no existen")
        raise TableError

def check(subexpr, cols1, table1 = "", cols2 = [], table2 = ""):
    (A, B) = equalSplit(subexpr)
    if not cols2:
        B.strip('\'')
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

def exprToBool(expr, cols1, table1 = "", cols2 = [], table2 = ""):
    expr = andSplit(expr)
    expr = [check(subexpr, cols1, table1, cols2, table2) for subexpr in expr]
    if not cols2:
        return lambda row: all([subexpr(row) for subexpr in expr])
    else:
        return lambda row1, row2: all([subexpr(row1, row2) for subexpr in expr])

def stmtToBool(stmt, cols1, table1 = "", cols2 = [], table2 = ""):
    stmt = orSplit(stmt)
    stmt = [exprToBool(expr, cols1, table1, cols2, table2) for expr in stmt]
    if not cols2:
        return lambda row: any([expr(row) for expr in stmt])
    else:
        return lambda row1, row2: any([expr(row1, row2) for expr in stmt])

def select(sel, table, inner, where, order_by, order_type):
    out = []
    cols1 = []
    cols2 = []
    try:
        file = open(table+".csv", 'r', encoding="utf-8-sig");
    except FileNotFoundError:
        print("La tabla solicitada no existe.")
        return
    if not inner:
        with file:
            cols1 = file.readline().strip().split(",")
            try:
                stmt = stmtToBool(where, cols1) if where else lambda *_: True
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
    cols = cols1+cols2

    for (i, col) in enumerate(sel):
        if col == '*':
            sel = range(len(cols))
            break
        else:
            try:
                (t, sel[i]) = getIndex(col, cols1, cols2, table, inner)
                if t == inner:
                    sel[i] += len(cols1)
            except (ColumnError, TableError):
                return

    if order_by:
        try:
            (*_, i) = getIndex(order_by, cols)
        except (ColumnError, TableError):
            return
        out = sorted(out, key=lambda l: l[i])
        if order_type == "DESC":
            out = reversed(out)

    if not out:
        print("La informacion solicitada no existe.")
        return

    new_out = []
    max_lens = [0] * len(cols)
    for line in out:
        l = []
        for col in sel:
            l.append(line[col])
            max_lens[col] = max(max_lens[col], len(line[col]))
        new_out.append(l)

    row_format = ''.join("{:<"+str(max_lens[col]+1)+"}" for col in sel)
    print('', *[row_format.format(*list) for list in new_out] , '', sep='\n')


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
        sel = comaSplit(select_match[2])
        table = select_match[4]
        inner = select_match[6]
        where = select_match[8]
        order_by = select_match[10]
        order_type = select_match[11]
        if inner and not where: #INNER JOIN sin un WHERE
            print("Error de Sintaxis!")
        else:
            select(sel, table, inner, where, order_by, order_type)
    elif insert_match:
        table = insert_match[2]
        keys = comaSplit(insert_match[3])
        values = comaSplit(insert_match[5])

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
