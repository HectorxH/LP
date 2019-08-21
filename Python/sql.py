import re

search_regx = re.compile("SELECT(?: )+(.+)(?: )+FROM(?: )+(\w+)?((?: )+INNER JOIN(?: )+(\w+))?((?: )+WHERE(?: )+(\w+|\w+.\w+)(?: *)?=(?: *)?(\w+|'.+'|\w+.\w+)((?: )+(AND|OR)(?: )+(\w+|\w+.\w+)( *)?=(?: *)?(\w+|'.+'|\w+.\w+))*)?((?: )+ORDER BY(?: )+(\w+|\w+.\w+)(?: )+(ASC|DESC))?;")
insert_regx = re.compile("INSERT INTO(?: )+(\w+)(?: )+\((?: *)?(\w+|\w+.\w+)((?: *)?,(?: *)?(\w+|\w+.\w+))*(?: *)?\)(?: )+VALUES(?: )+\((?: *)?(\w+|\w+.\w+)((?: *)?,(?: *)?(\w+|\w+.\w+))*(?: *)?\);")
update_regx = re.compile("UPDATE(?: )+(\w+)(?: )+SET(?: )+(\w+|\w+.\w+)(?: *)?=(?: *)?(\w+|'.+'|\w+.\w+)((?: *)?,(?: *)?(\w+|\w+.\w+)(?: *)?=(?: *)?(\w+|'.+'|\w+.\w+))*(?: )+WHERE(?: )+(\w+|\w+.\w+)(?: *)?=(?: *)?(\w+|'.+'|\w+.\w+)((?: )+(AND|OR)(?: )+(\w+|\w+.\w+)(?: *)?=(?: *)?(\w+|'.+'|\w+.\w+))*;")


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
        print("Insert command.")
        print(insert_match.groups())
    elif update_match:
        print("Update command.")
        print(update_match.groups())
    elif query == "EXIT":
        running = False
    else:
        print("Error de Sintaxis!")
