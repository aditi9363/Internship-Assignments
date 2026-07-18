from database import Database
db = Database("company.db")

db.open()

#-----------------Create Table-----------------
db.create_table(
    "employees",
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "role": "TEXT",
    }
)

#------------------List Tables-----------------
print("\nTables in Database:")
print(db.list_tables())

#----------------Insert Records----------------
id1 = db.write(
    "employees",
    {
        "name": "Ira",
        "role": "Developer"
    }
)

id2 = db.write(
    "employees",
    {
        "name": "Virat",
        "role": "Tester"

    }
)
print("\nInserted Row IDs:", id1, id2)

#--------------Read All Records------------------
print("\nEmployees:")

rows = db.read("employees")

for row in rows:
    print(row)

#-----------------Update Record-------------------
updated = db.update(
    "employees",
    {"role": "Senior Tester"},
    "name = ?",
    ("Virat",)
)
print("\nRows Updated:", updated)
print("\nEmployees After Update:")

rows = db.read("employees")

for row in rows:
    print(row)

#-----------------Add New Column-------------------
db.update_table(
    "employees",
    add_column=("salary", "REAL")
)


#-------------Delete One Record---------------------
deleted = db.delete(
    "employees",
    "name = ?",
    ("Virat",)
)
print("\nRows Deleted:", deleted)
print("\nEmployees After Delete:")

rows = db.read("employees")

for row in rows:
    print(row)

#-----------------Rename Table----------------------
db.update_table(
    "employees",
    rename_to="staff"
)

print("\nTables in Database:")
print(db.list_tables())

#------------------Delete Table----------------------
db.delete_table("staff")

print("\nAfter Deleting Table:")
print(db.list_tables())

# Close database
db.close()