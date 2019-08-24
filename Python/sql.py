import re

search_regx = re.compile(r"(SELECT)(?: +)((?:[\w\*]+)(?:(?: *),(?: *)(?:\w+))*)(?: +)(FROM)(?: +)(\w+)(?:(?: +)(INNER JOIN)(?: +)(\w+))?(?:(?: +)(WHERE)(?: +)((?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\w+|\w+\.\w+|'.*')(?:(?: +)(?:AND|OR)(?: +)(?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\w+|\w+\.\w+|'.*'))*))?(?:(?: +)(ORDER BY)(?: +)(\w+|\w+\.\w+)(?: +)(ASC|DESC))?;$")
insert_regx = re.compile(r"(INSERT INTO)(?: +)(\w+)(?: +)\((?: *)((?:\w+)(?:(?: *),(?: *)(?:\w+))*)(?: *)\)(?: +)(VALUES)(?: +)\((?: *)((?:\w+|\w+\.\w+|'.*')(?:(?: *),(?: *)(?:\w+|\w+\.\w+|'.*'))*)(?: *)\);$")
update_regx = re.compile(r"(UPDATE)(?: +)(\w+)(?: +)(SET)(?: +)((?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\d+|\d+\.\d+|'.*')(?:(?: *),(?: *)(?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\d+|\d+\.\d+|'.*'))*)(?: +)(WHERE)(?: +)((?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\d+|\d+\.\d+|'.*')(?:(?: +)(?:AND|OR)(?: +)(?:\w+|\w+\.\w+)(?: *)=(?: *)(?:\d+|\d+\.\d+|'.*'))*);$")

def comaSplit(str):
    return re.split(r"'?(?: *),(?: *)'?", str.strip(" \n'"))

def orSplit(str):
    return re.split(r"'?(?: *)OR(?: *)'?", str.strip(" \n'"))

def andSplit(str):
    return re.split(r"'?(?: *)AND(?: *)'?", str.strip(" \n'"))

def equalSplit(str):
    return re.split(r"'?(?: *)=(?: *)'?", str.strip(" \n'"))

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

def search():
    

    return

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

    print("Se ha insertado 1 fila.")

def update(table, set, stmt):
    count = 0

    file = open(table+".csv", "r")
    lines = file.read().splitlines()
    file.close()

    file = open(table+".csv", "w")

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
    file.close()
    if count == 0:
        print("No se han actualizado filas.")
    elif count == 1:
        print("Se ha actualizado 1 fila.")
    else:
        print("Se han actualizado {} filas.".format(count))

running = True
while running:
    query = str(input("Ingrese su query: "))

    search_match = re.fullmatch(search_regx, query)
    insert_match = re.fullmatch(insert_regx, query)
    update_match = re.fullmatch(update_regx, query)

    if search_match:
        if search_match[5] and not search_match[7]:
            print("Error de Sintaxis!")
        else:
            print("Search command.")
            print(search_match.groups())
    elif insert_match:
        tabla = insert_match[2]
        keys = comaSplit(insert_match[3])
        values = comaSplit(insert_match[5])

        if len(keys) != len(values):
            print("Error de Sintaxis!")
        else:
            fila_dat = dict(zip(keys,values))
            print(fila_dat)
            insert(tabla, fila_dat)

    elif update_match:
        tabla = update_match[2]
        set = equalSplit(update_match[4])
        stmt = update_match[6]
        update(tabla, set, stmt)

    elif query == "EXIT;":
        running = False
    else:
        print("Error de Sintaxis!")
