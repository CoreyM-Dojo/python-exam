def create_query(table, data):
    dict_keys = data.keys()
    start = f"INSERT INTO {table} ("
    keys = " "
    values = " VALUES ( "
    for i in range(len(dict_keys)):
        i = int(i)
        keys+=f"{list(dict_keys)[i]}"
        values+=f"%({list(dict_keys)[i]})s"
        if i < len(dict_keys)-1:
            keys+=","
            values+=","
    keys+=" )"
    values+=" )"
    result = start+keys+values+";"
    return result

def get_by(table, key):
    query = f"SELECT * FROM {table} WHERE {key} = %({key})s;"
    return query

def update_query(table, data):
    dict_keys = data.keys()
    start = f"Update {table} SET "
    set_string=""
    for i in range(len(dict_keys)):
        key = list(dict_keys)[i]
        set_string+=f"{key}=%({key})s"
        if i < len(dict_keys)-1:
            set_string+=","
    filter = " WHERE id = %(id)s"
    return start+set_string+filter+";"

def delete_query(table):
    query = f"DELETE FROM {table} WHERE id = %(id)s;"
    return query

def one_to_many(table1, table2, filtered=True, from_many=False):
    query = f"SELECT * FROM {table1} LEFT JOIN {table2}"
    if from_many:
        query+=f" ON {table1}.{table2}_id = {table2}.id"
    else:
        query+=f" ON {table1}.id = {table2}.{table1}_id"
    if filtered:
        query+=f" WHERE {table1}.id = %(id)s"
    return query

def many_to_many(table1, table2, joining_table, key=False):
    query = f"SELECT * FROM {table1} LEFT JOIN {joining_table} ON {table1}.id = {joining_table}.{table1}_id LEFT JOIN {table2} ON {joining_table}.{table2}_id = {table2}.id" 
    if key:
        query += f" WHERE {table1}.id = %(id)s;"
    return query


        
# data = {
#     "name": "Corey",
#     "age": 29,
#     "test": True

# }

# print(get_by("users", "email"))
# print(one_to_many("recipes", "users", True, True))
# print(many_to_many("authors", "books", "favorites", True))
# print(many_to_many("books", "authors", "favorites", True))
# print(update_query("users", data))
# print(delete_query("users"))


