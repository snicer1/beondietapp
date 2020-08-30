from db import db_conn
import csv

db = db_conn.create_db_session()

# same import and setup statements as above

# f = open("./db/data_ingredient.csv")
# reader = csv.reader(f)
#
#
# for name, carbs, protein, fat, kcal in reader:  # loop gives each column a name
#     db.execute("INSERT INTO ingredients (name, carbs, protein, fat, kcal) VALUES (:name, :carbs, :protein, :fat, :kcal)",
#                {"name": name, "carbs": float(carbs),
#                 "protein": float(protein), "fat": float(fat), "kcal": int(kcal)})
#     print(f"Added ingredient {name}.")
#
# db.commit()

db.execute("""UPDATE receipts SET (carbs, protein, fat, kcal) = (SELECT final_carbs, final_protein, final_fat,  final_kcal FROM (
    SELECT 
    round(sum((inrec.grams * i.carbs)/100),2) final_carbs, 
    round(sum((inrec.grams * i.protein)/100),2) final_protein, 
    round(sum((inrec.grams * i.fat)/100),2) final_fat, 
    round(sum((inrec.grams * i.kcal)/100),2) final_kcal, 
    receipts_id 
    FROM receipts r, 
    ingredients i, 
    ingr_rec inrec 
    WHERE r.id = inrec.receipts_id and i.id = inrec.ingred_id  
    group by receipts_id)
 subselect WHERE receipts.id = subselect.receipts_id);
 
    
    """)

db.commit()