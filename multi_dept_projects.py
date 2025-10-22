import sqlite3

# Connect to databae is given by ourself
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Drop tables if already exist in the table as you go
cursor.executescript("""
DROP TABLE IF EXISTS EmployeeProjects;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Departments;
""")

# Create tables
cursor.executescript("""
CREATE TABLE Departments (
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName TEXT
);

CREATE TABLE Employees (
    EmployeeID INTEGER PRIMARY KEY,
    Name TEXT,
    DepartmentID INTEGER,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

CREATE TABLE Projects (
    ProjectID INTEGER PRIMARY KEY,
    ProjectName TEXT
);

CREATE TABLE EmployeeProjects (
    EmployeeID INTEGER,
    ProjectID INTEGER,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);
""")

# Insert sample data
departments = [
    (101, 'HR'),
    (102, 'Finance'),
    (103, 'IT')
]
cursor.executemany("INSERT INTO Departments VALUES (?, ?)", departments)

employees = [
    (1, 'Alice', 101),
    (2, 'Bob', 101),
    (3, 'Charlie', 102),
    (4, 'David', 103),
    (5, 'Eve', 102),
]
cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?)", employees)

projects = [
    (1, 'Project A'),
    (2, 'Project B'),
    (3, 'Project C')
]
cursor.executemany("INSERT INTO Projects VALUES (?, ?)", projects)

employee_projects = [
    (1, 1),  # Alice - Project A
    (2, 1),  # Bob - Project A
    (3, 1),  # Charlie - Project A (=> HR + Finance)
    (4, 2),  # David - Project B (only IT)
    (5, 3),  # Eve - Project C (only Finance)
]
cursor.executemany("INSERT INTO EmployeeProjects VALUES (?, ?)", employee_projects)

conn.commit()

# SQL Query to find projects with employees from more than one department
query = """
SELECT 
    p.ProjectName
FROM 
    Projects p
JOIN 
    EmployeeProjects ep ON p.ProjectID = ep.ProjectID
JOIN 
    Employees e ON ep.EmployeeID = e.EmployeeID
GROUP BY 
    p.ProjectName
HAVING 
    COUNT(DISTINCT e.DepartmentID) > 1;
"""

cursor.execute(query)
rows = cursor.fetchall()

print("Projects with employees from more than one department:")
print("------------------------------------------------------")
for row in rows:
    print(row[0])

conn.close()
