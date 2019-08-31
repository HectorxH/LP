import re

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

def comaSplit(str):
    return re.split(r"'?(?: *),(?: *)'?", str.strip(" \n\'"))

def orSplit(str):
    return re.split(r"'?(?: +)OR(?: +)'?", str.strip(" \n\'"))

def andSplit(str):
    return re.split(r"'?(?: +)AND(?: +)'?", str.strip(" \n\'"))

def equalSplit(str):
    return re.split(r"'?(?: *)=(?: *)'?", str.strip(" \n\'"))

def equalSplitVar(str):
    return re.split(r"(?: *)=(?: *)", str.strip())

def hasTableName(str):
    return '.' in str

def isColumn(str):
    return all(not c.isnumeric() and c is not '\'' for c in str)

def isString(str):
    return '\'' in str


def check(subexpr, cols1, table1 = "", cols2 = [], table2 = ""):
    (A, B) = equalSplitVar(subexpr)

    if not cols2:
        try:
            pos = cols1.index(A)
        except ValueError:
            print("Una columna solicitada en WHERE no existe.")
            raise ColumnError
        return lambda row: row[pos] == B;
    else:
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
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        return lambda row1, row2: row1[posA] == row1[posB]
                    elif tableA == table1 and tableB == table2:
                        try:
                            posA = cols1.index(colA)
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        return lambda row1, row2: row1[posA] == row2[posB]
                    elif tableA == table2 and tableB == table1:
                        try:
                            posA = cols2.index(colA)
                            posB = cols1.index(colB)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        return lambda row1, row2: row2[posA] == row1[posB]
                    elif tableA == table2 and tableB == table2:
                        try:
                            posA = cols2.index(colA)
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise tableError
                        return lambda row1, row2: row2[posA] == row2[posB]
                    else:
                        print("Una tabla indicada en WHERE no existe.")
                        raise TableError
                else:
                    if tableA == table1:
                        try:
                            posA = cols1.index(colA)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        try:
                            posB = cols1.index(colB)
                            return lambda row1, row2: row1[posA] == row1[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row1[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada en WHERE no existe.")
                                raise ColumnError
                    elif tableA == table2:
                        try:
                            posA = cols2.index(colA)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        try:
                            posB = cols1.index(colB)
                            return lambda row1, row2: row2[posA] == row1[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row2[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada en WHERE no existe.")
                                raise ColumnError
                    else:
                        print("Una tabla indicada en WHERE no existe.")
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
            if isColumn(B):
                if hasTableName(B):
                    if tableB == table1:
                        try:
                            posB = cols1.index(colB)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        try:
                            posA = cols1.index(colA)
                            return lambda row1, row2: row1[posA] == row1[posB]
                        except ValueError:
                            try:
                                posA = cols2.index(colA)
                                return lambda row1, row2: row2[posA] == row1[posB]
                            except ValueError:
                                print("Una columna solicitada en WHERE no existe.")
                                raise ColumnError
                    elif tableB == table2:
                        try:
                            posB = cols2.index(colB)
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
                            raise ColumnError
                        try:
                            posA = cols1.index(colA)
                            return lambda row1, row2: row1[posA] == row2[posB]
                        except ValueError:
                            try:
                                posB = cols2.index(colB)
                                return lambda row1, row2: row2[posA] == row2[posB]
                            except ValueError:
                                print("Una columna solicitada en WHERE no existe.")
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
                                print("Una columna solicitada en WHERE no existe.")
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
                                    print("Una columna solicitada en WHERE no existe.")
                                    raise ColumnError
                        except ValueError:
                            print("Una columna solicitada en WHERE no existe.")
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
                        print("Una columna solicitada en WHERE no existe.")
                        raise ColumnError

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

def select(match):
    select = comaSplit(match[2])
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
        print("La tabla solicitada en FROM no existe.")
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
        set[0] = cols.index(set[0])
        try:
            stmt = stmtToBool(stmt, cols)
        except (ColumnError, TableError):
            return
        for line in lines:
            line = line.strip().split(",")
            if stmt(line):
                line[set[0]] = set[1]
                count += 1
            line = ",".join(line)+"\n"
            file.write(line)

    if count == 0:
        print("No se han actualizado filas.")
    elif count == 1:
        print("Se ha actualizado 1 fila.")
    else:
        print("Se han actualizado {} filas.".format(count))

running = True
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
