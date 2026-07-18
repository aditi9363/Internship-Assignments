from database import Database

# Create Database object
db = Database("company.db")

# Open database
db.open()

# Create table
db.create_table(
    "employees",
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "role": "TEXT"
    }
)

#--------PART 1 : Transaction + Rollback Demonstration--------

print("\n========== Transaction Demonstration ==========")

try:

    # Start a transaction
    db.conn.execute("BEGIN")

    print("\nWriting first employee...")

    db._execute(
        'INSERT INTO "employees"(name, role) VALUES (?, ?)',
        ("Ira", "Developer")
    )

    # Force an error
    print("Forcing an error...")

    raise Exception("Something went wrong!")

    # This statement never executes
    db._execute(
        'INSERT INTO "employees"(name, role) VALUES (?, ?)',
        ("Virat", "Tester")
    )

    db.conn.commit()

except Exception as e:

    print("Error:", e)

    print("Rolling back transaction...")

    db.conn.rollback()

print("\nEmployees after rollback:")

rows = db.read("employees")

for row in rows:
    print(row)

if len(rows) == 0:
    print("Database unchanged (All-or-Nothing successful)")

#-------------PART 2 : SQL Injection Demonstration---------------

print("\n========== SQL Injection Demonstration ==========")

malicious_input = "Robert'); DROP TABLE employees;--"

db.write(
    "employees",
    {
        "name": malicious_input,
        "role": "Tester"
    }
)

print("\nStored Record:")

rows = db.read("employees")

for row in rows:
    print(row)

print("\nTables still present:")

print(db.list_tables())

# Close database
db.close()

#Comparison

#1. Raw sqlite3
#- Provides direct control over SQL queries.
#- Lightweight and fast.
#- Suitable for desktop applications, small projects, and learning SQL.

#2. Plain File Storage
#- Stores data in text, CSV, or JSON files.
#- No SQL support.
#- No transactions or relationships.
#- Suitable for small datasets or configuration files.

#3. SQLAlchemy (ORM)
#- Uses Python classes instead of writing SQL manually.
#- Simplifies database operations.
#- Supports multiple database systems.
#- Best suited for large applications and web development.

