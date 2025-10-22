import sqlite3

conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create table
cursor.execute("DROP TABLE IF EXISTS Employees;")
cursor.execute("""
CREATE TABLE Employees (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    DepartmentName TEXT,
    Salary INTEGER
);
""")

# Insert sample data
sample_data = [
    ('Alice', 'HR', 60000),
    ('Bob', 'HR', 55000),
    ('Charlie', 'HR', 70000),
    ('David', 'Finance', 90000),
    ('Eve', 'Finance', 85000),
    ('Frank', 'Finance', 88000),
    ('Grace', 'IT', 120000),
    ('Hannah', 'IT', 110000),
    ('Ian', 'IT', 115000),
    ('Jack', 'IT', 125000),
    ('Kathy', 'IT', 95000),
    ('Leo', 'IT', 97000),
    ('Mona', 'IT', 89000),
    ('Nina', 'IT', 87000),
    ('Oscar', 'IT', 105000)
]

cursor.executemany("INSERT INTO Employees (Name, DepartmentName, Salary) VALUES (?, ?, ?);", sample_data)
conn.commit()

# Query: To Find departments with total salary > 500000 and more than 10 employees
query = """
SELECT DepartmentName,
       SUM(Salary) AS TotalSalary
FROM Employees
GROUP BY DepartmentName
HAVING SUM(Salary) > 500000 AND COUNT(EmployeeID) > 10;
"""

cursor.execute(query)
rows = cursor.fetchall()

print("DepartmentName | TotalSalary")
print("-----------------------------")
for row in rows:
    print(f"{row[0]} | {row[1]}")

conn.close()
