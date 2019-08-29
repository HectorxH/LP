import re
from pprint import pprint as pp

select_regex = re.compile(r"^(SELECT) +([^\s,=]+?(?: *, *[^\s,=]+?)*) +(FROM) +([^\s,=]+?)(?: +(INNER JOIN) +([^\s,=]+?))?(?: +(WHERE) +([^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:[^\s,=]+?(?:\.[^\s,=]+?)?|-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:[^\s,=]+?(?:\.[^\s,=]+?)?|-?\d+(?:\.\d+)?|'[^']*'))*))?(?: +(ORDER BY) +([^\s,=]+?(?:\.[^\s,=]+?)?) +(ASC|DESC))?;$")
insert_regex = re.compile(r"^(INSERT INTO) +([^\s,=]+?) +\( *([^\s,=]+?(?: *, *[^\s,=]+?)*) *\) +(VALUES) +\( *((?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *(?:-?\d+(?:\.\d+)?|'[^']*'))*) *\);$")
update_regex = re.compile(r"^(UPDATE) +([^\s,=]+?) +(SET) +([^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: *, *[^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*) +(WHERE) +([^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*')(?: +(?:AND|OR) +[^\s,=]+?(?:\.[^\s,=]+?)? *= *(?:-?\d+(?:\.\d+)?|'[^']*'))*);$")

def comaSplit(str):
    return re.split(r"(?:'|\")?(?: *),(?: *)(?:'|\")?", str.strip(" \n\'\""))

def orSplit(str):
    return re.split(r"(?:'|\")?(?: +)OR(?: +)(?:'|\")?", str.strip(" \n\'\""))

def andSplit(str):
    return re.split(r"(?:'|\")?(?: +)AND(?: +)(?:'|\")?", str.strip(" \n\'\""))

def equalSplit(str):
    return re.split(r"(?:'|\")?(?: *)=(?: *)(?:'|\")?", str.strip(" \n\'\""))

def check(subexpr, cols):
    (A, B) = equalSplit(subexpr)
    pos = cols.index(A)
    return lambda linea: linea[pos] == B;

def exprToBool(expr, cols):
    expr = andSplit(expr)
    expr = [check(subexpr, cols) for subexpr in expr]
    return lambda linea: all([subexpr(linea) for subexpr in expr])

def stmtToBool(stmt, cols):
    stmt = orSplit(stmt)
    stmt = [exprToBool(expr, cols) for expr in stmt]
    return lambda linea: any([expr(linea) for expr in stmt])

def select(match):
    select = comaSplit(match[2])
    table = match[4]
    inner = match[6]
    where = match[8]
    order_by = match[10]
    order_type = match[11]

    if not inner:
        out = []
        cols = []
        with open(table+".csv", "r", encoding='utf8') as file:
            cols = file.readline().strip().split(",")
            stmt = stmtToBool(where, cols) if where else lambda *_: True
            for line in file:
                line = line.strip().split(",")
                if stmt(line):
                    out.append(line)
    else:
        return print("f uwu")

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
    with open(table+".csv", "r", encoding='utf8') as file:
        cols = file.readline().strip().split(",")

    string = ""
    with open(table+".csv", "a", encoding='utf8') as file:
        for col in cols:
            if col in row_dat:
                string = string + row_dat[col] + ","
                contador+=1
            else:
                string = string + "" + ","
        string = string[:-1] + "\n"

        if len(row_dat) > contador:
            print("Error de Sintaxis!")

        file.write(string)

    print("Se ha insertado 1 fila.")

def update(table, set, stmt):
    count = 0

    with open(table+".csv", "r", encoding='utf8') as file:
        lines = file.read().splitlines()

    with open(table+".csv", "w", encoding='utf8') as file:
        cols = lines[0].strip().split(",")
        set[0] = cols.index(set[0])
        stmt = stmtToBool(stmt, cols)

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
        if select_match[5] and not select_match[7]:
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
            print(row_dat)
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
