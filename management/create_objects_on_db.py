from db import db_conn

db = db_conn.create_db_session()

list_procedures = []

drop_table_all = "DROP TABLE IF EXISTS receipts"
drop_type_all = "DROP TYPE IF EXISTS meal_type"

create_table_ingredients = """CREATE TABLE ingredients(
    id serial PRIMARY KEY,
    name VARCHAR (50) UNIQUE NOT NULL,
    carbs decimal NOT NULL,
    protein decimal NOT NULL,
    fat decimal NOT NULL,
    kcal integer NOT NULL);"""

create_enum_meal_type = "CREATE TYPE meal_type AS ENUM ('breakfast', 'lunch', 'dinner');"


create_table_receipe = """CREATE TABLE receipts(
   id serial PRIMARY KEY,
   version integer NOT NULL, 
   name VARCHAR (50) UNIQUE NOT NULL, 
   last_update date NOT NULL, 
   meal_type meal_type NOT NULL,
   grams integer, 
   carbs decimal, 
   protein decimal, 
   fat decimal, 
   kcal decimal 
);"""


create_table_ingr_rec = """CREATE TABLE ingr_rec(
   id serial PRIMARY KEY,
   receipts_id INTEGER,
   ingred_id INTEGER,
   grams integer NOT NULL,
   FOREIGN KEY (ingred_id) REFERENCES ingredients (id),
   FOREIGN KEY (receipts_id) REFERENCES receipts (id)
);"""

list_procedures.append(drop_table_all)
list_procedures.append(drop_type_all)
list_procedures.append(create_table_ingredients)
list_procedures.append(create_enum_meal_type)
list_procedures.append(create_table_receipe)
list_procedures.append(create_table_ingr_rec)

# print(list_procedures)
for item in list_procedures:
    print(item)
    db.execute(item)
    db.commit()