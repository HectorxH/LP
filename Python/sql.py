import re

search_regx = re.compile(r"(SELECT)(?: +)(.+)(?: +)(FROM)(?: +)(\w+)?(?:(?: +)(INNER JOIN)(?: +)(\w+))?(?:(?: +)(WHERE)(?: +)(.+?))?(?:(?: +)(ORDER BY)(?: +)(\w+|\w+.\w+)(?: +)(ASC|DESC))?;")
insert_regx = re.compile(r"(INSERT INTO)(?: +)(.+)(?: +)\((?: *)?(.+)(?: *)?\)(?: +)(VALUES)(?: +)\((?: *)?(.*)(?: *)?\);")
update_regx = re.compile(r"(UPDATE)(?: +)(.+)(?: +)(SET)(?: +)(.+)(?: +)(WHERE)(?: +)(.+);")


def search():


    return

def insert():


    return


def update():




    return


running = True
while running:
    query = str(input("Ingrese su query: "))

    search_match = re.fullmatch(search_regx, query)
    insert_match = re.fullmatch(insert_regx, query)
    update_match = re.fullmatch(update_regx, query)

    if search_match:
        print("Search command.")
        print(search_match.groups())
    elif insert_match:
        tabla = insert_match[2]

        keys = insert_match[3].strip().split(",");
        keys = list(map(lambda str: str.strip(" '"), keys))

        values = insert_match[5].strip().split(",")
        values = list(map(lambda str: str.strip(" '"), values))
        
        if len(keys) != len(values):
            print("Error de Sintaxis!")
        else:
            fila_dat = dict(zip(keys,values))
            #insert(tabla, fila_dat)
    elif update_match:
        print("Update command.")
        print(update_match.groups())
    elif query == "EXIT;":
        running = False
    else:
        print("Error de Sintaxis!")
